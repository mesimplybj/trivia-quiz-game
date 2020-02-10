from .opentdb import OpenTbRequest as API
from random import shuffle
import json
import psycopg2
from collections import Counter

class PostgreHelp:
    def __init__(self):
        #self.redisClient = redis.Redis(host="127.0.0.1", port=6379)
        self.user = 'user'
        '''
        self.connection = psycopg2.connect(user="postgres",
                                           password="admin",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="trivia")
        '''
        self.connection = psycopg2.connect(user="fmhwoxcvqiwsyq",
                                  password="a9e68ce1d86a8bb10a9ce15d10df57fb3a3351ce0a5d4241535ca8687f200d8b",
                                  host="ec2-184-72-236-57.compute-1.amazonaws.com",
                                  port="5432",
                                  database="d78hmogumse5m9")  
        
    #return the previous question's difficulty and question number.
    def OldQuestion(self, groupname):
        cursor = self.connection.cursor()
        question = "SELECT *  FROM public.questions where groupname = '{}' ".format(groupname)
        cursor.execute(question)
        self.connection.commit()
        difficulty = 'easy'
        quesno = 0
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            quesno = int(row[7])
        if quesno <= 10:
            difficulty = 'easy'
        elif quesno > 10 and quesno < 20:
            difficulty = 'medium'
        else:
            difficulty = 'hard'
        return (quesno, difficulty)

    #set the question needed to broadcast to the end users
    def SetQuestion(self, groupname, difficulty,exist):
        question = ''
        answers = ''
        quesno=0
        try:
            ##get question from API
            api = API()
            questionResult = api.GetQuestion(difficulty)
            result = questionResult['results'][0]
            question = result['question']
            correct_answer = result['correct_answer']
            answers = result['incorrect_answers']
            #mixed and shuffle the options
            answers.append(correct_answer)
            shuffle(answers)
            quesno += 1
            
            cursor = self.connection.cursor()
            if exist == True:
                #updateUserNO = "UPDATE questions SET  quesno=%s, correctanswer=%s, difficulty=%s, question=%s, answers=%s WHERE groupname= %s"
                #updateUserNO = (quesno,correct_answer,difficulty,question,answers,groupname)
                updateQuestionNo = "UPDATE questions SET  quesno=%s, correctanswer=%s, difficulty=%s, question=%s, answers=%s WHERE groupname= %s"
                ans = (quesno, correct_answer, difficulty,
                       question, '{}', groupname)
                cursor.execute(updateQuestionNo, ans)
                self.connection.commit()
            else:
                question_insert = "INSERT INTO public.questions(groupname, userno, correctanswer, difficulty, question,quesno) VALUES ( '{}',{},'{}','{}','{}',{})"
                question_insert = question_insert.format(
                    groupname, quesno, correct_answer, difficulty, question, 1)
                cursor.execute(question_insert)
                self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print(error)
        finally:
            # closing database connection.
            if(self.connection):
                cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")
        return (question, answers,quesno)

    def GetQuestion(self, groupname):
        cursor = self.connection.cursor()
        existingQuestion = 'SELECT * FROM public.questions where groupname = %s '
        cursor.execute(existingQuestion, groupname)
        self.connection.commit()
        question = None
        answers = None
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            question = int(row[5])
            answers = int(row[6])
        return (question, answers)

    #returns the number of users associated with current group.
    #this is called before the  room  has initiated the quiz
    def GetUserCount(self, groupname, maxuser, username):
        # the group already contains the user
        cursor = self.connection.cursor()
        existing_user = "SELECT Count(1) FROM public.answers where groupname = '{0}' ".format(groupname)
        cursor.execute(existing_user)
        self.connection.commit()
        row = cursor.fetchone()
        totalusers = int(row[0])
        if(totalusers < maxuser):
            cursor = self.connection.cursor()
            existing_user = "SELECT Count(1) FROM public.answers where groupname = '{0}' and username= '{1}' ".format(
                groupname, username)
            cursor.execute(existing_user)
            self.connection.commit()
            row = cursor.fetchone()
            currentUser = int(row[0])
            if currentUser == 0:
                self.ConnectionAdd(groupname, username, '')
                totalusers += 1
        elif totalusers == maxuser:
            totalusers += 1
        return totalusers
    
    #returns the number of users associated with current group that are answering.
    #this is checked before the result is sent the  room  has initiated the quiz
    def GetRemainingUserCount(self, groupname):
        cursor = self.connection.cursor()
        existing_user = "SELECT Count(1) FROM public.answers where groupname = '{0}' and ans != '' ".format(groupname)
        cursor.execute(existing_user)
        self.connection.commit()
        row = cursor.fetchone()
        totalusers = int(row[0])
        return totalusers

    
    def UpdateUserCount(self, groupname, users):
        users += 1
        updateUserCount = "UPDATE questions SET  userno={0}  WHERE groupname= '{1}'".format(
            users, groupname)
        cursor = self.connection.cursor()
        cursor.execute(updateUserCount)
        self.connection.commit()
        return users

    def ConnectionAdd(self, groupname, username, ans):
        ans_query = "INSERT INTO public.answers( groupname, username, ans) VALUES ('{}', '{}', '{}')"
        ans_query = ans_query.format(groupname, username, ans)
        cursor = self.connection.cursor()
        cursor.execute(ans_query)
        self.connection.commit()

    def AnswerUpdate(self, groupname, username, ans):
        ans_query = "Update answers set ans = '{}' where groupname='{}' and  username='{}'"
        ans_query = ans_query.format(ans, groupname, username)
        cursor = self.connection.cursor()
        cursor.execute(ans_query)
        self.connection.commit()

    def GetCorrectAnswer(self, groupname):
        cursor = self.connection.cursor()
        existingQuestion = "SELECT correctanswer FROM public.questions where groupname = '{}'".format(groupname)
        cursor.execute(existingQuestion)
        self.connection.commit()
        answers = None
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            answers = row[0]
        return answers 

    def GetGroupAnswer(self, groupname):
        correct_answer = self.GetCorrectAnswer(groupname) 
        cursor = self.connection.cursor()
        existingQuestion = "SELECT * FROM answers where groupname = '{}'".format(
            groupname)
        cursor.execute(existingQuestion)
        self.connection.commit()
        ans_result = []
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            for row in rows:
                answers = row[3] 
                ans_result.append(answers)
        ans_stat = Counter(ans_result) 
        return  (ans_stat.most_common(5), correct_answer)

    def DeleteCurrentAns(self, groupname,answer):
        ans_query = "Update answers set ans = '' where groupname='{}' and ans != '{}'"
        ans_query = ans_query.format(groupname,answer)
        cursor = self.connection.cursor()
        cursor.execute(ans_query)
        self.connection.commit()         

    def TruncateTables(self): 
        cursor = self.connection.cursor()
        truncatequestions = "truncate table questions"
        cursor.execute(truncatequestions)
        self.connection.commit()
        truncatequestions = "truncate table answers"
        cursor.execute(truncatequestions) 
        self.connection.commit()