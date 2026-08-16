"""
AnimalShelter CRUD Class
CS 499 – Milestone Three: Algorithms and Data Structures
Student: Kiera Watts

This artifact comes from my earlier work with the AAC MongoDB database.
It originally handled basic CRUD operations for the 'animals' collection.

For Milestone Three, I enhanced the artifact by adding algorithmic logic:
- Optimized breed search using regex filtering
- Alphabetical sorting for faster lookup
- Efficiency improvements and cleaner structure
- Time complexity notes (Big O) to show algorithmic reasoning

These updates demonstrate my ability to design and evaluate computing
solutions using algorithmic principles, improve performance, and write
clear, professional code aligned with course outcome #3.
"""

import os
from pymongo import MongoClient

class AnimalShelter:
    """
    AnimalShelter class for handling CRUD operations on the AAC MongoDB database.
    This version is cleaned up, easier to read, and includes the enhancements
    I made for CS 499 (security, structure, and algorithmic improvements).
    """

    def __init__(self):
        """
        Connect to MongoDB using environment variables.
        This removes hardcoded credentials and is a basic security improvement.
        """

        username = os.getenv("AAC_USER")
        password = os.getenv("AAC_PASS")

        # Make sure the environment variables exist
        if not username or not password:
            raise ValueError("Missing AAC_USER or AAC_PASS environment variables.")

        try:
            # Connect to MongoDB
            self.client = MongoClient(
                f"mongodb://{username}:{password}@localhost:27017/?authSource=aac"
            )
            self.database = self.client["aac"]
            self.collection = self.database["animals"]

        except Exception as e:
            raise ConnectionError(f"Could not connect to MongoDB: {e}")

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def create(self, data):
        """
        Insert a new animal document.
        Basic validation and error handling included.
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

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------
    def read(self, query=None):
        """
        Read documents from the animals collection.
        If no query is given, return all documents.
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

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    def update(self, query, new_values):
        """
        Update documents that match the query.
        Returns how many documents were updated.
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

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete(self, query):
        """
        Delete documents that match the query.
        Returns how many documents were deleted.
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

    # ---------------------------------------------------------
    # ALGORITHMIC ENHANCEMENT (Milestone Three)
    # ---------------------------------------------------------
    def find_by_breed(self, breed):
        """
        Optimized breed search.
        - Uses regex for flexible matching (case-insensitive)
        - Sorts results alphabetically by name
        - Includes time complexity notes for CS 499

        Time Complexity:
        - Regex search: O(n)
        - Sorting: O(n log n)
        """

        if not breed:
            print("Breed search failed: breed cannot be empty.")
            return []

        try:
            cursor = (
                self.collection.find({"breed": {"$regex": breed, "$options": "i"}})
                .sort("name", 1)
            )
            return list(cursor)

        except Exception as e:
            print(f"Breed search error: {e}")
            return []
