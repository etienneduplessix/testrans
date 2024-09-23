
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




function li_span_click(event)
{
	to = event.target.parentElement.dataset.username;

	if (event.target.classList.contains("chatmsg_username"))
	{
		if (to != document.querySelector("#p_name").innerText)
			showuserpopup(event);
		return
	}

	json_data = JSON.parse("{}")
	json_data['subtype'] = 'res';
	json_data['to'] = to;

	if (event.target.classList.contains("chatmsg")){
		if (event.target.classList.contains("yes"))
			{
				json_data['state'] = true;
				deal_with_friend_req(json_data);
			}
		else
			json_data['state'] = false;

		ws_send_req("friend_request", json_data);
	}

	if (event.target.classList.contains("gamereq")){
		if (event.target.classList.contains("yes"))
			{
				json_data['state'] = true;
				deal_with_game_req(json_data);
			}
		else
			json_data['state'] = false;

		ws_send_req("game_request", json_data);
	}

	event.target.parentElement.remove();
}

function stringToHslColor(str, s, l) {
	var hash = 0;
	for (var i = 0; i < str.length; i++) {
	  hash = str.charCodeAt(i) + ((hash << 5) - hash);
	}

	var h = hash % 360;
	return 'hsl('+h+', '+s+'%, '+l+'%)';
}

function make_chat_il(from, message, il_class="")
{
	var newelement = document.createElement("li");
	newelement.setAttribute("data-username", from);
	if (il_class != "")
		newelement.classList.add(il_class);
	var color = stringToHslColor(from, 50, 50);
	newelement.innerHTML = `<span class="chatmsg_username" style="color:`+color+`">` + from + `</span>` + (from != "" ? `:` : "") + message;

	newelement.querySelectorAll("span").forEach(e => e.addEventListener('click', li_span_click));
	// newelement.addEventListener('click', showuserpopup);

	if (document.querySelector("#chatBox"))
		{
			var ul = document.querySelector("#chatBox");
			ul.appendChild(newelement);
			ul.scrollTop = ul.scrollHeight;

		}
}

function deal_with_friend_req (data)
{
	if (data.subtype == 'err')
		make_chat_il(data.from, data.message, "err")
	if (data.subtype == 'request')
		make_chat_il(data.from, 'Wants to be your friend! Accept? <span class="chatmsg yes">Y</span> / <span class="chatmsg no">N</span>')
	if (data.subtype == 'newfriend')
	{
		if (data.state == false /* && data.friend != document.querySelector("#p_name").innerText */ )
			make_chat_il( data.friend, 'No friends:( sorry boo')
		else if (data.state == true)
			make_chat_il( data.friend, 'New Friend :)')
	}
}

function deal_with_game_req(data) {
	if (data.subtype === 'request') {
	    make_chat_il(data.from, 'Wants to play a game! Accept? <span class="gamereq yes">Y</span> / <span class="gamereq no">N</span>');
	}
  
	const csrfToken = getCookie('csrftoken');
	if (data.subtype === 'newgame') {
	    if (data.state === false) {
		  make_chat_il(data.friend, 'Game request politely declined :( sorry boo');
	    } else if (data.state === true) {
		let p_name = document.getElementById("p_name").textContent;
		console.log(p_name)
		console.log(data.friend)
		if(p_name == data.friend)
			{
			fetch('/game_api/init/', {
				method: 'POST',
				headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
				},
				body: JSON.stringify({
				to: data.friend, // Corrected typo here
				from: data.to// Assuming you also need to pass the `from` field
				}),
				})
				.then(response => response.json())
				.then(data => {
					console.log('Success:', data);
				})
				.catch((error) => {
					console.error('Error:', error);
				});
			}
		else
		{
			fetch('/game_api/init2/', {
				method: 'POST',
				headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
				},
				body: JSON.stringify({
				to: data.friend, // Corrected typo here
				from: data.to// Assuming you also need to pass the `from` field
				}),
				})
				.then(response => response.json())
				.then(data => {
					console.log('Success:', data);
				})
				.catch((error) => {
					console.error('Error:', error);
				});
		}
	load_game();
	}
	}
  }

  function load_game(event)
  {
	loadPage('game');
  }

  function send_game_request(event)
{
	var userpopup = document.querySelector('div.user_popup');
	var receiver = userpopup.dataset.popup_username;

	json = JSON.parse("{}");
	json['subtype'] = "request";
	json['to'] = receiver;

	ws_send_req("game_request", json);
	document.querySelector("div.user_popup").classList.remove("popup_show");

}

