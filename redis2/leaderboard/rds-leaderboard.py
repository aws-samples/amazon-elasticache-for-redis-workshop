import sys
import os
import pymysql
import base64
import requests
import time
from random import randint

#1-1. connect
#RDS Info
host = "[Your RDS Endpoint]"
port = 3306
username = "[Your Database User Name]"
database = "game"
password = "[Your Database Password]"

conn = pymysql.connect(host, username, password, database, port, use_unicode=True, charset='utf8')
cursor = conn.cursor()

truncate = "truncate leaderboard"
cursor.execute(truncate)


#2-1. create 100 users and scores
for i in range(100):
  player_id="gamer"+str(i+1)
  score=0
  create_user = "insert into leaderboard(player_id, score) values (\""+player_id+"\", "+str(score)+")"
  cursor.execute(create_user)
  conn.commit()

  
#3-1. game proceeds for n iteration
n = int(input('Total Iteration : '))
for i in range(n):

  
  #4-1. update score
  for users in range(10):
     player_id = 'gamer'+str(randint(1, 100))
     score = randint(0,1000)
     update_user = "update leaderboard set score = "+str(score)+" where player_id = \""+player_id+"\""
     cursor.execute(update_user)
     conn.commit()


  #4-2. put top 10 players in the list
  top10_user = "select * from leaderboard order by score desc limit 10"
  cursor.execute(top10_user)
  leaderboard = cursor.fetchall()


  #4-3. print leaderboard of top 10 players
  #leaderboard title
  print('{0:*^64}'.format('TOP 10 PLAYERS!!'))
  #leaderboard subtitle
  print('{0:^20} {1:^20} {2:^20}'.format('RANK', 'ID', 'SCORE'))
  #leaderboard content
  print('===============================================================')
  for j in range(10):
     print('{0:^20}|{1:^20}|{2:^20}'.format((j+1),leaderboard[j][0], leaderboard[j][1]))
  time.sleep(0.5);
  print('===============================================================')

cursor.close()
conn.commit()
