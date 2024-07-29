

# YULIAS WORK
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from mysite.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	password_confirm = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password_confirm']
		extra_kwargs = {
			'password': {'write_only': True},
		}

	# def validate(self, data):
	#
	#		 raise serializers.ValidationError("Passwords do not match.")
	#	 return data

	def save(self):
		# validated_data.pop('password_confirm')
		user = User(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			intra_oauth=False,
		)
		if self.validated_data['password'] != self.validated_data['password_confirm']:
			raise serializers.ValidationError({'password': 'Passwords do not match.'})
		user.password_hash=make_password(self.validated_data['password'])
		user.save()
		return user
