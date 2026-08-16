# Example Python Code to Insert a Document 
from pymongo import MongoClient 
from bson.objectid import ObjectId 
class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 
    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username 
        PASS = password
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient("mongodb://localhost:27017")
        self.database = self.client[DB]
        self.collection = self.database[COL]
 
    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """Insert a document into the animals collection."""
        if data is not None: 
            try: 
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(e)
                return False
        else: 
            return False
           
    # Create method to implement the R in CRUD.
    
    def read(self, query):
        """Query documents from the animals collection."""
        results = []
        
        try:
            cursor = self.collection.find(query)
            for document in cursor:
                results.append(document)
        except Exception as e:
            print(e)
            
        return results
    
    def update(self, query, new_values):
        """Update documents in the animals collection."""
        if query and new_values:
            try:
                result = self.collection.update_many(
                    query,
                    {"$set": new_values}
                )
                return result.modified_count
            except Exception as e:
                print(e)
                return 0
        return 0
    
    def delete(self, query):
        """Delete documents from the animals collection."""
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(e)
                return 0
        return 0
