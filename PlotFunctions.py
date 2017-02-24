import matplotlib.pyplot as plt

def plotResults(simulations, horizon, sim_file):
	with open(sim_file) as f:
		for line in f:
			percentages = [float(num) for num in line.split()]
			# percentages = reduce_list(percentages, 10)
			plt.plot([i for i in range(simulations)], percentages)
		plt.axis([0, simulations, 0, 1])
		plt.legend(['e = 0.1', 'e = 0.2', 'e = 0.3', 'e = 0.4'], loc='lower right')
		plt.xlabel('Simulations')
		plt.ylabel('Average reward')
		plt.show()

plotResults(100, 50, "simulation.txt")