
/*
	websockets:
		a socket is created as soon as the player logs in, to handle live chat, game requests etc.
		socket messages are json
		json message:
		{
			type: chat_message / game_request / friend_request
			from: <login>
			messsage: (assuming this is a chat message)
		}
*/

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Check if this cookie string begins with the name we want
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

let userid;

function loadProfileData() {
	fetch('/user_api/get_profile_data/')
		.then(response => response.json())
		.then(data => {
			if (data.status === 200) {
				const userData = data.data;
				userid = userData.id;

				// console.log("userId from loadProfileData(): ", userid);
				// Update the profile fields
				document.getElementById('avatar').src = userData.avatar_url;
				document.getElementById('p_name').textContent = userData.username;
				document.getElementById('id_username').value = userData.username;
				document.getElementById('id_email').value = userData.email;
				document.getElementById('id_first_name').value = userData.first_name;
				document.getElementById('id_last_name').value = userData.last_name;

				// Update the game statistics
				const totalGames = userData.total_games || 0; // Default to 0 if null or undefined
				const totalWins = userData.total_wins || 0;   // Default to 0 if null or undefined
				const totalLosses = userData.total_losses || 0; // Default to 0 if null or undefined

				document.getElementById('total_games').textContent = totalGames;
				document.getElementById('total_wins').textContent = totalWins;
				document.getElementById('total_losses').textContent = totalLosses;

				// Load match history
				const historyBody = document.getElementById('match-history-body');
				historyBody.innerHTML = ''; // Clear existing rows

				if (userData.match_history && userData.match_history.length > 0) {
					userData.match_history.forEach(match => {
						const row = document.createElement('tr');
						// const opponents = match.opponents.join(', ');  // Join opponent usernames into a single string
						row.innerHTML = `

							<td>${match.date_time_start}</td>
							<td>${match.opponents}</td>
							<td>${match.match_duration}</td>
							<td>${match.score}</td>
						`;
						historyBody.appendChild(row);
					});
				} else {
					// If match history is empty, show a message
					const emptyMessageRow = document.createElement('tr');
					emptyMessageRow.innerHTML = `

						<td colspan="3" class="text-center">No match history available.</td>
					`;
					historyBody.appendChild(emptyMessageRow);
				}
				// Handle cases where no games have been played
				if (totalGames === 0) {
					document.getElementById('winsLossesChart').style.display = 'none'; // Hide the chart

					const statsMessage = document.createElement('p');
					statsMessage.textContent = "No games played yet.";
					document.querySelector('.chart-container').appendChild(statsMessage); // Append message below the chart
					// document.querySelector('.chart-container').appendChild(statsMessage); // Append message below the chart
				} else {
					// Initialize the pie chart with wins and losses
					const ctx = document.getElementById('winsLossesChart').getContext('2d');
					new Chart(ctx, {
						type: 'pie',
						data: {
							labels: ['Wins', 'Losses'],
							datasets: [{
								data: [totalWins, totalLosses],
								backgroundColor: ['#28a745', '#dc3545'],
								borderWidth: 1
							}]
						},
						options: {
							responsive: true,
							plugins: {
								legend: {
									position: 'bottom',
								},
								tooltip: {
									callbacks: {
										label: function(tooltipItem) {
											return tooltipItem.label + ': ' + tooltipItem.raw;
										}
									}
								}
							}
						}
					});
				}
			} else {
				alert('Failed to load profile data: ' + data.message);
			}
		})
		.catch(error => {
			console.error('Error fetching profile data:', error);
		});
}


function loadFriendsData() {
	// console.log("User ID from loadFriendsData:", userid);
	fetch('/user_api/friends/') // Adjust the URL to your endpoint
		.then(response => response.json())
		.then(data => {
			if (data.status === 200) {
				const friendsList = data.data.friends; // Assuming the response structure
				const friendsContainer = document.getElementById('friends-list'); // The container where friends will be displayed
				friendsContainer.innerHTML = ''; // Clear existing content

				if (friendsList.length > 0) {
					friendsList.forEach(friend => {
						const friendItem = document.createElement('div');
						friendItem.className = 'friend-item'; // Add a class for styling
						friendItem.innerHTML = `
							<img src="${friend.avatar_url}" alt="${friend.username}'s avatar" class="friend-avatar">
							<span>${friend.first_name} ${friend.last_name} (@${friend.username})</span>
						`;
						friendsContainer.appendChild(friendItem);
					});
				} else {
					friendsContainer.innerHTML = '<p>No friends found.</p>';
				}
			} else {
				alert('Failed to load friends data: ' + data.message);
			}
		})
		.catch(error => {
			console.error('Error fetching friends data:', error);
		});
}


let gameJSAdded = true;
let currentPage = '';


let web_socket;
let ws_heartbeat_interval = 0;


//42 api login
function login() {
	const win = window.open('/api', '_blank');

	const timer = setInterval(() => {
		if (win.closed) {
		clearInterval(timer);
		history.pushState({ page: 'gameTypeForm' }, '', 'gameTypeForm');
		loadPage('gameTypeForm');
		}
	}, 500);
}

