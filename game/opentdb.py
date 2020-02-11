import requests
from random import randint
import json


class OpenTbRequest:
    """
    Class that uses the open trivia api and helps to return the question
    """
    def GetQuestion(self,difficulty):
        """
        Returns question along with right and wrong answers from open trivia database.
        Args: 
           difficulty (str): The difficulty of the question to be set
        Raises:
            RuntimeError: None
        Returns:
            json: json containing the question and  answers
        """
        category = str(randint(9, 32))
        url = 'https://opentdb.com/api.php?'
        url += 'amount=1'
        url += '&category='+category
        url += '&difficulty='+difficulty
        url += '&type=multiple'
        resp = requests.get(url)
        if resp.status_code != 200:
            # This means something went wrong.
            print('error')
            return None   
        return resp.json()