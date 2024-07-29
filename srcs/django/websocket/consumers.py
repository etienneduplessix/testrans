# chat/consumers.py

from channels.generic.websocket import WebsocketConsumer
from mysite.tools import myprint
from mysite.models import Online_ws, User

import random


class Consumer(WebsocketConsumer):
	def connect(self):
		myprint("New Connection! ")
		self.accept()

		if 'session' in self.scope:
			myprint("YAY")
		else:
			myprint("NAY")
			# return
		if not self.scope["session"].has_key('login'):
			myprint ("wesocket attempted without login")
			self.close()
			return
		if (User.objects.filter(username=self.scope["session"]['login']).exists()):
			username = User.objects.filter(username=self.scope["session"]['login'])[0]
		else:
			myprint ("user does not exist")
			self.close()
			return

		wsuser = Online_ws(login=username, channelname=self.channel_name)
		wsuser.save()
		# myprint("New Connection! ")
		# self.accept()

	def disconnect(self, close_code):
		myprint("Connection disconnected")
		# Online_ws.objects.filter(channelName=self.channel_name).delete()
		self.close()

	def receive(self, text_data):
		# myprint(type(self.channel_name))
		self.send( self.channel_name +   ' you said: ' + text_data)



# from channels.layers import get_channel_layer

# channel_layer = get_channel_layer()
# await channel_layer.send("channel_name", {
#	 "type": "chat.message",
#	 "text": "Hello there!",
# })
