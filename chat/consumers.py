"""
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))





    self.scope["url_route"]["kwargs"]["room_name"]
            Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
            Every consumer has a scope that contains information about its connection, including in particular any positional or keyword arguments from the URL route and the currently authenticated user if any.

    self.room_group_name = f"chat_{self.room_name}"
            Constructs a Channels group name directly from the user-specified room name, without any quoting or escaping.
            Group names may only contain alphanumerics, hyphens, underscores, or periods. Therefore this example code will fail on room names that have other characters.

    async_to_sync(self.channel_layer.group_add)(...)
            Joins a group.
            The async_to_sync(...) wrapper is required because ChatConsumer is a synchronous WebsocketConsumer but it is calling an asynchronous channel layer method. (All channel layer methods are asynchronous.)
            Group names are restricted to ASCII alphanumerics, hyphens, and periods only and are limited to a maximum length of 100 in the default backend. Since this code constructs a group name directly from the room name, it will fail if the room name contains any characters that aren’t valid in a group name or exceeds the length limit.

    self.accept()
            Accepts the WebSocket connection.
            If you do not call accept() within the connect() method then the connection will be rejected and closed. You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
            It is recommended that accept() be called as the last action in connect() if you choose to accept the connection.

    async_to_sync(self.channel_layer.group_discard)(...)
            Leaves a group.

    async_to_sync(self.channel_layer.group_send)
            Sends an event to a group.
            An event has a special 'type' key corresponding to the name of the method that should be invoked on consumers that receive the event. This translation is done by replacing . with _, thus in this example, chat.message calls the chat_message method.


"""

"""
self.scope in channels = request in django
ex of self.scope from any method in consumer
{
    'type': 'websocket', 
    'path': '/ws/chat/jwt/', 
    'raw_path': b'/ws/chat/jwt/', 
    'headers': [
        (b'host', b'127.0.0.1:8000'), 
        (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'), 
        (b'accept', b'*/*'), 
        (b'accept-language', b'en-US,en;q=0.5'), 
        (b'accept-encoding', b'gzip, deflate, br'), 
        (b'sec-websocket-version', b'13'), 
        (b'origin', b'http://127.0.0.1:8000'), 
        (b'sec-websocket-extensions', b'permessage-deflate'), 
        (b'sec-websocket-key', b'6Ys6/4vSXe2jLpDjQ37uxA=='), 
        (b'connection', b'keep-alive, Upgrade'), 
        (b'cookie', b'csrftoken=VN2FEDW0xGpeNusrg78aAlHCEhHtDHHw; pga4_session=f7239bde-9fe4-47d6-88fb-8bedc3a368e1!depgxy1tV4MWqsTMt57kn/dBjBo='), 
        (b'sec-fetch-dest', b'empty'), 
        (b'sec-fetch-mode', b'websocket'), 
        (b'sec-fetch-site', b'same-origin'), 
        (b'pragma', b'no-cache'), 
        (b'cache-control', b'no-cache'), 
        (b'upgrade', b'websocket')
    ], 'query_string': b'', 
    'client': [
        '127.0.0.1', 54324
    ], 'server': [
        '127.0.0.1', 8000
    ], 'subprotocols': [], 
    'asgi': {'version': '3.0'}, 
    'cookies': {'csrftoken': 'VN2FEDW0xGpeNusrg78aAlHCEhHtDHHw', 'pga4_session': 'f7239bde-9fe4-47d6-88fb-8bedc3a368e1!depgxy1tV4MWqsTMt57kn/dBjBo='}, 
    'session': <django.utils.functional.LazyObject object at 0x00000239B5553EE0>, 
    'user': <channels.auth.UserLazyObject object at 0x00000239B5553490>, 
    'path_remaining': '', 
    'url_route': {'args': (), 'kwargs': {'room_name': 'jwt'}}
}
scope['type'] ...etc

    Note:
        It's important to note that user data is available in the scope only if the connection has been authenticated and the user is logged in. 
        If the connection is anonymous or not authenticated, self.scope['user'] will be an instance of an anonymous user or None.

        Make sure that you've configured authentication properly in your Django Channels setup to ensure that user data is available in the scope. 
        This typically involves using the AuthMiddlewareStack in your Channels routing configuration and authenticating the connection using a valid authentication method, such as session authentication or token authentication.
"""
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import User
from chat.models import ChatRoom , ChatMessage , AudioVideo, VideoCall
from channels.db import database_sync_to_async
from django.core.serializers import serialize
from django.core.files.base import ContentFile
from io import BytesIO
from django.utils import timezone

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        self.user = self.scope["user"]
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        print('*'*50 , 'connecting call Successfully ', '*'*50)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            data = json.loads(text_data)
            print(data)
            
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            if data['action'] == 'videoCall':
                if data['type'] == 'initiate':
                    caller = json.dumps({"type":"initiate","caller":data['caller']})
                    await self.channel_layer.group_send(
                        self.room_group_name, 
                        {
                            "type": "chat.message", 
                            "message": caller, 
                        }
                    )
                elif data['type'] == 'offer':
                    offer = data['offer']
                    # Serialize offer data
                    serialized_offer = json.dumps(offer)
                    # print("offer++" , serialized_offer)
                    # Send offer to room group
                    await self.channel_layer.group_send(
                        self.room_group_name, 
                        {
                            "type": "chat.message", 
                            "message": serialized_offer,  # Pass serialized offer data as a message

                        }
                    )
                elif data['type'] == 'answer':
                    answer = data['answer']
                    # print("answer++",answer)
                    # Serialize answer data
                    serialized_answer = json.dumps(answer)
                    # Send answer to room group
                    await self.channel_layer.group_send(
                        self.room_group_name, 
                        {
                            "type": "chat.message", 
                            "message": serialized_answer,  # Pass serialized answer data as a message

                        }
                    )
                elif data['type'] == 'candidate':
                    candidate = data['candidate']
                    # print("candidate++",candidate)
                    # Send ice candidate to specific user
                    serialized_candidate = json.dumps({"candidate":candidate,"from":data['from']})
                    # Send candidate to room group
                    await self.channel_layer.group_send(
                        self.room_group_name, 
                        {
                            "type": "chat.message", 
                            "message": serialized_candidate,  # Pass serialized candidate data as a message

                        }
                    )
                elif data['type'] == 'close':
                    await self.close_call(self.room_name)
    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        # Send message to WebSocket
        if 'message' in  event:
            await self.send(text_data=json.dumps({"message": event["message"]}))
    
    @database_sync_to_async
    def close_call(self , room_name):
        room_ = ChatRoom.objects.get(name = room_name)
        VideoCall.objects.get(room = room_).delete()

