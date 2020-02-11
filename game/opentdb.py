import requests
from random import randint
import json


class OpenTbRequest:
    """
    Class that 
    """
    def GetQuestions(self,difficulty):
        """
        Returns question along with right and wrong answers from open trivia database.

        Args: 
           difficulty (str): The difficulty of the question to be set
        Raises:
            RuntimeError: Out of fuel
        Returns:
            jsom: json containing the question and  answers

        """
        category = str(randint(9, 32))
        url = 'https://opentdb.com/api.php?'
        url += 'amount=1'
        url += '&category='+category
        url += '&difficulty='+difficulty
        url += '&type=multiple'
        #url+= '&encode=base64'
        # print(url)
        resp = requests.get(url)
        if resp.status_code != 200:
            # This means something went wrong.
            print('error')
            return None   
        return resp.json()

    def GetQuestion(self, difficulty):
        """
        Test question
        """
        return {
            "results": [{
                "question": " Who is the first prime minister of nepal ?",
                "correct_answer": "Bhimsen thapa",
                "incorrect_answers": ['asdfasdf', 'xyzasdfasdf', 'pqrsdfasd']
            }]
        }
        
