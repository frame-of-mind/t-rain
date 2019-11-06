from pymongo import MongoClient

from settings import MONGODB_URI

# Connect to the MongoDB, change the connection string per your MongoDB environment
# client = MongoClient(port=27017)
# db_name = 'train_mongo'
if MONGODB_URI is None:
    MONGODB_URI = 'mongodb://localhost:27017/train_mongo'

mongo_db_name = MONGODB_URI.split('/')[-1]

client = MongoClient(MONGODB_URI, retryWrites=False)
# Set the db object to point to the business database
db = client[mongo_db_name]
trains = db.trains


def insert(train):
    post_id = trains.insert_one(train).inserted_id
    print(post_id)
    return post_id


def get_all():
    cursor = trains.find({})
    result = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        result.append(document)
        print(document)
    return result