function submit_registration_form (event) {
	event.preventDefault(); // Prevent the default form submission

		// Gather form data
		var formData = new FormData(this);

		const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		// make post request
		fetch('/user_api/register/', {

			method: 'POST',
			body: formData,
			headers: {
				'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
			},
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

function submit_login_form (event) {
	event.preventDefault(); // Prevent the default form submission

		// Gather form data
		var formData = new FormData(this);
		const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		// make post request
		fetch('/user_api/login/', {
			method: 'POST',
			body: formData,
			headers: {
				'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
			},
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



async function profile_update_form (event)
{
	event.preventDefault(); // Prevent the default form submission

	// Gather form data
	var formData = new FormData(this);
	// make post request
	// await fetch('/user_api/who_am_i')
	// 	.then(res => res.json())
	// 	.then(json_res => {
	// 		// console.log(json_res);
	// 		jsonres = JSON.parse(json_res);
	// 		//when json_res is empty:
	// 		// Uncaught (in promise) SyntaxError: "[object Object]" is not valid JSON
	// 		//at JSON.parse (<anonymous>)
	// 		console.log(jsonres);
	// 		console.log(jsonres.status);
	// 		if (jsonres.status == 200){
	// 			userid = jsonres.data[0]['id'];
	// 			console.log("User ID from who_am_i:", userid);}
	// 		else
	// 			userid = "user not logged :/";
	// 	}).catch(err => {
	// 		console.log(err.response);
	// });
	const csrfToken = getCookie('csrftoken');
	await fetch(`/user_api/profile/${userid}`, {
			method: 'PUT',
			body: formData,
			headers: {
				'X-CSRFToken': csrfToken // Add CSRF token here
			}
		})
		.then(response => response.json())
		.then(data => {
			if (data.status === 200) {
				// history.pushState({ page: 'profile' }, '', 'profile');
				loadPage('profile');
			} else {
				alert('Profile update failed: ' + data.message);
			}
		})
		.catch(error => {
			alert('An error occurred: ' + error);
		});
}


async function pass_update_form (event)
{
	event.preventDefault(); // Prevent the default form submission

	// Gather form data
	var formData = new FormData(this);
	// console.log("in pass_update");
	await fetch('/user_api/who_am_i')
		.then(res => res.json())
		.then(json_res => {
			jsonres = JSON.parse(json_res);
			//when json_res is empty:
			// Uncaught (in promise) SyntaxError: "[object Object]" is not valid JSON
			//at JSON.parse (<anonymous>)
			// console.log(jsonres);
			// console.log(jsonres.status);
			if (jsonres.status == 200)
				userid = jsonres.data[0]['id'];
			else
				userid = "user not logged :/";
		}).catch(err => {
			console.log(err.response);
		});
	//
	// console.log(userid);
	// console.log("in pass_update2222");
	const csrfToken = getCookie('csrftoken');
	// make post request
	await fetch(`/user_api/change_pass/${userid}`, {
		method: 'PUT',
		body: formData,
		headers: {
			'X-CSRFToken': csrfToken // Add CSRF token here
		}
	})
		.then(response => response.json())
		.then(data => {
			if (data.status === 200) {
				history.pushState({ page: 'passwordChange' }, '', 'passwordChange'); // has to be added to history????
				loadPage('profile');
			} else {
				alert('Password change failed: ' + data.message);
			}
		})
		.catch(error => {
			alert('An error occurred: ' + error);
		});
}

window.addEventListener("load", (event) => {
	const urlParams = new URLSearchParams(window.location.search);
	let template = urlParams.get('template')
	if (template == null)
		loadPage('loginForm');
	else
		loadPage(template);
	hookupButtons();
});

window.addEventListener('popstate', function (event) {
	//the thing that actually changes the page when the back button is used.
	// gets triggered when active history entry changes while the user navigates the session history.
	// aka back/forward button used
	if (event.state && event.state.page) {
		loadPage(event.state.page);
	} else {
		loadPage('loginForm');
	}
})

//the separate function keeps it so the event listener doesn't get relinked.
function buttonAction(event) {
	var pageName = event.target.dataset.page;
	history.pushState({ page: pageName }, '', pageName);
	loadPage(pageName);
}
//add button listener to each button with class '.redirectionButton'

function hookupButtons () {
	document.querySelectorAll('button.redirectionButtons').forEach(a => {
			a.addEventListener('click', buttonAction);
});

	if (document.querySelector('#p_name'))
	{
		fetch('/user_api/who_am_i')
		.then(res => res.json())
		.then(json_res => {
			// console.log(json_res);
			jsonres = JSON.parse(json_res);
			//when json_res is empty:
			// Uncaught (in promise) SyntaxError: "[object Object]" is not valid JSON
			//at JSON.parse (<anonymous>)
			// console.log(jsonres);
			// console.log(jsonres.status);
			if (jsonres.status == 200) {
				info = jsonres.data[0]['username'];
				userid = jsonres.data[0]['id'];
				// console.log("User ID from who_am_i:", userid);
			}
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
	if (document.getElementById('profile')) {
		loadProfileData(); // Load profile data for the profile page
		document.getElementById('profile').addEventListener('submit', profile_update_form);
	}
	if (document.getElementById('passChangeForm'))
		document.getElementById('passChangeForm').addEventListener('submit', pass_update_form);
	if (document.getElementById('friends'))
		loadFriendsData();
	if (document.querySelector("#chatInput"))
		document.querySelector("#chatInput").addEventListener('keypress', send_chat_message);
}

function loadPage(pageName) {
	console.log("here " + pageName);
	if (currentPage == pageName)
		return;
	currentPage = pageName;
	//return promise to be able to wait for the page to load
	return fetch('templates/' + pageName + '.html')
		.then((response) => {
		// 1. check response is ok
		if (response.ok)
			return response.text();
		console.error (response);
		return '[ Error fetching resource ' + pageName + ' ]';
	  })
	.then((html) => {
		document.querySelector('#content').innerHTML = html;
		hookupButtons();

	if (pageName == 'game') {
		console.log ("loading game");
		setupgame(pageName);
	}

	if (pageName == 'gameTypeForm')
		web_socket = setup_websocket();
	})
}