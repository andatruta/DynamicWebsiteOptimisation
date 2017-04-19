import matplotlib.pyplot as plt

def plotResults(horizon, sim_file):
	with open(sim_file) as f:
		for line in f:
			percentages = [float(num) for num in line.split()]
			# percentages = reduce_list(percentages, 10)
			plt.plot([i for i in range(horizon)], percentages)
		plt.axis([0, horizon, 0, 1])
		plt.legend(['E-greedy', 'Softmax', 'UCB'], loc='upper right')
		plt.xlabel('Trials')
		plt.ylabel('Probability of choosing the best arm')
		plt.title('Accuracy of different bandit algorithm')
		plt.show()

# plotResults(500, "simulation.txt")
plotResults(500, "egreedy-softmax-ucb-accuracy-500x1000.txt")