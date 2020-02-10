import game.opentdb as api
from random import shuffle
import json
import psycopg2

class PostgreHelp:
    def __init__(self):
        #self.redisClient = redis.Redis(host="127.0.0.1", port=6379)
         self.user= 'user'    
    '''
    def GetHashData(self, hashname, key):
        return self.redisClient.hget(hashname, key)
    '''
    def SetQuestion(self, groupname):
        question = ''
        answers= ''
        try:
            print ("here i am ")
            connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="trivia")
            cursor = connection.cursor()
            existingQuestion = "SELECT * FROM public.questions where groupname = '{}' ".format(groupname)
            cursor.execute(existingQuestion)
            connection.commit()

            difficulty ='easy'
            quesno = 0
            exist = False
            if cursor.rowcount >0:
                row = cursor.fetchone()
                quesno  = int(row[7])
                exist = True
            if quesno <= 10:
                difficulty ='easy'
            elif quesno > 10 and quesno < 20:
                difficulty ='medium'
            else:
                difficulty = 'hard'
            questionResult = api.GetQuestion(difficulty)
            result= questionResult['results'][0]
            question = result['question']
            correct_answer =result['correct_answer']
            answers =result['incorrect_answers']
            answers.append(correct_answer)
            shuffle(answers)
            quesno += 1

            if exist:
                #updateUserNO = "UPDATE questions SET  no={0}, correctanswer={1}, difficulty={2}, question={3}, answers={4} WHERE groupname= '{5}'"
                updateUserNO = "UPDATE questions SET  quesno={0}, correctanswer={1}, difficulty={2}, question={3}, answers={4} WHERE groupname= '{5}'"
                updateUserNO = updateUserNO.format(quesno,correct_answer,difficulty,question,answers,groupname)
                cursor.execute(updateUserNO)
                connection.commit()
            '''
            else:
                postgres_insert_query = "INSERT INTO public.questions(groupname, no, correctanswer, difficulty, question, answers) VALUES ( {0},{1},{2},{3},{4},{5}}"
                record_to_insert = (groupname,no,correct_answer,difficulty,question,answers)
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()
            '''
            print(quesno)
            print(question, answers)
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print(error)
        finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
        return (question, answers)
    
    def GetQuestion(self, groupname):
        connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="trivia")
        cursor = connection.cursor()
        existingQuestion = 'SELECT * FROM public.questions where groupname = %s '
        cursor.execute(existingQuestion,groupname)
        question =None
        answers = None
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            question  = int(row[5])
            answers  = int(row[6])
        return (question, answers)

    def GetUserCount(self, groupname, maxuser):
        connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="trivia")
        cursor = connection.cursor()
        existingQuestion = "SELECT * FROM public.questions where groupname = '{0}' ".format(groupname)
        cursor.execute(existingQuestion)  
        connection.commit()      
        users = 0
        #the group already contains the user
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            users  = int(row[2])
            #if there is still space for the user
            if(users < maxuser):
               users = self.UpdateUserCount( groupname, users)
            elif users > maxuser:                
                print('this user is late, in between somebody took that space')
        #this user is the first user.
        else:
            users = self.FirstUser(groupname)
            print('')

        return  users

    def UpdateUserCount(self, groupname, users):
        connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="trivia")
        users += 1
        updateUserCount = "UPDATE questions SET  userno={0}  WHERE groupname= '{1}'".format(users, groupname)
        cursor = connection.cursor()
        cursor.execute(updateUserCount)
        connection.commit()
        return users

    def FirstUser(self, groupname):
        connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="trivia")
        query_firstperson = "INSERT INTO public.questions(groupname, userno, correctanswer, difficulty, question,quesno) VALUES ( '{}',{},'{}','{}','{}',{})"
        query_firstperson = query_firstperson.format(groupname,1,'','easy','',0)
        cursor = connection.cursor()
        cursor.execute(query_firstperson)
        connection.commit()
        return 1