import os
import json
import pytest
from unittest.mock import MagicMock, patch
import app as app_module

API_TOKEN = "static-test-token"

@pytest.fixture
def client():
    os.environ["API_TOKEN"] = API_TOKEN
    os.environ["USE_FIREBASE_AUTH"] = "0"
    app = app_module.app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class DummyDoc:
    def __init__(self, id, data):
        self.id = id
        self._data = data
        self.exists = True
    def to_dict(self):
        return self._data
    def get(self):
        return self

class DummyCollection:
    def __init__(self):
        self.store = {}
    def document(self, doc_id=None):
        if doc_id is None:
            # create new id
            new_id = "id_" + str(len(self.store)+1)
            self.store[new_id] = {}
            return MagicMock(id=new_id, set=lambda d: self.store.update({new_id:d}), update=lambda d: self.store[new_id].update(d), delete=lambda : self.store.pop(new_id, None), get=lambda : DummyDoc(new_id, self.store[new_id]))
        else:
            if doc_id in self.store:
                return MagicMock(id=doc_id, set=lambda d: self.store.update({doc_id:d}), update=lambda d: self.store[doc_id].update(d), delete=lambda : self.store.pop(doc_id, None), get=lambda : DummyDoc(doc_id, self.store[doc_id]))
            else:
                # simulate non-existent
                m = MagicMock(id=doc_id)
                doc = MagicMock(exists=False)
                m.get = lambda : doc
                m.delete = lambda : None
                return m
    def where(self, *args, **kwargs):
        # return self as an iterable
        return self
    def stream(self):
        for k,v in self.store.items():
            yield DummyDoc(k,v)

class DummyDB:
    def __init__(self):
        self.collections = {}
    def collection(self, name):
        if name not in self.collections:
            self.collections[name] = DummyCollection()
        return self.collections[name]

@pytest.fixture(autouse=True)
def patch_db():
    dummy = DummyDB()
    with patch('firebase_client.get_db', return_value=dummy):
        yield

def test_create_user(client):
    rv = client.post("/users", headers={"Authorization": f"Bearer {API_TOKEN}"}, json={"name":"A", "email":"a@e.com", "role":"admin"})
    assert rv.status_code == 201
    data = rv.get_json()
    assert "id" in data
    assert data["email"] == "a@e.com"

def test_list_users(client):
    # create two users
    client.post("/users", headers={"Authorization": f"Bearer {API_TOKEN}"}, json={"name":"A", "email":"a@e.com", "role":"admin"})
    client.post("/users", headers={"Authorization": f"Bearer {API_TOKEN}"}, json={"name":"B", "email":"b@e.com", "role":"user"})
    rv = client.get("/users", headers={"Authorization": f"Bearer {API_TOKEN}"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_get_user_not_found(client):
    rv = client.get("/users/nonexistent", headers={"Authorization": f"Bearer {API_TOKEN}"})
    assert rv.status_code == 404

def test_update_user(client):
    create = client.post("/users", headers={"Authorization": f"Bearer {API_TOKEN}"}, json={"name":"C", "email":"c@e.com", "role":"user"})
    uid = create.get_json()["id"]
    rv = client.put(f"/users/{uid}", headers={"Authorization": f"Bearer {API_TOKEN}"}, json={"role":"admin"})
    assert rv.status_code == 200
    assert rv.get_json()["role"] == "admin"

def test_delete_user(client):
    create = client.post("/users", headers={"Authorization": f"Bearer {API_TOKEN}"}, json={"name":"D", "email":"d@e.com", "role":"user"})
    uid = create.get_json()["id"]
    rv = client.delete(f"/users/{uid}", headers={"Authorization": f"Bearer {API_TOKEN}"})

    assert rv.status_code == 204
