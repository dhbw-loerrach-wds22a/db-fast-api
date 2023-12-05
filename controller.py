import pymongo

from db import *
from bson.son import SON

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


def update_and_check_reviews_rating(business_id: str):
    db = get_mongo_db()
    last_5_reviews = db.reviews.find({"business_id": business_id}).sort("date", pymongo.DESCENDING).limit(5)
    # Extract the "stars" values into a list
    stars_list = [x['stars'] for x in last_5_reviews]

    # Calculate the average of the "stars" values
    if stars_list:
        avg_stars = sum(stars_list) / len(stars_list)
        print(f"Average Stars: {avg_stars}")
        if (avg_stars < 2):
            print(f"NOTIFY HERE: {avg_stars}")
    else:
        print("No reviews found.")


async def startup_function():
    # db = get_mongo_db()
    # # Aggregation pipeline
    # pipeline = [
    #     {"$sort": SON([("date", -1)])},  # Sort by date in descending order
    #     {"$group": {
    #         "_id": "$business_id",  # Group by business_id
    #         "documents": {"$push": "$$ROOT"}  # Push all documents for each business_id
    #     }},
    #     {"$project": {
    #         "documents": {"$slice": ["$documents", 5]}  # Limit to latest 5 documents
    #     }}
    # ]
    # # Execute the aggregation query
    # latest_documents_per_business = list(db.reviews.aggregate(pipeline, allowDiskUse=True))
    # print(latest_documents_per_business)

    print("Running startup function")
    # Place your startup code here