# Business Reviews API
# See services repository for setup instructions
## Description
This FastAPI application provides an interface for managing and retrieving business reviews. It supports operations such as fetching reviews for a specific business, retrieving business details, adding new reviews, and deleting reviews.

## Features
- Fetch reviews by business ID
- Get business details by name or ID
- Add new reviews to the database
- Delete reviews by review ID or all augmented reviews

## Setup and Installation
- run the docker-compose.yml in the services repository
## API Endpoints

### Get Reviews
- `GET /reviews/{business_id}`: Fetch reviews for a given business.

### Get Business Details
- `GET /business/{name}`: Get business details by name.
- `GET /business_id/{business_id}`: Get business details by business ID.

### Manage Reviews
- `POST /review/add`: Add a new review.
- `GET /review/del/{review_id}`: Delete a review by its ID.
- `GET /review/del-augmented`: Delete all reviews added manually (marked with the user_id 'augmented').

### Run the pubsub_demo
- set the channel to the listening business_id: `channel = '_5k9hs8ae9S9Dj46EZrSAg'`
- run `python3 pubsub_demo.py`

## License
[MIT](LICENSE)


