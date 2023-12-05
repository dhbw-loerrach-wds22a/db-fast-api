import json

import pymongo

from db import *
from bson.son import SON

def update_review_cache(business_id: str):
    redis_con = get_redis_connection()
    value = redis_con.get(business_id)
    if value is None:
        return
    db = get_mongo_db()
    reviews = db.reviews.find({"business_id": business_id}, {"_id": 0})
    ret_reviews = list(reviews)
    redis_con.set(business_id, json.dumps(ret_reviews), ex=REDIS_CACHE_TIME)
    redis_con.close()


def update_and_check_reviews_rating(business_id: str):
    db = get_mongo_db()
    last_5_reviews = db.reviews.find({"business_id": business_id}, {"_id": 0}).sort("date", pymongo.DESCENDING).limit(5)
    # Extract the "stars" values into a list
    stars_list = [x['stars'] for x in last_5_reviews]

    # Calculate the average of the "stars" values
    if stars_list:
        avg_stars = sum(stars_list) / len(stars_list)
        print(f"Average Stars: {avg_stars}")
        if (avg_stars < 2):
            # Connect to Redis server
            redis_client = get_redis_connection()

            # Publish a message

            message = 'Your rating for the past 5 reviews fell bellow 2 (' + avg_stars + ')'
            redis_client.publish(business_id, message)
            print(f"[{business_id}]: {message}")
    else:
        print("No reviews found.")

