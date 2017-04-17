import matplotlib.pyplot as plt

def plotResults(horizon, sim_file):
	with open(sim_file) as f:
		for line in f:
			percentages = [float(num) for num in line.split()]
			# percentages = reduce_list(percentages, 10)
			plt.plot([i for i in range(horizon)], percentages)
		plt.axis([0, horizon, 0, 1])
		plt.legend(['Annealed', 'Standard'], loc='upper right')
		plt.xlabel('Trials')
		plt.ylabel('Average reward')
		plt.title('Performance of annealed vs standard Softmax')
		plt.show()

plotResults(500, "simulation.txt")