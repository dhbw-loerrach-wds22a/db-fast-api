import json

from pymongo import MongoClient
import mysql.connector
import redis
REDIS_CACHE_TIME = None # seconds
def get_mongo_db():
    client = MongoClient('mongodb', 27017)
    db = client.yelp_data
    return db


def get_mysql_connection():
    connection = mysql.connector.connect(
        host='mysql',
        user='root',
        password='mypassword',
        database='yelp_data'
    )
    return connection


def get_redis_connection():
    r = redis.Redis(host='redis', port=6379, db=0)
    return r


