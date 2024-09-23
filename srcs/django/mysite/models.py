from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now, timedelta


# table to describe and store info about each user in webapp
class User(AbstractUser):
	intra_oauth = models.BooleanField(default=True)
	image_link = models.URLField(null=True, blank=True)
	last_seen = models.DateTimeField(auto_now=True)
	blocked_users = ArrayField(models.CharField(max_length=100), default=list)

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




class Game(models.Model):
    id = models.AutoField(primary_key=True)
    date_time_start = models.DateTimeField()
    date_time_end = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Game {self.id} started at {self.date_time_start} and ended at {self.date_time_end} with state {self.state}"


# table to describe and store info about GAME in terms of participants(game id is unique and connected to previous table, Game,
# and user id is also unique and connected to User table)
# in case of several players table will consit of several rows with the same game id and id of users in that game, as their score


class GameUserRelation(models.Model):
    game = models.ForeignKey('Game', related_name='user_relations', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='game_relations', on_delete=models.CASCADE)
    side = models.CharField(max_length=5, default='left')
    score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(GameUserRelation, self).save(*args, **kwargs)
        self.side = 'left' if self.id % 2 == 0 else 'right'
        super(GameUserRelation, self).save(*args, **kwargs)

    def __str__(self):
        return f"User {self.user.username} scored {self.score} in Game {self.game.id}"



# Adding ManyToMany fields to User model through Friend and GameUserRelation models
User.add_to_class('friends',
				models.ManyToManyField('self', through=Friend, symmetrical=True, related_name='user_friends'))
# User.add_to_class('friends',
# 				models.ManyToManyField('self', through=Friend, symmetrical=False, related_name='user_friends'))
User.add_to_class('games', models.ManyToManyField(Game, through=GameUserRelation, related_name='game_users'))



class Online_WS(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	username =  models.CharField(max_length=2000, default="")
	channelname = models.CharField(max_length=2000)
