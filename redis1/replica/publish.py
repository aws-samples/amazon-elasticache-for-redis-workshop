from rediscluster import RedisCluster
from random import randint
import datetime
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)

#1-1. connect
redis = RedisCluster(startup_nodes=[{"host": "[Your Redis Cluster Endpoint]","port": "6379"}], decode_responses=True,skip_full_coverage_check=True, socket_timeout=2, retry_on_timeout=True)

#1-2. connection check
if redis.ping():
    logging.info("Connected to Redis")

#2-1. continuous publish
while True:
    try:
        now=datetime.datetime.now()
        msg = "Current time is : "+ str(now)
        redis.publish(channel="awsomechat",message=msg)
        time.sleep(1);

    except KeyboardInterrupt:
        sys.exit()
    except:
        try:
            time.sleep(1);
            redis = RedisCluster(startup_nodes=[{"host": "[Your Redis Cluster Endpoint]","port": "6379"}], decode_responses=True,skip_full_coverage_check=True, socket_timeout=2, retry_on_timeout=True)
        except KeyboardInterrupt:
            sys.exit()
        except:
            pass