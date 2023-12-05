import pymongo

from db import *


def update_review_cache(business_id: str):
    redis_con = get_redis_connection()
    value = redis_con.get(business_id)
    if value is None:
        return
    db = get_mongo_db()
    reviews = db.reviews.find({"business_id": business_id})
    ret_reviews = []
    for review in reviews:
        review['_id'] = str(review['_id'])
        ret_reviews.append(review)
    redis_con.set(business_id, json.dumps(ret_reviews), ex=REDIS_CACHE_TIME)
    redis_con.close()


def update_recent_reviews_rating(business_id: str):
    redis_con = get_redis_connection()
    db = get_mongo_db()
    # Extract the "stars" values into a list
    stars_list = [x['stars'] for x in last_5_reviews]

    # Calculate the average of the "stars" values
    if stars_list:
        avg_stars = sum(stars_list) / len(stars_list)
        print(f"Average Stars: {avg_stars}")
    else:
        print("No reviews found.")