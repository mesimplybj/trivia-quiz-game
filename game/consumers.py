# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import psycopg2
from .postgrehelper import PostgreHelp
import time
import asyncio
from . import scheduler
#Game consumer that implements the websockerconsumer
class GameConsumer(WebsocketConsumer):
    numberofuser = 3
    groups = ["broadcast"]
    def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    # Receive message from WebSockets
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        state = text_data_json['state']
        postgreHelp = PostgreHelp()
        if state == 'connect':
            username = text_data_json['username']
            #count the number of user in the group
            count = postgreHelp.GetUserCount(self.room_name, self.numberofuser, username)
            context = 'connection'
            if count <= self.numberofuser:
                # response to a  new connection with the number
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'client_broadcast',
                        'message': count,  
                        'context': context,
                        'numberofuser': self.numberofuser
                    }
                )
                # if the group is full then start the quiz
                if count == self.numberofuser:  # and self.openstate == True:
                    context = 'startgame'
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'client_broadcast_gamestarting',
                            'context': 'gamestarting'
                        }
                    )
                    scheduler.add_new_job(self,self.room_group_name, context)
            # no room for the new user
            
            else:
                self.send(text_data=json.dumps({
                    'context': 'rooomfull'
                }))
                #dicontinue from the  group pool
                async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name,
                    self.channel_name
                )
        elif state == 'answer':
            answer = text_data_json['answer']
            username = text_data_json['username']
            postgreHelp.AnswerUpdate(self.room_name, username, answer)
        '''
        elif state == 'disconnect':
            print('disconnect')
            username = text_data_json['username']
            postgreHelp.RemoveUser(self.room_name, username)
        '''

    def client_broadcast_gamestarting(self, event):
            # Send message to WebSocket
        self.send(text_data=json.dumps({
            'context': event['context']
    }))
    # Receive message from room group
    def client_broadcast(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'context': event['context'],
            'numberofuser': event['numberofuser']
        }))

    def client_broadcast_question(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'context': event['context'],
            'question': event['question'],
            'options': event['options']
        }))

    def client_broadcast_result(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'context': event['context'],
            'answer': event['answer'],
            'stat': event['stat']
    }))

    def client_broadcast_winner(self, event):
            # Send message to WebSocket
        self.send(text_data=json.dumps({
            'context': event['context']
    }))

    def Question(self, que,context):
        if que is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'client_broadcast_question',
                    'question': que[0],
                    'context': context,
                    'options': que[1]
                }
            )

    def check_score(self, roomname, context):
        # Receive message from room group
        postgreHelp = PostgreHelp()
        #check  for the old question's number aand difficulty
        questionNo, diffculty = postgreHelp.OldQuestion(self.room_name)
        # this is the first question so no need to broadcast previous ans statistics
        if(questionNo < 1):
            que = postgreHelp.SetQuestion(self.room_name,diffculty,False)
            self.Question(que,"startgame")
        else:
            stat, correct_answer = postgreHelp.GetGroupAnswer(self.room_name)
            #if correct_answer is not None and len(correct_answer) > 0:
            postgreHelp.DeleteCurrentAns(self.room_name,correct_answer)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                 {
                    'type': 'client_broadcast_result',
                    'answer': correct_answer,
                    'stat': stat,
                    'context': "result" 
                }
            )
            usercount = postgreHelp.GetRemainingUserCount(self.room_name)
            if usercount == 0:
                ##discontinue to broadcast
                postgreHelp.EmptyRoom(self.room_name)
                scheduler.stop(self.room_group_name)
                pass
            elif usercount == 1:
                # declare winner here
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                        {
                        'type': 'client_broadcast_winner',
                        'context': "winner" 
                    }
                )
                postgreHelp.EmptyRoom(self.room_name)
                scheduler.stop(self.room_group_name)
                pass
            else:
                time.sleep(5) 
                que = postgreHelp.SetQuestion(self.room_name,diffculty,True)
                self.Question(que,context)       
