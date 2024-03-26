import os
import certifi
import pymongo
from dotenv import load_dotenv
import requests

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_KEY"], tlsCAFile=certifi.where())
db = client.Lore
collection = db.lore

def answer_question(question: str):
    hf_token = os.environ["HF_TOKEN"]
    embedding_url="https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

    def generate_embedding(text: str) -> list[float]:
        response = requests.post(embedding_url, headers={"Authorization": f"Bearer {hf_token}"}, json={"inputs": text})
        if response.status_code != 200:
            raise ValueError(f"Failed to generate embedding: {response.status_code} {response.text}")
        return response.json()

    query = question

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "plot_embedding_hf",
                "numCandidates": 100,
                "limit": 10,
                "index": "DndSemanticSearch",
            }
        }
    ])

    text = ""

    for document in results:
        text += f"{document['original_description']}\n"

    print("Completed vectorsearch.py function.")
    return text


def add_embedding(title):
    hf_token = os.environ["HF_TOKEN"]
    embedding_url="https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

    def generate_embedding(text: str) -> list[float]:
        response = requests.post(embedding_url, headers={"Authorization": f"Bearer {hf_token}"}, json={"inputs": text})
        if response.status_code != 200:
            raise ValueError(f"Failed to generate embedding: {response.status_code} {response.text}")
        return response.json()


    for doc in collection.find({'original_title': title}):
        doc['plot_embedding_hf'] = generate_embedding(doc['original_description'])
        collection.replace_one({'_id': doc['_id']}, doc)
        print("Document has been found and embedding has been added.")
