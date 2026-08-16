import os
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter:
    """
    CRUD operations for the AAC animals collection in MongoDB.
    Enhanced for CS 499 Milestone Two:
    - Environment variable credentials
    - Input validation
    - Error handling
    - Cleaner structure
    - Security‑minded checks
    """

    def __init__(self):
        """
        Initialize the MongoDB connection using environment variables.
        This removes hardcoded credentials and improves security.
        """

        username = os.getenv("AAC_USER")
        password = os.getenv("AAC_PASS")

        if not username or not password:
            raise ValueError("Missing AAC_USER or AAC_PASS environment variables.")

        try:
            self.client = MongoClient(
                f"mongodb://{username}:{password}@localhost:27017/?authSource=aac"
            )
            self.database = self.client["aac"]
            self.collection = self.database["animals"]
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    # -----------------------------
    # CREATE
    # -----------------------------
    def create(self, data):
        """
        Insert a document into the animals collection.
        Includes validation and error handling.
        """

        if not isinstance(data, dict):
            print("Create failed: data must be a dictionary.")
            return False

        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Create error: {e}")
            return False

    # -----------------------------
    # READ
    # -----------------------------
    def read(self, query=None):
        """
        Query documents from the animals collection.
        Returns a list of documents.
        """

        if query is not None and not isinstance(query, dict):
            print("Read failed: query must be a dictionary.")
            return []

        try:
            cursor = self.collection.find(query or {})
            return list(cursor)
        except Exception as e:
            print(f"Read error: {e}")
            return []

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(self, query, new_values):
        """
        Update documents in the animals collection.
        Returns number of modified documents.
        """

        if not isinstance(query, dict) or not isinstance(new_values, dict):
            print("Update failed: query and new_values must be dictionaries.")
            return 0

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except Exception as e:
            print(f"Update error: {e}")
            return 0

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete(self, query):
        """
        Delete documents from the animals collection.
        Returns number of deleted documents.
        """

        if not isinstance(query, dict):
            print("Delete failed: query must be a dictionary.")
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Delete error: {e}")
            return 0
