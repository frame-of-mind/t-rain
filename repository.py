from pymongo import MongoClient

from settings import mongo_db_name, mongo_host, mongo_password, mongo_port, mongo_username

# Connect to the MongoDB, change the connection string per your MongoDB environment
# client = MongoClient(port=27017)
# db_name = 'train_mongo'
client = MongoClient(
    'mongodb://%s:%s@%s:%s/%s' % (mongo_username, mongo_password, mongo_host, mongo_port, mongo_db_name),
    retryWrites=False)
# Set the db object to point to the business database
db = client.train_mongo
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
