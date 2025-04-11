import settings
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from logger import Logger
import constants

DB_URL = f"mongodb+srv://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@patientpal.awkaqvw.mongodb.net/?retryWrites=true&w=majority&appName={constants.DB_NAME}"
logger = Logger("MongoDB")

class MongoDBInterface:
    _instance = None  # Class-level variable to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        """Override __new__ to ensure only one instance is created."""
        if cls._instance is None:
            logger.debug("Creating a new instance of MongoDBInterface.")
            cls._instance = super(MongoDBInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the MongoDBInterface instance."""
        if not hasattr(self, "initialized"):  # Ensure __init__ runs only once
            logger.debug("Initializing MongoDBInterface singleton instance.")
            self.client = None
            self.db = None
            self.initialized = True  # Mark as initialized

    # Connect to the MongoDB database
    def connect(self):
        logger.debug("Checking existing connection to MongoDB...")
        if self.client is not None:
            logger.debug("Already connected to MongoDB.")
            return
        logger.debug("No existing connection found. Establishing a new connection...")
        # Attempt to connect to the MongoDB server
        try:
            logger.debug(f"Connecting to DB {constants.DB_NAME}...")
            self.client = MongoClient(DB_URL, serverSelectionTimeoutMS=120000, connectTimeoutMS=120000)
            self.db = self.client[constants.DB_NAME]
            logger.info(f"Successfully connected to {constants.DB_NAME} database.")
        except ConnectionFailure as e:
            logger.critical(f"Could not connect to MongoDB. Error: {e}")
            raise e

    # List all collections in the database
    def list_collections(self):
        def list_collections_action():
            logger.debug("Fetching all collections from the database.")
            return self.db.list_collection_names()
        return self.__perform_db_action(list_collections_action)

    # Add a document to a collection
    def add_document(self, collection_name, document):
        def add_document_action(collection_name, document):
            logger.debug(f"Adding document to collection {collection_name}: {document}")
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            logger.info(f"Document added with _id: {result.inserted_id}")
            return result.inserted_id
        return self.__perform_db_action(add_document_action, collection_name, document)

    # Add multiple documents to a collection
    def add_documents(self, collection_name, documents):
        def add_documents_action(collection_name, documents):
            logger.debug(f"Adding multiple documents to collection {collection_name}.")
            collection = self.db[collection_name]
            result = collection.insert_many(documents)
            logger.info(f"{len(result.inserted_ids)} documents added.")
            return result.inserted_ids
        return self.__perform_db_action(add_documents_action, collection_name, documents)

    # Get a document from a collection with an optional filter
    def get_document(self, collection_name, filter=None):
        def get_document_action(collection_name, filter):
            logger.debug(f"Fetching document from collection {collection_name} with filter {filter}.")
            collection = self.db[collection_name]
            result = collection.find_one(filter) if filter else collection.find_one()
            logger.info(f"Fetched document: {result}")
            return result
        return self.__perform_db_action(get_document_action, collection_name, filter)

    # Get multiple documents from a collection with an optional filter
    def get_documents(self, collection_name, filter=None):
        def get_documents_action(collection_name, filter):
            logger.debug(f"Fetching multiple documents from collection {collection_name} with filter {filter}.")
            collection = self.db[collection_name]
            result = collection.find(filter) if filter else collection.find()
            result_list = list(result)
            logger.info(f"Fetched documents: {result_list}")
            return  result_list # Convert the cursor to a list to return all documents
        return self.__perform_db_action(get_documents_action, collection_name, filter)

    # Update a single document in a collection with an optional filter and update parameters
    def update_document(self, collection_name, filter, update_data, upsert=False):
        def update_document_action(collection_name, filter, update_data, upsert):
            logger.debug(f"Updating document in collection {collection_name} with filter {filter} and update data {update_data}.")
            collection = self.db[collection_name]
            result = collection.update_one(filter, {'$set': update_data}, upsert=upsert)
            if result.matched_count > 0:
                logger.info(f"Document updated, matched {result.matched_count} document(s).")
            elif result.upserted_id:
                logger.info(f"Document inserted (upsert), new _id: {result.upserted_id}")
            else:
                logger.info("No matching document found.")
            return result
        return self.__perform_db_action(update_document_action, collection_name, filter, update_data, upsert)

    # Update multiple documents in a collection with an optional filter and update parameters
    def update_documents(self, collection_name, filter, update_data, upsert=False):
        def update_documents_action(collection_name, filter, update_data, upsert):
            logger.debug(f"Updating multiple documents in collection {collection_name} with filter {filter} and update data {update_data}.")
            collection = self.db[collection_name]
            result = collection.update_many(filter, {'$set': update_data}, upsert=upsert)
            logger.debug(f"Update result: Matched {result.matched_count}, Modified {result.modified_count}")
            logger.info(f"{result.modified_count} documents updated.")
            return result
        return self.__perform_db_action(update_documents_action, collection_name, filter, update_data, upsert)

    # Delete a single document from a collection with a filter
    def delete_document(self, collection_name, filter):
        def delete_document_action(collection_name, filter):
            logger.debug(f"Deleting document from collection {collection_name} with filter {filter}.")
            collection = self.db[collection_name]
            result = collection.delete_one(filter)
            if result.deleted_count > 0:
                logger.info(f"Document deleted, deleted {result.deleted_count} document(s).")
            else:
                logger.info("No matching document found.")
            return result
        return self.__perform_db_action(delete_document_action, collection_name, filter)

    # Delete multiple documents from a collection with a filter
    def delete_documents(self, collection_name, filter):
        def delete_documents_action(collection_name, filter):
            logger.debug(f"Deleting multiple documents from collection {collection_name} with filter {filter}.")
            collection = self.db[collection_name]
            result = collection.delete_many(filter)
            if result.deleted_count > 0:
                logger.info(f"{result.deleted_count} documents deleted.")
            else:
                logger.info("No matching documents found.")
            return result
        return self.__perform_db_action(delete_documents_action, collection_name, filter)

    # Perform the database action (invoking the provided action function)
    def __perform_db_action(self, action, *args):
        if self.db is not None:
            logger.debug(f"Executing database action with arguments: {args}")
            return action(*args)  # Pass the arguments to the action method
        else:
            logger.error("Database not connected")
            raise ConnectionFailure("Not connected to the database.")


"""        
# Block of code to test the above functions
import logging
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
    db_interface.delete_documents("users", delete_filter)
"""