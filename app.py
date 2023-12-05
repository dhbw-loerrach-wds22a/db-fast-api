import json

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import time

from db import *
from util import *
from controller import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/reviews/{business_id}")
async def get_reviews(business_id: str):
    start_time = time.time()  # Zeitmessung starten
    update_and_check_reviews_rating(business_id)
    redis_con = get_redis_connection()
    value = redis_con.get(business_id)

    end_time = time.time()  # Zeitmessung beenden
    execution_time = end_time - start_time  # Berechnung der Ausführungszeit
    print(f"Ausführungszeit(after redis.get): {execution_time} Sekunden")
    if value is not None:
        return json.loads(value)
    db = get_mongo_db()
    reviews = db.reviews.find({"business_id": business_id}, {"_id": 0})
    ret_reviews = list(reviews)
    end_time = time.time()  # Zeitmessung beenden
    execution_time = end_time - start_time  # Berechnung der Ausführungszeit
    print(f"Ausführungszeit(after for loop): {execution_time} Sekunden")
    redis_con.set(business_id, json.dumps(ret_reviews), ex=REDIS_CACHE_TIME)
    redis_con.close()
    return ret_reviews


@app.get("/business/{name}")
async def get_business(name: str):
    redis_con = get_redis_connection()
    value = redis_con.get(name)
    if value is not None:
        return json.loads(value)
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM business WHERE name = %s", (name,))
    businesses = cursor.fetchall()
    cursor.close()
    connection.close()
    redis_con.set(name, json.dumps(businesses), ex=REDIS_CACHE_TIME)
    return businesses

@app.get("/business_id/{business_id}")
async def get_business_by_id(business_id: str):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM business WHERE business_id = %s", (business_id,))
    business = cursor.fetchone()
    cursor.close()
    connection.close()
    return business


class ReviewDocument(BaseModel):
    business_id: str = Field(..., description="The ID of the business being reviewed", example="abc123")
    review_id: str = Field(None, description="The ID of the review")
    user_id: str = Field(None, description="The ID of the user who wrote the review")
    stars: float = Field(..., description="The star rating of the review", example=4.5)
    useful: int = Field(None, description="The number of users who found the review useful")
    funny: int = Field(None, description="The number of users who found the review funny")
    cool: int = Field(None, description="The number of users who found the review cool")
    text: str = Field(..., description="The review text", example="This is a great place!")
    date: str = Field(None, description="The Date", example="This is a great place!")


@app.post("/review/add")
async def add_review_to_redis(review: ReviewDocument):
    review.review_id = generate_random_sequence()
    review.user_id = "augmented"
    review.useful = 0
    review.funny = 0
    review.cool = 0
    review.date = get_today()
    db = get_mongo_db()
    db.reviews.insert_one(review.dict())
    update_review_cache(review.business_id)
    update_and_check_reviews_rating(review.business_id)
    return ({"message": "Review added to MongoDB", "review_id": review.review_id})

@app.get("/review/del/{review_id}")
async def del_review(review_id: str):
    filter_query = {"review_id": review_id}
    db = get_mongo_db()
    cursor = db.reviews.find(filter_query)
    business_ids_to_delete = [doc["business_id"] for doc in cursor]
    result = db.reviews.delete_many(filter_query)
    for business_id in business_ids_to_delete:
        update_review_cache(business_id)
        update_and_check_reviews_rating(business_id)
    return {"message": "Review deleted to Redis", "review_id": review_id}


@app.get("/review/del-augmented")
async def delete_augmented():
    filter_query = {"user_id": "augmented"}
    db = get_mongo_db()
    cursor = db.reviews.find(filter_query)
    business_ids_to_delete = [doc["business_id"] for doc in cursor]
    result = db.reviews.delete_many(filter_query)
    for business_id in business_ids_to_delete:
        update_and_check_reviews_rating(business_id)
        update_review_cache(business_id)
    # Check the result and return a message
    if result.deleted_count > 0:
        return {"message": f"{result.deleted_count} documents deleted"}
    else:
        return {"message": "No documents matching the filter"}

