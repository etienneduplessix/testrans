Structure for the JSON API that js will communicate with to grab info, sign in new users without intra login, add games + scores etc

basic url:
	/user_api

register new user with email/password:
	/user_api/register

login user with email/password:
	/user_api/login

get info about self, from the USER model:
	/user_api/who_am_i

get info about user, from the USER model:
	/user_api/who_is/<username>

	/user_api/register

get info about self, from the USER model:
	/user_api/who_am_i

get players online within the last minute, from the USER model:
	/user_api/online