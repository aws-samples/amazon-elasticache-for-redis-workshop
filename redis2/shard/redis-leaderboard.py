from rediscluster import RedisCluster
from random import randint
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)

#1-1. connect
redis = RedisCluster(startup_nodes=[{"host": "[Your Redis Cluster Endpoint]","port": "6379"}], decode_responses=True,skip_full_coverage_check=True, socket_timeout=2, retry_on_timeout=True)

#1-2. connection check
if redis.ping():
    logging.info("Connected to Redis")


#2-1. create 50 leaderboards, 100 users and scores
for i in range(50):
    key='leaderboard'+str(i+1)
    redis.zadd(key, {'gamer'+str(j+1):0 for j in range(100)})


#3-1. game proceeds for continuous iteration
while True:
    try:
        #4-1. select random leaderboard and update score
        cur=randint(1,50)
        key='leaderboard'+str(cur)
        redis.zadd(key, {'gamer'+str(randint(1,100)):randint(0,1000) for x in range(10)})

        #4-2. put top 10 players in the list
        leaderboard = redis.zrevrange(key, 0, 9, withscores=True)

        #4-3. print leaderboard of top 10 players
        #leaderboard title
        print('{0:*^64}'.format('TOP 10 PLAYERS!! ('+key+')'))
        #leaderboard subtitle
        print('{0:^20} {1:^20} {2:^20}'.format('RANK', 'ID', 'SCORE'))
        #leaderboard content
        print('===============================================================')
        for j in range(10):
            print('{0:^20}|{1:^20}|{2:^20}'.format((j+1),leaderboard[j][0], leaderboard[j][1]))

        time.sleep(0.5);
        print('===============================================================')
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass