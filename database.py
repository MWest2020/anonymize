from pymongo import MongoClient
import logging

class EntityDatabase:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client["anonymization_db"]
        self.entities = self.db["entities"]

    def add_entity(self, text, entity_type, confidence):
        try:
            result = self.entities.insert_one({
                "text": text,
                "entity_type": entity_type,
                "confidence": confidence
            })
            logging.info(f"Added entity: {text} (ID: {result.inserted_id})")
            return result.inserted_id
        except Exception as e:
            logging.error(f"Error adding entity to database: {str(e)}")
            return None

    def get_entity(self, text):
        return self.entities.find_one({"text": text})

    def update_entity(self, text, new_data):
        try:
            result = self.entities.update_one({"text": text}, {"$set": new_data})
            if result.modified_count > 0:
                logging.info(f"Updated entity: {text}")
            return result.modified_count
        except Exception as e:
            logging.error(f"Error updating entity in database: {str(e)}")
            return 0

    def delete_entity(self, text):
        try:
            result = self.entities.delete_one({"text": text})
            if result.deleted_count > 0:
                logging.info(f"Deleted entity: {text}")
            return result.deleted_count
        except Exception as e:
            logging.error(f"Error deleting entity from database: {str(e)}")
            return 0

    def get_all_entities(self):
        return list(self.entities.find())

    def close(self):
        self.client.close()