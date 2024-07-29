class PongGame:
	def __init__(self):
		self.ball_position = [50, 50]
		self.ball_velocity = [1, 1]
		self.paddle1_position = 50
		self.paddle2_position = 50
		self.score = [0, 0]

	def update(self):
		# Update ball position
		self.ball_position[0] += self.ball_velocity[0]
		self.ball_position[1] += self.ball_velocity[1]

		# Collision with top and bottom walls
		if self.ball_position[1] <= 0 or self.ball_position[1] >= 100:
			self.ball_velocity[1] = -self.ball_velocity[1]

		# Check for scoring
		if self.ball_position[0] <= 0:
			self.score[1] += 1
			self.reset_ball()
		elif self.ball_position[0] >= 100:
			self.score[0] += 1
			self.reset_ball()

		# Collision with paddles
		# (Add your paddle collision logic here)

	def move_paddle(self, paddle, direction):
		if paddle == 1:
			self.paddle1_position += direction
		elif paddle == 2:
			self.paddle2_position += direction

	def reset_ball(self):
		self.ball_position = [50, 50]
		self.ball_velocity = [1, 1]

	def get_state(self):
		return {
			'ball_position': self.ball_position,
			'paddle1_position': self.paddle1_position,
			'paddle2_position': self.paddle2_position,
			'score': self.score
		}
