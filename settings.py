import os

mongo_username = 'root'
mongo_password = 'r00tr00t'
mongo_host = 'ds241968.mlab.com'
mongo_port = '41968'
mongo_db_name = 'heroku_s34x7260'

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/train_mongo')
