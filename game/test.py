from postgrehelper import PostgreHelp


postgreHelp = PostgreHelp()

postgreHelp.GetUsers('sffffffffdassssssssssssss')





'''
import opentdb as api
questionResult = api.GetQuestion(difficulty)
'''



#redis is working
'''
from redishelper import RedisHelp

redisHelp = RedisHelp()
redishash ='asgi::group:game_one_ques'
question = redisHelp.SetQuestion(redishash)
print(question)
print(redisHelp.GetHashData(redishash,"no"))
print(redisHelp.GetHashData(redishash,"ans"))
print(redisHelp.GetHashData(redishash,"difficulty"))
'''