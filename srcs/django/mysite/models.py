from django.db import models

# table to describe and store info about each user in webapp
class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	email = models.EmailField(max_length=254, unique=True, default="", blank=True)
	intra_oauth = models.BooleanField(default=True )
	password_hash = models.CharField(max_length=100, blank=True)
	last_seen = models.DateTimeField(auto_now=True, blank=True)
	image_link = models.URLField(null=True, blank=True)

	def __str__(self):
		return self.username

# table of relations to describe and store info about friend requests from one user to another
class FriendshipRequest(models.Model):
	user_from = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
	user_to = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user_from.username} -> {self.user_to.username}"

# table of relations to describe and store info about user's friends
class Friend(models.Model):
	user1 = models.ForeignKey(User, related_name='friends_with_user1', on_delete=models.CASCADE)
	user2 = models.ForeignKey(User, related_name='friends_with_user2', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user1.username} & {self.user2.username}"

# table to describe and store info about EACH GAME(game id is unique and connected to next table, GameUserRelation)
class Game(models.Model):
	id = models.AutoField(primary_key=True)
	date_time_start = models.DateTimeField()
	date_time_end = models.DateTimeField()

	def __str__(self):
		return f"Game {self.id} started at {self.date_time_start} and ended at {self.date_time_end}"

# table to describe and store info about GAME in terms of participants(game id is unique and connected to previous table, GameUserRelation,
# and user id is also unique and connected to User table)
# in case of several players table will consit of several rows with the same game id and id of users in that game, as their score
class GameUserRelation(models.Model):
	game = models.ForeignKey(Game, related_name='user_relations', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='game_relations', on_delete=models.CASCADE)
	score = models.IntegerField(default=0)

	def __str__(self):
		return f"User {self.user.username} scored {self.score} in Game {self.game.id}"


### Naomi test table to store websockets

class Online_ws(models.Model):
	login = models.ForeignKey(User, related_name='login', on_delete=models.CASCADE)
	channelname = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.username



# Adding ManyToMany fields to User model through Friend and GameUserRelation models
User.add_to_class('friends',
				  models.ManyToManyField('self', through=Friend, symmetrical=False, related_name='user_friends'))
User.add_to_class('games', models.ManyToManyField(Game, through=GameUserRelation, related_name='game_users'))

#User.add_to_class('channels', models.ManyToManyField(Online_ws, related_name='online_users'))

