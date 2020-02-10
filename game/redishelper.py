import redis
import game.opentdb as api
from random import shuffle
import json

class RedisHelp:
    def __init__(self):
        #self.redisClient = redis.Redis(host="127.0.0.1", port=6379)
        self.redisClient = redis.Redis(host="redis-14423.c56.east-us.azure.cloud.redislabs.com", port=14423,password='JQYiJE2Qb2tpSXClKcL2IbkKlYbPKpE1' )
    def GetHashData(self, hashname, key):
        return self.redisClient.hget(hashname, key)
    def SetQuestion(self, hashname):
        difficulty ='easy'
        no = self.GetHashData(hashname,"no")
        if no is None:
            no = 0
        no = int(no)
        if no < 10:
            difficulty ='easy'
        elif no > 10 and no < 20:
            difficulty ='medium'
        else:
            difficulty = 'hard'

        questionResult = api.GetQuestion(difficulty)
        result= questionResult['results'][0]
        question = result['question']
        correct_answer =result['correct_answer']
        incorrect_answers =result['incorrect_answers']
        shuffle(incorrect_answers)
        incorrect_answers.append(correct_answer)
        no += 1
        self.redisClient.hset(hashname, "no", no)
        self.redisClient.hset(hashname, "correct_answer", correct_answer)
        self.redisClient.hset(hashname, "difficulty", result['difficulty'])
        self.redisClient.hset(hashname, "question", question)
        self.redisClient.hset(hashname, "answers", incorrect_answers)

        return (question, incorrect_answers)
    def GetQuestion(self, hashname):
        return  (self.redisClient.hget(hashname, "question"),self.redisClient.hget(hashname, "answers"))
'''
redisHelp = RedisHelp()
redishash ='asgi::group:game_one_ques'
question = redisHelp.SetQuestion(redishash)
#print(question)
print(redisHelp.GetHashData(redishash,"no"))
print(redisHelp.GetHashData(redishash,"ans"))
print(redisHelp.GetHashData(redishash,"difficulty"))
'''