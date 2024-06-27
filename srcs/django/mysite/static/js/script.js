/* TODO:
	- find a way to pass data between templates? there has to be something
		better than global variables
	- test!!! game!!!
	- player scores, names

 */

	hookupButtons();

let gameJSAdded = true;
let currentPage = '';

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
function hookupButtons ()
{
	document.querySelectorAll('button.redirectionButtons').forEach(a => {
				a.addEventListener('click', buttonAction);
	});
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

		if (pageName == 'game' && !gameJSAdded)
	{
		console.log('adding js gamescript!');
		const script = document.createElement('script');
		document.body.appendChild(script);
		script.async = true;
		script.src = './game.js';
		script.id = 'gameJs';
		gameJSAdded = true;
	}
	else if (pageName == 'game' && gameJSAdded)
	{
		setupgame();
		// reset_screen(); //function from game.js
	}
	})

	}


function superspecial(e)
{
	pageName = 'playerNames'
	return fetch('./templates/' + pageName + '.html')
		.then((response) => {
		console.log('loading ' + pageName);
		// 1. check response is ok
		if (response.ok) {

			history.pushState({ page: pageName }, '', pageName);
			return response.text();
		}
		console.error (response);
		return '[ Error fetching resource ' + pageName + ' ]';
	  })
	.then((html) => {
		document.querySelector('#content').innerHTML = html;
		hookupButtons();

		redire

		if (pageName == 'game' && !gameJSAdded)
	{
		console.log('adding js gamescript!');
		const script = document.createElement('script');
		document.body.appendChild(script);
		script.async = true;
		script.src = 'JS/game.js';
		script.id = 'gameJs';
		gameJSAdded = true;
	}
	else if (pageName == 'game' && gameJSAdded)
	{
		reset_screen(); //function from game.js
	}
	})
}