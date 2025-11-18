import os
from functools import wraps
from flask import Flask, request, jsonify
from firebase_client import get_db, push_notification

app = Flask(__name__)

API_TOKEN = os.environ.get("API_TOKEN", "static-test-token")
db = get_db()


# Authentication decorator
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing bearer token"}), 401
        token = auth.split(" ", 1)[1]
        if token != API_TOKEN:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


# Home route (for browser)
@app.route("/", methods=["GET"])
def home():
    return {"message": "Hello World!"}, 200


# CREATE USER
@app.route("/users", methods=["POST"])
@auth_required
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data or "role" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    ref = db.reference("users")
    new_user = ref.push({
        "name": data["name"],
        "email": data["email"],
        "role": data["role"]
    })

    push_notification({
        "type": "user_created",
        "user_id": new_user.key
    })

    return jsonify({"id": new_user.key, **data}), 201


# LIST USERS
@app.route("/users", methods=["GET"])
@auth_required
def list_users():
    users = db.reference("users").get()
    if not users:
        return jsonify([]), 200
    result = [{"id": key, **value} for key, value in users.items()]
    return jsonify(result), 200


# GET USER
@app.route("/users/<user_id>", methods=["GET"])
@auth_required
def get_user(user_id):
    user = db.reference(f"users/{user_id}").get()
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": user_id, **user}), 200

# UPDATE USER
@app.route("/users/<user_id>", methods=["PUT"])
@auth_required
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid payload"}), 400

    ref = db.reference(f"users/{user_id}")
    if not ref.get():
        return jsonify({"error": "not found"}), 404

    ref.update(data)
    return jsonify({"id": user_id, **ref.get()}), 200


# DELETE USER
@app.route("/users/<user_id>", methods=["DELETE"])
@auth_required
def delete_user(user_id):
    ref = db.reference(f"users/{user_id}")
    if not ref.get():
        return jsonify({"error": "not found"}), 404

    ref.delete()
    return "", 204


# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
