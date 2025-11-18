# User Management System
# Firebase + Flask REST API

Minimal Flask REST API using Firebase Realtime Database.

## Features

* Endpoints: `POST /users`, `GET /users`, `GET /users/<id>`, `PUT /users/<id>`, `DELETE /users/<id>`
* Simple **static token authentication** (`Bearer token`)
* Simulated background job: writes a `notifications` document when a user is created
* Firebase Realtime Database integration

---

## Setup (local)

1. Create Python virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Configure Firebase credentials **(do not commit keys)**:

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=E:\SIH-2025\Task\secrets\serviceAccount.json
set FIREBASE_DB_URL=https://<your-project-id>.firebaseio.com
set API_TOKEN=static-test-token
```

3. Run the app:

```cmd
python app.py
```

---

## Authentication

* Use `Authorization: Bearer <token>` header.
* Static token is checked from `API_TOKEN` environment variable.

---

## Example curl commands

Create user:

```cmd
curl -X POST http://127.0.0.1:5000/users -H "Authorization: Bearer static-test-token" -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"email\":\"alice@example.com\",\"role\":\"admin\"}"
```

List users:

```cmd
curl http://127.0.0.1:5000/users -H "Authorization: Bearer static-test-token"
curl http://127.0.0.1:5000/users?role=admin -H "Authorization: Bearer static-test-token"
```

Get single user:

```cmd
curl http://127.0.0.1:5000/users/<id> -H "Authorization: Bearer static-test-token"
```

Update user:

```cmd
curl -X PUT http://127.0.0.1:5000/users/<id> -H "Authorization: Bearer static-test-token" -H "Content-Type: application/json" -d "{\"role\":\"user\"}"
```

Delete user:

```cmd
curl -X DELETE http://127.0.0.1:5000/users/<id> -H "Authorization: Bearer static-test-token"
```

---
