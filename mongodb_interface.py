import settings
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

DB_NAME = "PatientPal"
DB_URL = f"mongodb+srv://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@patientpal.awkaqvw.mongodb.net/?retryWrites=true&w=majority&appName=PatientPal"

class MongoDBInterface:
    def __init__(self):
        self.client = None
        self.db = None

    # Connect to the MongoDB database
    def connect(self):
        try:
            self.client = MongoClient(DB_URL)
            self.db = self.client[DB_NAME]
            print(f"Successfully connected to {DB_NAME} database.")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB. Error: {e}")
            raise

    # List all collections in the database
    def list_collections(self):
        if self.db is not None:
            return self.db.list_collection_names()
        else:
            raise ConnectionFailure("Not connected to the database.")

    # Add a document to a collection
    def add_document(self, collection_name, document):
        if self.db is not None:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            print(f"Document added with _id: {result.inserted_id}")
            return result.inserted_id
        else:
            raise ConnectionFailure("Not connected to the database.")
        
    # Add multiple documents to a collection
    def add_documents(self, collection_name, documents):
        if self.db is not None:
            collection = self.db[collection_name]
            result = collection.insert_many(documents)
            print(f"{len(result.inserted_ids)} documents added.")
            return result.inserted_ids
        else:
            raise ConnectionFailure("Not connected to the database.")

    # Get a document from a collection with an optional filter
    def get_document(self, collection_name, filter=None):
        if self.db is not None:
            collection = self.db[collection_name]
            if filter:
                result = collection.find_one(filter)
            else:
                result = collection.find_one()
            return result
        else:
            raise ConnectionFailure("Not connected to the database.")
        
    # Get multiple documents from a collection with an optional filter
    def get_documents(self, collection_name, filter=None):
        if self.db is not None:
            collection = self.db[collection_name]
            if filter:
                result = collection.find(filter)
            else:
                result = collection.find()
            return list(result)  # Convert the cursor to a list to return all documents
        else:
            raise ConnectionFailure("Not connected to the database.")
        
    # Update a single document in a collection with an optional filter and update parameters
    def update_document(self, collection_name, filter, update_data, upsert=False):
        if self.db is not None:
            collection = self.db[collection_name]
            result = collection.update_one(filter, {'$set': update_data}, upsert=upsert)
            if result.matched_count > 0:
                print(f"Document updated, matched {result.matched_count} document(s).")
            elif result.upserted_id:
                print(f"Document inserted (upsert), new _id: {result.upserted_id}")
            else:
                print("No matching document found.")
            return result
        else:
            raise ConnectionFailure("Not connected to the database.")

    # Update multiple documents in a collection with an optional filter and update parameters
    def update_documents(self, collection_name, filter, update_data, upsert=False):
        # upsert parameter allows creating a new document if no matching document is found
        if self.db is not None:
            collection = self.db[collection_name]
            result = collection.update_many(filter, {'$set': update_data}, upsert=upsert)
            print(f"{result.modified_count} documents updated.")
            return result
        else:
            raise ConnectionFailure("Not connected to the database.")

    # Delete a single document from a collection with a filter
    def delete_document(self, collection_name, filter):
        if self.db is not None:
            collection = self.db[collection_name]
            result = collection.delete_one(filter)
            if result.deleted_count > 0:
                print(f"Document deleted, deleted {result.deleted_count} document(s).")
            else:
                print("No matching document found.")
            return result
        else:
            raise ConnectionFailure("Not connected to the database.")

    # Delete multiple documents from a collection with a filter
    def delete_documents(self, collection_name, filter):
        if self.db is not None:
            collection = self.db[collection_name]
            result = collection.delete_many(filter)
            if result.deleted_count > 0:
                print(f"{result.deleted_count} documents deleted.")
            else:
                print("No matching documents found.")
            return result
        else:
            raise ConnectionFailure("Not connected to the database.")
        
"""
Block of code to test the above functions
if __name__ == "__main__":
    db_interface = MongoDBInterface()
    db_interface.connect()

    # List collections in the database
    collections = db_interface.list_collections()
    print("Collections in the database:", collections)

    # Add a single document to a collection
    doc = {"name": "John Doe", "age": 30, "job": "Engineer"}
    inserted_id = db_interface.add_document("users", doc)

    # Add multiple documents to a collection
    docs = [
        {"name": "Jane Doe", "age": 25, "job": "Designer"},
        {"name": "Alice Smith", "age": 35, "job": "Developer"}
    ]
    inserted_ids = db_interface.add_documents("users", docs)

    # Get a document with an optional filter
    filter_criteria = {"name": "John Doe"}
    document = db_interface.get_document("users", filter_criteria)
    print("Document fetched:", document)

    # Update a document
    update_data = {"age": 31}
    update_filter = {"name": "John Doe"}
    db_interface.update_document("users", update_filter, update_data)

    # Update multiple documents
    update_data = {"age": 30}
    update_filter = {"age": {"$gt": 30}}  # Update users older than 30
    db_interface.update_documents("users", update_filter, update_data)

    # Delete a document
    delete_filter = {"name": "John Doe"}
    db_interface.delete_document("users", delete_filter)

    # Delete multiple documents
    delete_filter = {"age": {"$lt": 30}}  # Delete users younger than 30
    db_interface.delete_documents("users", delete_filter)"
"""