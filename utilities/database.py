import os
# from dotenv import load_dotenv
import certifi
from pymongo import MongoClient

# load_dotenv()

if os.environ["env"] == "production":
   use_database = "Lore"
else:
   use_database = "Lore"

mongo = MongoClient(os.environ["MONGO_KEY"], tlsCAFile=certifi.where())

db = mongo[use_database]

lore_collection = db["lore"]
characters_collection = db["characters"]
items_collection = db["items"]
locations_collection = db["locations"]

def get_lore():
   return lore_collection.find()

def get_lore_by_query(query):
   return lore_collection.find(query)

def save_lore(lore):
    try:
      lore_collection.insert_one(lore)
      return True
    except:
        return False

def get_characters():
    return characters_collection.find()

def get_characters_by_query(query):
    return characters_collection.find(query)

def save_character(character):
    try:
        characters_collection.insert_one(character)
        return True
    except:
        return False

def get_items():
    return items_collection.find()

def get_items_by_query(query):
    return items_collection.find(query)

def save_item(item):
    try:
        items_collection.insert_one(item)
        return True
    except:
        return False

def get_locations():
    return locations_collection.find()

def get_locations_by_query(query):
    return locations_collection.find(query)

def save_location(location):
    try:
        locations_collection.insert_one(location)
        return True
    except:
        return False
    