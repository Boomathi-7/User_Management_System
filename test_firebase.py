import os
import firebase_admin
from firebase_admin import credentials, db

cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
firebase_url = os.environ.get("FIREBASE_DB_URL")

if not cred_path or not firebase_url:
    raise Exception("Set GOOGLE_APPLICATION_CREDENTIALS and FIREBASE_DB_URL before running!")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {'databaseURL': firebase_url})

try:
    ref = db.reference("test") 
    ref.push({"message": "Firebase connection successful!"})
    print("✅ Firebase write successful!")
except Exception as e:
    print("❌ Firebase write failed!")
    print(e)
