from pymongo import MongoClient

# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient(port=27017)
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
