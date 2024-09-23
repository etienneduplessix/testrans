# chat/consumers.py

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from mysite.tools import *
from mysite.models import  *
from asgiref.sync import async_to_sync

import json
import random
import datetime

# Close code 4000 is reserved for error code for user who tried to connect without log in
		#  https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code

class ChatConsumer(WebsocketConsumer):

	def send_private_message(self, event):
		if not User.objects.filter(username=event["to"]).exists():
			self.send(text_data=json.dumps({"type": "err", "message": f"user { event['to'] } does not exist"}))
			return
		if not Online_WS.objects.filter(username=event["to"]).exists():
			self.send(text_data=json.dumps({"type": "err", "message": f"user { event['to'] } is not online"}))
			return
		if event["to"] in User.objects.get(username=self.username).blocked_users:
			self.send(text_data=json.dumps({"type": "err", "message": f"user { event['to'] } is blocked"}))
			return

		message_to_login(event["to"], {
					"type": "private.message",
					"to": event["to"],
					"from": self.username,
					"message": event["message"]})

		self.send(text_data=json.dumps({"type": "private_message", "from": self.username, "message": event["message"]}))


	def connect(self):
		if 'login' not in self.scope["session"]:
			myprint ("wesocket attempted without login")
			self.disconnect(4000)
			return
		if (User.objects.filter(username=self.scope["session"]['login']).exists()):
			self.username = self.scope["session"]['login']

		else:
			myprint ("user does not exist")
			self.disconnect(4001)
			return

		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = f"chat_{self.room_name}"

		#add to db
		ws = Online_WS(
				user = self.scope["user"],
				username = self.username,
				channelname = self.channel_name)
		if Online_WS.objects.filter(user=self.scope["user"]).count() > 0:
			Online_WS.objects.get(user=self.scope["user"]).delete()
		ws.save()

		# Join room group
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name, self.channel_name
		)
		self.accept()

	def disconnect(self, close_code):
		myprint("Connection disconnected. code: " + str (close_code))
		if close_code == 1000: #normal closure code
			async_to_sync(self.channel_layer.group_discard)(
				self.room_group_name, self.channel_name
			)
			Online_WS.objects.get(user=self.scope["user"]).delete()
		ws_cleanup()
		self.close(close_code)

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		myprint(text_data_json)
		type = text_data_json["type"]

		if type == 'chat_message':
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, {"type": "chat.message", "from": self.username, "message": text_data_json["message"]}
			)
		elif type == 'private_message':
			self.send_private_message(text_data_json)

		elif type == 'friend_request':
			# STEP 2 this will redirect the message to all members of the room.
			text_data_json["from"] = self.username
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, text_data_json)
		elif type == 'game_request':
			# STEP 2 this will redirect the message to all members of the room.
			text_data_json["from"] = self.username
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, text_data_json)
		elif type == 'block':
			user = User.objects.get(username=self.username)
			user.blocked_users += [text_data_json["to"]]
			user.save()
			self.send(text_data=json.dumps({"type": "err", "message": f"user { text_data_json['to'] } is now blocked"}))
		elif type == 'send_game_start':
			myprint2("HERE send_game_start")

			user = User.objects.get(username=self.username)
			user3 = user.username
			myprint(user3)
			game_user_rel = GameUserRelation.objects.filter(user=user).last()
			user2 =GameUserRelation.objects.filter(game=game_user_rel.game).exclude(user=user).first()
			myprint3(user2.user.username)
			username2 = user2.user.username
			game = game_user_rel.game
			if game.date_time_end == game.date_time_start:
				# send game start timer to user a and b
				game_rels = GameUserRelation.objects.filter(game=game)
				for g in game_rels:
					myprint2("sending... + " + User.objects.get(id=g.user_id).username)
					username = User.objects.get(id=g.user_id).username
					#User.game_relations.get(game=game).exclude(user=g.user).first().user.username
					# username2 = User.game_relations.get(game=game).exclude(user=g.user).first().user.username
					message_to_login(username, {
						"type": "game_timer",
						"gamestart_time": int((datetime.datetime.now() + datetime.timedelta(seconds=5)).timestamp()),
						"player1":(user3), 
						"player2":(username2),
						"game_id": game.id
					})
			else:
				self.send(text_data=json.dumps({"type": "err", "message": "no active games!"}))

		elif type == 'heartbeat':
			user = User.objects.get(username=self.scope["session"]['login'])
			user.lastSeen = datetime.datetime.now()
			user.save()
			ws_cleanup()


	def start_game(self, event):
		if event["to"] != self.username:
			return

			self.send(text_data=json.dumps({
				"type": "game_start",
				"from": event["from"]
			}))

	def game_timer(self, event):
			self.send(text_data=json.dumps(event))
	def game_request(self, event):
		if event["to"] != self.username:
			return

		if event["subtype"] == 'request' or event["subtype"] == 'newgame':
			# redirect request to client
			# myprint (str(event))
			self.send(text_data=json.dumps(event))

		if event["subtype"] == 'res':
			newgame_msg = json.loads("{}")
			newgame_msg["type"] = "game_request"
			newgame_msg["subtype"] = "newgame"
			newgame_msg["to"] = event['to']
			newgame_msg["friend"] = event['from']
			newgame_msg["state"] = event['state']
			myprint2(event['from'])
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, newgame_msg)
			newgame_msg["to"] = event['from']
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, newgame_msg)

	def friend_request(self, event):
		myprint(event)
		if "from" in event.keys() and event["from"] in User.objects.get(username=self.username).blocked_users:
			return

		if event["to"] != self.username:
			return

		if event["subtype"] == 'request':
			# check if user is already a friend
			entries = Friend.objects.filter(user1=self.scope["user"],
							user2 = User.objects.get(username=event['from']))
			entries2 = Friend.objects.filter(user1=User.objects.get(username=event['from']),
							user2 = self.scope["user"])

			if entries.count() > 0 or entries2.count() > 0:
				message_to_login(event["from"], {
					"type": "friend_request",
					"to": event["from"],
					"from": self.username,
					"subtype": "err",
					"message": f"You and {event['to']} are already friends!"
					})
				myprint	("here!")
				return

		if event["subtype"] == 'request' or event["subtype"] == 'newfriend' or event["subtype"] == 'err':
			self.send(text_data=json.dumps(event))
			return

		if event["subtype"] == 'res':
			newgame_msg = json.loads("{}")
			newgame_msg["type"] = "friend_request"
			newgame_msg["subtype"] = "newfriend"
			newgame_msg["to"] = event['to']
			newgame_msg["friend"] = event['from']
			newgame_msg["state"] = event['state']
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, newgame_msg)
			newgame_msg["to"] = event['from']
			newgame_msg["friend"] = event['to']
			async_to_sync(self.channel_layer.group_send)(
				self.room_group_name, newgame_msg)

			if event['state']:
				friend = Friend (
					user1 = self.scope["user"],
					user2 = User.objects.get(username=event['from']),
				)
				friend.save()

	def chat_message(self, event):
		if event["from"] in User.objects.get(username=self.username).blocked_users:
			return
		message = event["message"]
		sender = event["from"]

		# Send message to WebSocket
		self.send(text_data=json.dumps({"type": "chat_message", "from": sender, "message": message}))

	def private_message(self, event):
		if event["from"] in User.objects.get(username=self.username).blocked_users:
			return
		message = event["message"]
		sender = event["from"]
		# Send message to WebSocket
		self.send(text_data=json.dumps({"type": "private_message", "from": sender, "message": message}))

def message_to_login(login, json_message):
	try:
		receiver_channelname = Online_WS.objects.get(username=login).channelname
	except:
		myprint ("No such user! " + login)
		return

	async_to_sync(get_channel_layer().send)(
					receiver_channelname, json_message
				)

# deletes any WS object that hasn't sent a heartbeat in 20 sec
# heartbeat is every 10sec
def ws_cleanup():
	timediff = datetime.datetime.now() - datetime.timedelta(seconds=20)
	online_users = User.objects.filter(last_seen__lte=timediff)

	for user in online_users:
		try:
			ws_obj = Online_WS.objects.get(user=user)
			ws_obj.delete()
		except Exception as error:
			# handle the exception
			# myprint("user has no WS entry:" + str(error) +" " + str(user)) # An exception occurred:
			pass
