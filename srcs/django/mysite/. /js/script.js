
/* TODO:

	- test!!! game!!!
	- player scores, names

 */

// var ws;

// function setup_websocket()
// {
// 	console.log ("WEBSOCKET SETUP");
// 	ws = new WebSocket("ws://localhost:8000");
// 	ws.onmessage = (data) => console.log(data.data);
// }

let gameJSAdded = true;
let currentPage = '';

//42 api login
function login()
{
	const win = window.open('/api', '_blank');

	const timer = setInterval(() => {
		if (win.closed) {
		clearInterval(timer);
		history.pushState({ page: 'gameTypeForm' }, '', 'gameTypeForm');
		loadPage('gameTypeForm');
		}
	}, 500);
}

function submit_registration_form (event)
{
	event.preventDefault(); // Prevent the default form submission

		// Gather form data
		var formData = new FormData(this);

		// make post request
		fetch('/game_api/register/', {
			method: 'POST',
			body: formData
		})
		.then(response => response.json())
		.then(data => {
			if (data.status === 200) {
				history.pushState({ page: 'gameTypeForm' }, '', 'gameTypeForm');
				loadPage('gameTypeForm');
			} else {
				alert('Registration failed: ' + data.message);
			}
		})
		.catch(error => {
			alert('An error occurred: ' + error);
		});
}

function submit_login_form (event)
{
	event.preventDefault(); // Prevent the default form submission

		// Gather form data
		var formData = new FormData(this);

		// make post request
		fetch('/game_api/login/', {
			method: 'POST',
			body: formData
		})
		.then(response => response.json())
		.then(data => {
			if (data.status === 200) {
				history.pushState({ page: 'gameTypeForm' }, '', 'gameTypeForm');
				loadPage('gameTypeForm');
			} else {
				alert('Login failed: ' + data.message);
			}
		})
		.catch(error => {
			alert('An error occurred: ' + error);
		});
}


window.addEventListener("load", (event) => {
	console.log ("LOAD EVENT");
	const urlParams = new URLSearchParams(window.location.search);
	let template = urlParams.get('template')
	if (template == null)
		loadPage('home');
	else
		loadPage(template);
	hookupButtons();
	// setup_websocket();

});

window.addEventListener('popstate', function (event) {
	//the thing that actually changes the page when the back button is used.
	// gets triggered when active history entry changes while the user navigates the session history.
	// aka back/forward button used
	if (event.state && event.state.page) {
		loadPage(event.state.page);
	} else {
		loadPage('home');
	}
})

//the separate function keeps it so the event listener doesn't get relinked.
function buttonAction(event)
{
	var pageName = event.target.dataset.page;

	history.pushState({ page: pageName }, '', pageName);
	loadPage(pageName);
}
//add button listener to each button with class '.redirectionButton'
var jsonres;
function hookupButtons ()
{
	console.log("in button hook");
	document.querySelectorAll('button.redirectionButtons').forEach(a => {
				a.addEventListener('click', buttonAction);
	});


	if (document.querySelector('#p_name'))
	{
		fetch('http://127.0.0.1:8000/game_api/who_am_i')
		.then(res => res.json())
		.then(json_res => {
			jsonres = JSON.parse(json_res);
			console.log(jsonres);
			console.log(jsonres.status);
			if (jsonres.status == 200)
				info = jsonres.data[0]['username'];
			else
				info = "user not logged :/";
			document.querySelector('#p_name').innerText = info;
		})
	}


	if (document.getElementById('registerForm'))
	{
		document.getElementById('registerForm').addEventListener('submit', submit_registration_form);
		document.getElementById('loginForm').addEventListener('submit', submit_login_form);
	}
}

function loadPage(pageName) {
	if (currentPage == pageName)
		return;
	currentPage = pageName;

	//return promise to be able to wait for the page to load
	return fetch('templates/' + pageName + '.html')
		.then((response) => {
		console.log('loading ' + pageName);
		// 1. check response is ok
		if (response.ok)
			return response.text();
		console.error (response);
		return '[ Error fetching resource ' + pageName + ' ]';
	  })
	.then((html) => {
		document.querySelector('#content').innerHTML = html;
		hookupButtons();

	if (pageName == 'game')
		setupgame();
	})

	}

