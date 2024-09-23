import os
import neat
import pickle
from django.http import JsonResponse, HttpResponse
from game_api.pong_game import PongGame

def train_ai_view(request):
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config.txt')

	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_path)

	winner = run_neat(config)

	return JsonResponse({"message": "AI Training complete", "winner_fitness": winner.fitness})

def run_neat(config):
	p = neat.Population(config)
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(1))

	winner = p.run(eval_genomes, 50)

	with open("best.pickle", "wb") as f:
		pickle.dump(winner, f)

	return winner

def eval_genomes(genomes, config):
	width, height = 1000, 500

	for i, (genome_id1, genome1) in enumerate(genomes):
		if i == len(genomes) - 1:
			break
		genome1.fitness = 0
		for genome_id2, genome2 in genomes[i+1:]:
			genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
			game = PongGame(width, height)
			left_hits, right_hits = game.train_ai(genome1, genome2, config)
			game.calculate_fitness(genome1, genome2)



def test_ai_view(request):
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config.txt')

	# Load the NEAT configuration
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_path)

	# Load the trained AI (best genome)
	try:
		with open("best.pickle", "rb") as f:
			winner = pickle.load(f)
	except FileNotFoundError:
		return HttpResponse("No trained AI found. Please train the AI first.", status=404)

	# Create a neural network from the best genome
	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

	# Initialize the game and test the AI
	game = PongGame()
	game_state = game.test_ai(winner_net, config)

	return JsonResponse({
		"message": "AI tested successfully.",
		"final_state": game_state
	})