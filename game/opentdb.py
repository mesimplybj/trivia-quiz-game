import requests
from random import randint
def GetQuestion(difficulty):
    category = str(randint(9, 32))
    url = 'https://opentdb.com/api.php?'
    url+= 'amount=1'
    url+= '&category='+category
    url+= '&difficulty='+difficulty
    url+= '&type=multiple'
    #url+= '&encode=base64'
    #print(url)
    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        print('error')
        return None
    #print(resp.json())

    print("question being asked")
    return resp.json()