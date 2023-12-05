import redis

from db import *
def message_handler(message):
    print(f"Received: {message['data']}")

# Connect to Redis server
redis_client = get_redis_connection()

# Subscribe to the channel
channel = 'test_channel'
pubsub = redis_client.pubsub()
pubsub.subscribe(**{channel: message_handler})

print(f"Subscribed to {channel}")

# Listen for messages
pubsub.run_in_thread(sleep_time=0.001)
