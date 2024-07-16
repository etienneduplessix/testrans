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

function login()
{
	const win = window.open('/api', '_blank');

	const timer = setInterval(() => {
		if (win.closed) {
		clearInterval(timer);
		loadPage('gameTypeForm');
		}
	}, 500);
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
		fetch('http://127.0.0.1:8000/game_api')
		.then(res => res.json())
		.then(json_res => {
			console.log(json_res)
			jsonres = JSON.parse(json_res);
			document.querySelector('#p_name').innerText = jsonres[0]['fields']['username'];
		})


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
		if (response.ok) {

			return response.text();
		}
		console.error (response);
		return '[ Error fetching resource ' + pageName + ' ]';
	  })
	.then((html) => {
		document.querySelector('#content').innerHTML = html;
		hookupButtons();

	if (pageName == 'game')
	{
		setupgame();
	}
	})

	}


function superspecial(e)
{
	pageName = 'playerNames'
	return fetch('./templates/' + pageName + '.html')
		.then((response) => {
			console.log('loading ' + pageName);
			console.log("then 1")
			// 1. check response is ok
			if (response.ok) {

				history.pushState({ page: pageName }, '', pageName);
				return response.text();
			}
			console.error (response);
			return '[ Error fetching resource ' + pageName + ' ]';
			})
		.then((html) => {
			console.log("then 2")
			document.querySelector('#content').innerHTML = html;
			hookupButtons();

			if (pageName == 'game')
			{
				reset_screen(); //function from game.js
			}
		})
}