from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import redis



class GameConsumer(WebsocketConsumer):
    client = redis.Redis(host = "127.0.0.1", port = 6379)
    numberofuser = 3
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

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
                        'type': 'room_message',
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
        message = text_data_json['message']
        state = text_data_json['state']
        if state =='connected':
            count =  self.client.zcard('asgi::group:room_' + self.room_name)
            serverstate = 'open'
            context = 'connection'
            if count== self.numberofuser:
                serverstate = 'close'
                context = 'startgame'
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'client_broadcast',
                    'message': count,
                    'serverstate': serverstate,
                    'context':context,
                    'numberofuser':self.numberofuser
                }
            )
        elif state == 'update':
            willdolater=0       
   
    # Receive message from room group
    def client_broadcast(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'serverstate': event['serverstate'],
            'context': event['context'],
            'numberofuser': event['numberofuser']
        }))
    '''
    def broadcast(self, msg):
        self.send(text_data=json.dumps({
                'message': event['message'],
                'serverstate': event['serverstate']
            }))
    '''
    def countdown(self ,t):
        while t:
            mins, secs = divmod(t, 60)      
            time.sleep(1)
            t -= 1