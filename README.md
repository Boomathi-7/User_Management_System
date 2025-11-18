# Firebase + Flask REST API

This repository contains a minimal Flask REST API that uses Google Firebase Firestore as a persistent store.

## Features
- Endpoints: POST /users, GET /users, GET /users/<id>, PUT /users/<id>, DELETE /users/<id>
- Simple token authentication (Bearer token). Optionally verify Firebase ID tokens.
- Writes a `notifications` document when a user is created (simulated background job).
- Dockerfile included.
- Unit tests and GitHub Actions workflow example.

---

## Setup (local)

1. Create a Python virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure Firebase credentials **(do not commit keys)**:
- Option A: set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your service account JSON.
- Option B: set `FIREBASE_CREDENTIALS_JSON` to the raw JSON content of the service account.

Example (bash):
```bash
export FIREBASE_CREDENTIALS_JSON="$(cat ~/keys/firebase-service-account.json)"
export API_TOKEN="static-test-token"
# To use Firebase Auth verify instead of static token:
export USE_FIREBASE_AUTH=1
```

3. Run the app:
```bash
python app.py
```

## Docker

Build and run:
```bash
docker build -t firebase-flask-api:local .
docker run -p 5000:5000 -e FIREBASE_CREDENTIALS_JSON="$FIREBASE_CREDENTIALS_JSON" -e API_TOKEN="static-test-token" firebase-flask-api:local
```

## Authentication

The API accepts `Authorization: Bearer <token>` header.
- By default the app checks a static token from `API_TOKEN` environment variable.
- To verify Firebase ID tokens instead, set `USE_FIREBASE_AUTH=1` and ensure the Firebase Admin SDK is configured with service account credentials. The server will call `firebase_admin.auth.verify_id_token()` for each request.

**Production improvements**:
- Use short-lived access tokens (OAuth2) or JWTs minted by a trusted auth service.
- Use Firebase Authentication + IAM to issue and validate tokens server-side; cache token verification results and use proper rejection/rotation.
- Rate-limit endpoints and use HTTPS / mTLS for services.

## Example curl commands

Replace `http://localhost:5000` and `STATIC_TOKEN` accordingly.

Create user:
```bash
curl -X POST http://localhost:5000/users -H "Authorization: Bearer STATIC_TOKEN" -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com","role":"admin"}'
```

List users:
```bash
curl http://localhost:5000/users -H "Authorization: Bearer STATIC_TOKEN"
curl http://localhost:5000/users?role=admin -H "Authorization: Bearer STATIC_TOKEN"
```

Get single user:
```bash
curl http://localhost:5000/users/<id> -H "Authorization: Bearer STATIC_TOKEN"
```

Update user:
```bash
curl -X PUT http://localhost:5000/users/<id> -H "Authorization: Bearer STATIC_TOKEN" -H "Content-Type: application/json" -d '{"role":"user"}'
```

Delete user:
```bash
curl -X DELETE http://localhost:5000/users/<id> -H "Authorization: Bearer STATIC_TOKEN"
```


