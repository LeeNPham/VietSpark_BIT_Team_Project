from google.cloud import firestore

class Firestore:
    """ Firestore Service """
    def __init__(self, credentials):
        if credentials:
            self.client = firestore.Client(credentials=credentials)
        else:
            self.client = firestore.Client()

    def collection(self, collection_name):
        """ Returns a reference to a Firestore collection """
        return self.client.collection(collection_name)

    def add_document(self, collection_name, data, doc_id=None):
        """ Add a new document to a collection. Use `doc_id` for a specific ID """
        if doc_id:
            doc_ref = self.client.collection(collection_name).document(doc_id)
            doc_ref.set(data)
        else:
            doc_ref = self.client.collection(collection_name).add(data)
        return doc_ref

    def get_document(self, collection_name, doc_id):
        """ Get a document by ID """
        doc_ref = self.client.collection(collection_name).document(doc_id)
        return doc_ref.get().to_dict()

    def update_document(self, collection_name, doc_id, data):
        """ Update fields of a document """
        doc_ref = self.client.collection(collection_name).document(doc_id)
        doc_ref.update(data)

    def delete_document(self, collection_name, doc_id):
        """ Delete a document """
        doc_ref = self.client.collection(collection_name).document(doc_id)
        doc_ref.delete()

    def get_all_documents(self, collection_name):
        """ Get all documents in a collection """
        docs = self.client.collection(collection_name).stream()
        return {doc.id: doc.to_dict() for doc in docs}

    def query_collection(self, collection_name, field, op, value):
        """ Query documents in a collection """
        docs = self.client.collection(collection_name).where(field, op, value).stream()
        return {doc.id: doc.to_dict() for doc in docs}


'''
# Initialize Firestore
firestore_service = Firestore(credentials=config["serviceAccount"])

# Add a document to a collection
firestore_service.add_document("users", {"name": "John", "age": 30})

# Get a document
user_data = firestore_service.get_document("users", "user_id_123")

# Update a document
firestore_service.update_document("users", "user_id_123", {"age": 31})

# Delete a document
firestore_service.delete_document("users", "user_id_123")

# Get all documents in a collection
all_users = firestore_service.get_all_documents("users")

# Query a collection
queried_users = firestore_service.query_collection("users", "age", ">=", 25)
'''