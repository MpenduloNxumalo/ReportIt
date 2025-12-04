import firebase_admin
from firebase_admin import credentials, firestore


class UserNetwork:
    _instance = None
    _db = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cred = credentials.Certificate("service_key.json")
            firebase_admin.initialize_app(cred)
            cls._db = firestore.client()
            cls._instance = super(UserNetwork, cls).__new__(cls)
        return cls._instance

    def get_db(self):
        return self._db