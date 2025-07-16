from flask import current_app
from pymongo import MongoClient
from datetime import datetime



def get_collection():
    client = MongoClient(current_app.config['MONGO_URI'])
    db = client.get_default_database()
    return db.urls

def insert_url(original_url, short_code):
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    result = get_collection().insert_one({
        "url": original_url,
        "shortCode": short_code,
        "accessCount": 0,
        "createdAt": now,
        "updatedAt": now
    })
    return result.inserted_id

def find_by_short_code(short_code):
    collection = get_collection()
    return collection.find_one({"shortCode": short_code})

def increment_access(short_code):
    collection = get_collection()
    collection.update_one(
        {"shortCode": short_code},
        {
            "$inc": {"accessCount": 1},
            "$set": {"updatedAt": datetime.utcnow().replace(microsecond=0).isoformat() + "Z"}
        }
    )

def update_url(short_code, new_url):
    updated_at = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    result = get_collection().find_one_and_update(
        {"shortCode": short_code},
        {
            "$set": {
                "url": new_url,
                "updatedAt": updated_at
            }
        },
        return_document=True
    )
    return result

def delete_url(short_code):
    collection = get_collection()
    result = collection.delete_one({"shortCode": short_code})
    return result.deleted_count > 0

