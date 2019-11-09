import re

from bson import ObjectId
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
logs = db.logs


def save_train(train):
    found_trains = get_trains(train['from'], train['to'], train['start'], train['arrive'])
    if len(found_trains) == 0:
        train['count'] = 1
        in_id = trains.insert_one(train).inserted_id
        train['_id'] = str(in_id)
        return train
    else:
        best_train = None
        for t in found_trains:
            if best_train is None or t['count'] > best_train['count']:
                best_train = t
        best_train['count'] += 1
        res = trains.update_one({'_id': ObjectId(best_train['_id'])}, {"$set": {'count': best_train['count']}})
        return best_train


def get_trains(from_station=None, to_station=None, starting_h=None, arriving_h=None):
    query = {}
    if from_station is not None:
        query['from'] = from_station
    if to_station is not None:
        query['to'] = to_station
    if starting_h is not None:
        # take only time
        time = starting_h.split()[-1]
        time = '.*'+re.escape(time)
        rgx = re.compile(time, re.IGNORECASE)  # compile the regex
        query['start'] = rgx
    if arriving_h is not None:
        # take only time
        time = arriving_h.split()[-1]
        time = '.*' +re.escape(time)
        rgx = re.compile(time, re.IGNORECASE)  # compile the regex
        query['arrive'] = rgx
    cursor = trains.find(query)
    result = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        result.append(document)
    return result


def get_train_by_id(id):
    train = trains.find_one({'_id': ObjectId(id)})
    return train


def save_log(log):
    res = logs.insert_one(log)
    return res


def get_logs():
    cursor = logs.find({})
    result = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        result.append(document)
    return result


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
