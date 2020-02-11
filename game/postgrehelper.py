"""
HQTrivia Databse class: PostgreHelp

This is the database layer. This layer is responsible for  the implementaion of
functions that  performs the CRUD operations and provides a implemetable layer to
the caller
"""
from .opentdb import OpenTbRequest as API
from random import shuffle
import json
import psycopg2
from collections import Counter
import os

class PostgreHelp:
    def __init__(self):
        #self.redisClient = redis.Redis(host="127.0.0.1", port=6379)
        self.user = 'user'
        self.connection = psycopg2.connect(user="postgres",
                                           password="admin",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="trivia")
        '''
        self.connection = psycopg2.connect(user="d78hmogumse5m9",
                                  password="2f55bd846a95842e210cc3ac1585d2254479ccd33219fc5615b23aa1de07feb9",
                                  host="ec2-184-72-236-57.compute-1.amazonaws.com",
                                  port="5432",
                                  database="d78hmogumse5m9")  
        '''
    def OldQuestion(self, groupname):
        """
        Gives the previous question's difficulty and question number.

        Args: 
            groupname (str): name of the group
        Returns:
            Tuple: question number , difficulty
        """
        cursor = self.connection.cursor()
        question = "SELECT *  FROM public.questions where groupname = '{}' ".format(
            groupname)
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

    # set the question needed to broadcast to the end users
    def SetQuestion(self, groupname, difficulty, exist):
        """
        Gives the previous question's difficulty and question number.

        Args: 
            groupname (str): name of the group
        Returns:
            Tuple: question number , difficulty
        """
        question = ''
        answers = ''
        quesno = 0
        try:
            cursor = self.connection.cursor()
            # get question from API
            api = API()
            questionResult = api.GetQuestion(difficulty)
            result = questionResult['results'][0]
            question = result['question']
            correct_answer = result['correct_answer']
            answers = result['incorrect_answers']
            # mixed and shuffle the options
            answers.append(correct_answer)
            shuffle(answers)
            quesno += 1

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
        return (question, answers, quesno)

    def GetQuestion(self, groupname):
        """
        Gives the previous question's difficulty and question number.

        Args: 
            groupname (str): name of the group
        Returns:
            Tuple: question number , difficulty
        """
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

    def GetUserCount(self, groupname, maxuser, username):
        """
        Gives the number of users associated with current group.
        This is called before the  room  has initiated the quiz.
        Args: 
            groupname (str): name of the group
            maxuser (str): maximum number of user that the group can hold
            username (str): name of the user
        Returns:
            totalusers(int): total number of user in the room
        """
        # the group already contains the user
        cursor = self.connection.cursor()
        existing_user = "SELECT Count(1) FROM public.answers where groupname = '{0}' ".format(
            groupname)
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
                self.AddUserToGroup(groupname, username, '')
                totalusers += 1
        elif totalusers == maxuser:
            totalusers += 1
        return totalusers

    def GetRemainingUserCount(self, groupname):
        """
        Gives the remaining number of user in the group

        Args: 
            groupname (str): name of the group
        Returns:
            totalusers(int):  remaining users
        """
        cursor = self.connection.cursor()
        existing_user = "SELECT Count(1) FROM public.answers where groupname = '{0}' and ans != '' ".format(
            groupname)
        cursor.execute(existing_user)
        self.connection.commit()
        row = cursor.fetchone()
        totalusers = int(row[0])
        return totalusers

    def UpdateUserCount(self, groupname, user):
        """
        Updates the user who is joining the group
        Args: 
            groupname (str): name of the group
            user (int): name of the group
        Returns:
            user(int): total new users
        """
        user += 1
        updateUserCount = "UPDATE questions SET  userno={0}  WHERE groupname= '{1}'".format(
            user, groupname)
        cursor = self.connection.cursor()
        cursor.execute(updateUserCount)
        self.connection.commit()
        return user

    def AddUserToGroup(self, groupname, username, ans):
        """
        initialize the connected user to group.
        Args: 
            groupname (str): name of the group
            username (str): name of the user
            ans (str): ans of the user
        """
        ans_query = "INSERT INTO public.answers( groupname, username, ans) VALUES ('{}', '{}', '{}')"
        ans_query = ans_query.format(groupname, username, ans)
        cursor = self.connection.cursor()
        cursor.execute(ans_query)
        self.connection.commit()

    def AnswerUpdate(self, groupname, username, ans):
        """
        Updates the ans of the question that the user choosed

        Args: 
            groupname (str): name of the group
            username (str): name of the user
            ans (str): ans of the user
        """
        ans_query = "Update answers set ans = '{}' where groupname='{}' and  username='{}'"
        ans_query = ans_query.format(ans, groupname, username)
        cursor = self.connection.cursor()
        cursor.execute(ans_query)
        self.connection.commit()

    def GetCorrectAnswer(self, groupname):
        """
        Only current question is saved in the database.
        You can get the current question's correct answer calling this function

        Args: 
            groupname (str): name of the group
        Returns:
            answers:  correct answer of the group
        """
        cursor = self.connection.cursor()
        existingQuestion = "SELECT correctanswer FROM public.questions where groupname = '{}'".format(
            groupname)
        cursor.execute(existingQuestion)
        self.connection.commit()
        answers = None
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            answers = row[0]
        return answers

    def GetGroupAnswer(self, groupname):
        """
        Returns the ans given by all the users to provide the statistics

        Args: 
            groupname (str): name of the group
        Returns:
            Tuple: answers wth ther status, correct answer
        """
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
        return (ans_stat.most_common(5), correct_answer)

    def DeleteCurrentAns(self, groupname, answer):
        """
        Deletes the user that has given the wrong answer
        Users with  empty answers will be deleted later
        Args: 
            groupname (str): name of the group
            groupname (str): correct answer of the group's current session
        """
        ans_query = "Update answers set ans = '' where groupname='{}' and ans != '{}'"
        ans_query = ans_query.format(groupname, answer)
        cursor = self.connection.cursor()
        cursor.execute(ans_query)
        self.connection.commit()

    def EmptyRoom(self, groupname):
        """
        After succesfull game play empty the room.

        Args: 
            groupname (str): name of the group
        """
        remove_user = "Delete from answers where groupname='{}'"
        remove_user = remove_user.format(groupname)
        cursor = self.connection.cursor()
        cursor.execute(remove_user)
        self.connection.commit()

        remove_question = "Delete from questions where groupname='{}'"
        remove_question = remove_question.format(groupname)
        cursor = self.connection.cursor()
        cursor.execute(remove_question)
        self.connection.commit()

    def RemoveUser(self, groupname, username):
        """
        Removes the user in the certain group

        Args: 
            groupname (str): name of the group
            username (str): name of the user
        """
        remove_user = "Delete from answers where groupname='{}' and username = '{}'"
        remove_user = remove_user.format(groupname, username)
        cursor = self.connection.cursor()
        cursor.execute(remove_user)
        self.connection.commit()

    def TruncateTables(self):
        """
        Truncates all the tables 
        This function is applicable to call at project iniitiation
        """
        cursor = self.connection.cursor()
        truncatequestions = "truncate table questions"
        cursor.execute(truncatequestions)
        self.connection.commit()
        truncatequestions = "truncate table answers"
        cursor.execute(truncatequestions)
        self.connection.commit()
