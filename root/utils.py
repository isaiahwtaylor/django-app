import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firestore:

    def __init__(self, project_id : str):
        if len(firebase_admin._apps) < 1:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id,
            })

        self.db = firestore.client()

    def put(self, collection, doc, data, merge):
        doc_ref = self.db.collection(collection).document(doc)
        doc_ref.set(data, merge=merge)

    def get(self, collection, doc):
        doc_ref = self.db.collection(collection).document(doc)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print("document not found")
            return None

    def update(self, collection, doc, data):
        doc_ref = self.db.collection(collection).document(doc)
        doc_ref.update(data)

    def query(self, collection, key, value):
        return self.db.collection(collection).where(key, "==", value).stream()

# class Bucket:
#
#     def __init__(self):
#         pass