class ChatConsumer(AsyncWebsocketConsumer):
    # channel_layer_alias = "echo_alias"
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        self.user = self.scope["user"]
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.make_msgs_read(room_name=self.room_name , message_sender=self.user)
        print('*'*50 , 'connecting chat Successfully ', '*'*50)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            data = json.loads(text_data)
            print(data)
            username = self.user.username
            
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            if data["action"] == 'createMsg':
                if data["message_type"] == 'text': 
                    message = data["message"]
                    
                    chat_msg = await self.create_message(username , self.room_name , message)
                    serialized_chat_msg = serialize('json', [chat_msg] , fields= ['user','content','timestamp'] , use_natural_foreign_keys=True , use_natural_primary_keys=True)
                    # Send message to room group
                    await self.channel_layer.group_send(
                        self.room_group_name, {"type": "chat.message", "message": serialized_chat_msg}
                    )
                else:
                    # Extract the base64-encoded ArrayBuffer data
                    base64_data = data['record']
                    # Convert the base64-encoded string to an ArrayBuffer
                    array_buffer = base64.b64decode(base64_data)
                    # create the record
                    chat_record = await self.create_voice(username , self.room_name , array_buffer)
                    serialized_chat_msg = serialize('json', [chat_record] , fields= ['user','file','timestamp'] , use_natural_foreign_keys=True , use_natural_primary_keys=True)
                    # Send message to room group
                    await self.channel_layer.group_send(
                        self.room_group_name, {"type": "chat.message", "message": serialized_chat_msg}
                    )
            elif data["action"] == 'deleteMsg':
                await self.delete_message(data["message_id"],data["message_type"])

    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        # Send message to WebSocket
        if 'message' in  event:
            await self.send(text_data=json.dumps({"message": event["message"]}))

    # create messages in database
    @database_sync_to_async
    def create_message(self , username , room_name , content):
        user_sender = User.objects.get(username=username)
        room = ChatRoom.objects.get(name = room_name)
        chat_msg = ChatMessage(user = user_sender , room = room , content = content)
        chat_msg.save()
        return chat_msg

    @database_sync_to_async
    def delete_message(self , id , type):
        try :
            if type == 'text':
                msg = ChatMessage.objects.get(id=id)
                msg.delete()
            else:
                voice = AudioVideo.objects.get(id=id)
                voice.delete()
            return "Deleted Successfully"
        except:
            return "Error occurred"
        
    #create voice in database
    @database_sync_to_async
    def create_voice(self, username , room_name ,binary_data):
        byte_data = bytes(binary_data)
        # Create a BytesIO object and write the byte data to it
        bytes_io = BytesIO()
        bytes_io.write(byte_data)

        # Create a ContentFile from the BytesIO object
        content_file = ContentFile(bytes_io.getvalue())
        # create record in database
        user_sender = User.objects.get(username=username)
        room = ChatRoom.objects.get(name = room_name)
        record_msg =  AudioVideo(user = user_sender , room = room )
        record_msg.file.save(f'{timezone.now()}_{user_sender.username}.wav', content_file)
        record_msg.save()
        return record_msg
    
    #make messages read when enter the channel
    @database_sync_to_async
    def make_msgs_read(self , room_name , message_sender):
        room_ = ChatRoom.objects.get(name = room_name)
        user = User.objects.get(username = message_sender)
        room_.chat_chatmessage_related.filter(read=False).exclude(user=user).update(read=True)
        room_.chat_audiovideo_related.filter(read=False).exclude(user=user).update(read=True)

    # def send_to_peer(self, data):
    #     # Forward message to remote peer
    #     self.send(text_data=json.dumps(data))

'''
- the receive() method handles incoming messages from the WebSocket and performs actions such as saving data and broadcasting messages, 
- the chat_message() method handles messages received from the room group and sends them back to the WebSocket clients. 
These methods work together to facilitate bidirectional communication between the server and the WebSocket clients.
'''
"""
Consumers do a couple of things in particular:

    Structure your code as a series of functions to be called whenever an event happens, rather than making you write an event loop.
    Allow you to write synchronous or async code, and deal with handoffs and threading for you.

}
"""
