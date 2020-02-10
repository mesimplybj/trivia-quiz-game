# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import psycopg2
from game.postgrehelper import PostgreHelp

class ChatConsumer(WebsocketConsumer):
    numberofuser = 3
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        #self.openstate = True
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        '''
        self.send(text_data=json.dumps({
                    'message': count
         }))
        async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': 'member added'
                    }
                )
        '''
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #message = text_data_json['message']
        state = text_data_json['state']
        if state =='connect':
            postgreHelp = PostgreHelp()
            count =  postgreHelp.GetUserCount('roomname_' + self.room_name,self.numberofuser)
            context = 'connection'
            # response to a  new connection with the number of users and
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'client_broadcast',
                    'message': count,
                    'context':context,
                    'numberofuser':self.numberofuser
                }
            )
            # if the group is full then start the quiz
            if count== self.numberofuser: # and self.openstate == True:
                context = 'startgame'    
                print(context)
                self.Question(context,'set')
                #self.openstate = False
            '''
            if self.openstate == False:
                context = 'runninggame'
                self.Question(context,'get')
            '''
        elif state == 'answer':
            answer = text_data_json['answer']
            self.send(text_data=json.dumps({
                                'message': answer
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
    
    def Question(self, context, status):        
        
        postgreHelp = PostgreHelp()
        groupName ='asgi::group:chat_' + self.room_name + '_ques'
        que = None
        if status =='set':
            que = postgreHelp.SetQuestion(groupName)
        else:
            que = postgreHelp.GetQuestion(groupName)
        if  que is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'client_broadcast_question',
                    'question': que[0],
                    'context':context,
                    'options':que[1]
                }
            )


    '''
    def broadcast(self, msg):
        self.send(text_data=json.dumps({
                'message': event['message'],
            }))
    '''
    def countdown(self ,t):
        while t:
            mins, secs = divmod(t, 60)      
            time.sleep(1)
            t -= 1