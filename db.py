import json

from pymongo import MongoClient
import mysql.connector
import redis
REDIS_CACHE_TIME = 12000 # seconds
def get_mongo_db():
    client = MongoClient('localhost', 27017)
    db = client.yelp_data
    return db


def get_mysql_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mypassword',
        database='yelp_data'
    )
    return connection


def get_redis_connection():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r


