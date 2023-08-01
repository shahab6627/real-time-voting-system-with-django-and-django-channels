from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import PollVote, Candidates
 

import json

class PollVoteConsumer(WebsocketConsumer):
    groups = ["broadcast"]
    def connect(self): 
        self.group_name = self.room_name = self.scope['url_route']['kwargs']['slug']
        print("group name" ,self.group_name)
        print("channel name", self.channel_name)
        self.accept()
        print("connected")
 
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
            )
        
        
    
    def receive(self, text_data=None, bytes_data=None):
        
        data = json.loads(text_data)
        user = data['user']
        candidate_id = data['candidate_id']
        print(user)
        poll_vote = PollVote.objects.create(user_id = user, candidate_id=candidate_id)
        # poll_vote.save()
        
        total_votes = Candidates.objects.get(id = candidate_id)
        t_votes = total_votes.total_votes
        candidate_name = total_votes.candidate_name
        # self.send(json.dumps({'votes':total_votes.total_votes, 'user_id':candidate_id}))
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
        'type':'chat.showVotes',
        't_votes':t_votes,
        'user':candidate_id,
        'candidate':candidate_name
        })
        
    def chat_showVotes(self, event):
        self.send(text_data=json.dumps(
            
            {
            'type' : 'websocket.send',
            'votes': event['t_votes'],
             'user_id':event['user'],
             'candidate': event['candidate']
        }))
    
    def disconnect(self, code):
        print("disconnet")
        
        
        