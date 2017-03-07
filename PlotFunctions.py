import matplotlib.pyplot as plt

def plotResults(simulations, horizon, sim_file):
	with open(sim_file) as f:
		for line in f:
			percentages = [float(num) for num in line.split()]
			# percentages = reduce_list(percentages, 10)
			plt.plot([i for i in range(simulations)], percentages)
		plt.axis([0, simulations, 0, 1.05])
		# plt.legend(['t = 0.1', 't = 0.2', 't = 0.3', 't = 0.4'], loc='lower right')
		plt.legend(['E-greedy', 'UCB'], loc='lower right')
		plt.title('Average reward of different algorithms: 18-armed bandit')
		plt.xlabel('Simulations')
		plt.ylabel('Average reward')
		plt.margins(0.5)
		plt.show()

plotResults(500, 50, "simulation.txt")