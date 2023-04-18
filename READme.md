# FastAPI Demo

## Install

`pip install fastapi`

To Run our WebServer: `pip install uvicorn`

## To Run

`uvicorn myapi:app --reload`

## Points

1. FASTAPI uses the JSON Data
2. FASTAPI generate documentation automatically on `/docs`. So we don't need any external API Testing tools like Postman we can directly execute from here.

## Use Redis

1. It can cache the data in-memory which reduces the server operation.
2. By default, data in Redis does not expire and remains in memory until it is explicitly deleted or overwritten.
3. Set the Redis TTL (Time to Live). Currently 1 Day i.e 86400 sec is set.
   `redis_client.set('mykey', 'myvalue')
redis_client.expire('mykey', 86400)`

## Install Redis

1. To Install: `https://redis.io/docs/getting-started/installation/install-redis-on-linux/`
2. Start the Redis server by running the redis-server command in your terminal.
3. Test the Redis server by running the redis-cli ping command. You should see a response of PONG if the server is running correctly.
4. Install the Redis Python client library using pip install redis command.
5. In your Python code, import the Redis library and create a Redis client instance using redis.Redis() function with the appropriate host, port, and database number arguments.
