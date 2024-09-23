import neat
import random
import math
import time

class PongGame:
    def __init__(self, width=1000, height=500):
        self.width = width
        self.height = height
        self.paddle_width = 20
        self.paddle_height = 100
        self.paddle_speed = 10
        self.reset()  # Reset all game values
        self.pause_timer = 0  # Timer for pausing the ball
        self.pause_duration = 2  # 2-second pause duration

    def reset(self):
        """Resets the game to the initial state."""
        self.ball_position = [self.width // 2, self.height // 2]
        self.ball_velocity = self.random_velocity()
        self.paddle1_position = self.paddle2_position = self.height // 2
        self.score = [0, 0]
        self.left_hits = 0
        self.right_hits = 0
        self.gameon = False
        self.pause_timer = 0  # Reset the pause timer

    def random_velocity(self):
        """Generates a random initial velocity for the ball."""
        return [
            random.choice([-1, 1]) * random.uniform(1.0, 2.0),
            random.choice([-1, 1]) * random.uniform(1.0, 2.0)
        ]

    def move_paddle(self, left=True, up=True):
        """Moves the paddles. `left` determines if it's paddle1 (True) or paddle2 (False), and `up` determines the direction."""
        paddle_pos = self.paddle1_position if left else self.paddle2_position
        paddle_pos += -self.paddle_speed if up else self.paddle_speed
        paddle_pos = max(0, min(self.height - self.paddle_height, paddle_pos))

        if left:
            self.paddle1_position = paddle_pos
        else:
            self.paddle2_position = paddle_pos

    def check_collision(self, paddle_pos):
        """Checks if the ball collides with a paddle."""
        return paddle_pos <= self.ball_position[1] <= paddle_pos + self.paddle_height

    def apply_randomness(self):
        """Applies slight random adjustments to the ball's velocity."""
        self.ball_velocity[0] += random.uniform(-0.5, 0.5)
        self.ball_velocity[1] += random.uniform(-0.5, 0.5)

    def update_ball_position(self):
        """Updates the ball's position and handles collisions."""
        if self.pause_timer > 0:
            self.pause_timer -= 1  # Decrease the pause timer
            return  # Don't update the ball position during the pause

        # Move the ball
        self.ball_position[0] += self.ball_velocity[0]
        self.ball_position[1] += self.ball_velocity[1]

        # Ball collision with top and bottom walls
        if self.ball_position[1] <= 0 or self.ball_position[1] >= self.height:
            self.ball_velocity[1] = -self.ball_velocity[1]

        # Ball collision with paddles
        if self.ball_position[0] <= self.paddle_width:  # Left paddle
            if self.check_collision(self.paddle1_position):
                self.ball_velocity[0] = -self.ball_velocity[0]
                self.apply_randomness()
                self.left_hits += 1
        elif self.ball_position[0] >= self.width - self.paddle_width:  # Right paddle
            if self.check_collision(self.paddle2_position):
                self.ball_velocity[0] = -self.ball_velocity[0]
                self.apply_randomness()
                self.right_hits += 1

    def handle_scoring(self):
        """Handles scoring and resets the ball after a 2-second pause."""
        if self.ball_position[0] <= 0:  # Ball out of left side
            self.score[1] += 1
            self.start_pause()
        elif self.ball_position[0] >= self.width:  # Ball out of right side
            self.score[0] += 1
            self.start_pause()

    def start_pause(self):
        """Pauses the game for 2 seconds before restarting the ball."""
        self.pause_timer = self.pause_duration * 60  # 2 seconds in frames (assuming 60 FPS)
        self.ball_position = [self.width // 2, self.height // 2]  # Keep ball in the center

    def reset_ball(self):
        """Resets the ball to the center with a random velocity."""
        self.ball_position = [self.width // 2, self.height // 2]
        self.ball_velocity = self.random_velocity()

    def get_state(self):
        """Returns the current game state."""
        return {
            'ball_position': self.ball_position,
            'paddle1_position': self.paddle1_position,
            'paddle2_position': self.paddle2_position,
            'score': self.score,
            'gameon': self.gameon,
        }

    def start(self):
        """Starts the game and initializes the ball movement."""
        self.gameon = True
        self.reset_ball()

    def update(self):
        """Main game loop logic: update ball position and handle scoring."""
        self.update_ball_position()
        self.handle_scoring()


    # def train_ai(self, genome1, genome2, config):
    #     net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    #     net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    #     self.start()
    #     while max(self.score) < 1 and self.left_hits <= 50:
    #         output1 = net1.activate((self.paddle1_position, self.ball_position[1], abs(self.ball_position[0] - self.paddle_width)))
    #         decision1 = output1.index(max(output1))

    #         if decision1 == 1:
    #             self.move_paddle(left=True, up=True)
    #         elif decision1 == 2:
    #             self.move_paddle(left=True, up=False)

    #         output2 = net2.activate((self.paddle2_position, self.ball_position[1], abs(self.width - self.ball_position[0] - self.paddle_width)))
    #         decision2 = output2.index(max(output2))

    #         if decision2 == 1:
    #             self.move_paddle(left=False, up=True)
    #         elif decision2 == 2:
    #             self.move_paddle(left=False, up=False)

    #         self.update()

    #     return self.left_hits, self.right_hits

    # def calculate_fitness(self, genome1, genome2):
    #     genome1.fitness += self.left_hits
    #     genome2.fitness += self.right_hits

    # def test_ai(self, net, config):
    #     self.start()
    #     for _ in range(1000):
    #         # AI paddle movement based on neural network output
    #         output = net.activate((self.paddle2_position, abs(self.width - self.ball_position[0]), self.ball_position[1]))
    #         decision = output.index(max(output))

    #         if decision == 0:
    #             self.move_paddle(left=False, up=True)
    #         elif decision == 1:
    #             self.move_paddle(left=False, up=False)

    #         self.update()

    #     return self.get_state()
