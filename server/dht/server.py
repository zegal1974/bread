import asyncio
import logging

import redis
from kademlia.network import Server

from dht import config


class Server:
    def __init__(self):
        self.log = get_logger()
        self.redis = get_redis()


def get_logger():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger(config.DHT_SERVER_LOGGER)
    log.setLevel(config.DHT_SERVER_LOGGER_LEVEL)
    log.addHandler(handler)
    return log


def get_redis():
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
    if not r.ping():
        print("Failed to connect to Redis server.")
    else:
        print("Connected to Redis server.")
    return r


async def run():
    # Create a node and start listening on port 5678
    node = Server()
    await node.listen(config.DHT_SERVER_PORT)

    # Bootstrap the node by connecting to other known nodes, in this case
    # replace 123.123.123.123 with the IP of another node and optionally
    # give as many ip/port combos as you can for other nodes.
    await node.bootstrap([("123.123.123.123", config.DHT_SERVER_PORT)])

    # set a value for the key "my-key" on the network
    await node.set("my-key", config.DHT_SERVER_APIKEY)

    # get the value associated with "my-key" from the network
    result = await node.get("my-key")
    print(result)


asyncio.run(run())