function page_game() {
	var pageName = window.location.pathname.split('/').pop();
	console.log(pageName);
	return pageName;
  }


function setup_websocket()
{
	if (web_socket && web_socket.OPEN)
			return web_socket;
	var roomname = "lobby";
	var url = `ws://${window.location.host}/ws/${roomname}/`
	var ws = new WebSocket(url);
	// var ws = new WebSocket("ws://127.0.0.1:8000/ws/" + roomname + '/');
	if (!ws.OPEN)
	{
		console.error("WEBSOCKET no bueno:(")
		return;
	}

	ws.onopen = function(e){
		ws.send(JSON.stringify({
			'type': 'heartbeat',
			'message': '<3'
		}));

		ws_heartbeat_interval = window.setInterval(()=>{
			web_socket.send(JSON.stringify({
				'type': 'heartbeat',
				'message': '<3'
			}));
		}, 10 * 1000) //every 10sec
	};

	ws.onmessage = function(e) {
		const data = JSON.parse(e.data);
		console.log(data);

		if (data.type == 'game_request')
			{
				deal_with_game_req(data);
			}
		else if (data.type == 'friend_request')
			deal_with_friend_req(data);
		else if (data.type == 'private_message')
		{
			let username = data.from;
			let message = data.message;
			make_chat_il(username, message, "private_message");
		}
		else if (data.type == 'chat_message')
		{
			let username = data.from;
			let message = data.message;
			make_chat_il(username, message);
		}
		else if (data.type == 'err')
		{
			let message = data.message;
			make_chat_il("", message, "err");
		}
		else if (data.type == 'game_timer')
		{
		let	message = data.message;
		console.log(message);
			startGame();
		}
	};

	ws.onclose = function(e) {
		console.log('Socket closed. code: ' + e.code);
		clearInterval(ws_heartbeat_interval);
		ws_heartbeat_interval = 0;
	};

	return ws;
}

function send_chat_message(e)
{
	if (!web_socket || e.charCode != 13)
		return;
	message = e.target.value;
	if (message.startsWith('@'))
	{
		username = message.slice (0, message.indexOf(" ")).substring(1);
		web_socket.send(JSON.stringify({
			'type': 'private_message',
			'to': username,
			'message': message
		}));
	}
	else
	{
		web_socket.send(JSON.stringify({
			'type': 'chat_message',
			'message': message
		}));
	}

	e.target.value = ''
}

function showuserpopup(event)
{
	var userpopup = document.querySelector('div.user_popup');
	var userpopup_content = document.querySelector('div.user_popup div.popup_content');
	var username = event.srcElement.innerText;

	var img_el = userpopup_content.querySelector('img');
	var username_el = userpopup_content.querySelector('#popup_username');
	var email_el = userpopup_content.querySelector('#popup_email');
	var online_el = userpopup_content.querySelector('button#online_vis');

	fetch('/user_api/who_is/' + username)
	.then(res => res.json())
	.then(json_res => {

		var parsed_json = JSON.parse(json_res);
		if (parsed_json.status == 200)
			info = parsed_json.data;
		else
			info = parsed_json.data['error'];

		img_el.setAttribute('src', info['image_link'])
		username_el.innerText = info['username'];
		email_el.innerText = info['email'];
		userpopup.setAttribute('data-popup_username', info['username']);

		last_seen_min = (Date.now() - Date.parse(info.last_seen)) / 1000 / 60;
		online_el.title = `last seen ${last_seen_min.toFixed(3)} min ago`
		online_el = online_el.querySelector("svg")
		if (last_seen_min >= 2)
			online_el.style.fill = "greenyellow"
		else if (last_seen_min >= 10)
			online_el.style.filter = "darkred"

		userpopup.classList.toggle("popup_show");
	})
}

function ws_send_req(type, json_data)
{
	if (!web_socket)
		return;
	json_data["type"] = type;

	web_socket.send(JSON.stringify(json_data));
}

function send_friend_request(event)
{
	var userpopup = document.querySelector('div.user_popup');
	var receiver = userpopup.dataset.popup_username;

	json = JSON.parse("{}");
	json['subtype'] = "request";
	json['to'] = receiver;

	ws_send_req("friend_request", json);
	document.querySelector("div.user_popup").classList.remove("popup_show");
}


function block_user(event){
	var userpopup = document.querySelector('div.user_popup');
	var receiver = userpopup.dataset.popup_username;

	json = JSON.parse("{}");
	json['to'] = receiver;

	ws_send_req("block", json);
	document.querySelector("div.user_popup").classList.remove("popup_show");

}