import os
import firebase_admin
from firebase_admin import credentials, db

cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if not cred_path:
    raise Exception("GOOGLE_APPLICATION_CREDENTIALS environment variable is missing!")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": os.environ.get("FIREBASE_DB_URL")
    })

def get_db():
    return db

def push_notification(data):
    ref = db.reference("notifications")
    ref.push(data)
