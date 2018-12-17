
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import redis


redis_host = "localhost"
redis_port = 6379
redis_password = ""


def hello_redis():
    try:
        r = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password)
        r.set("msg:hello", "Hello Redis!!!")
        msg = r.get("msg:hello")
        print(msg)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hello_redis()



