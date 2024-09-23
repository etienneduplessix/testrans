working on websockets for now
chat is working
user popup working
	set login menu as home
	login/register forms to toggle eachother
	friend requests
		KINDA WORKS?
		add to DB
		delete li when respond is sent
		not allow user to send request to self
		send newfriend ws message to both users

todo:
	how to determine if user is online? add color in popup
	chat database -> how much to keep? last num of messages / time frame



/*
	websockets:
		a socket is created as soon as the player logs in, to handle live chat, game requests etc.
		socket messages are json
		json message:
		{
			type: chat_message  / friend_request / game_request / new_friend
			from: <login>
			messsage: (assuming this is a chat message)
		}


  STEPS	friend request:
			note: no 'from' field bc easier to get from server
	1	user1 -> server : send request to user 2 {type: friend_request,
													subtype: request,
													to: user2}

	2	server -> user2 : user1 sent a request {type: friend_request,
													subtype: request,
													from: sender,
													to: user2}

	3	user2 -> server : accept/decline {type: friend_request,
													subtype: res ,
													to: user1,
													 state: true / false}

	4	server -> user1 : was declined {type: friend_request,
													subtype: newfriend,
													to: user1,
													from: sender,
													state:  false}

	5	server -> user1 + 2 : new friend!{type: friend_request,
													subtype: newfriend,
													friend: newFriendLogin,
													state:  true}


*/




user 1 sent 2 request
user2 accepted

user2=> server {res, state: true}
server=> user2client {newfriens, friend:u1}

