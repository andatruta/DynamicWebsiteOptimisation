import matplotlib.pyplot as plt
import sys, pandas

file_baseline = sys.argv[1]
file_ucb = sys.argv[2]
simulations = int(sys.argv[3])
col_names = ["date","clicks","time","reward"]
data_baseline = pandas.read_csv(file_baseline, names=col_names)
data_ucb = pandas.read_csv(file_ucb, names=col_names)

rewards_baseline = data_baseline.reward.tolist()
rewards_ucb = data_ucb.reward.tolist()

plt.plot([i*200 for i in range(simulations)], rewards_baseline[1:])
plt.plot([i*200 for i in range(simulations)], rewards_ucb[0:])
plt.axis([0, (simulations-1)*200, 0.3, 0.7])
plt.legend(['Baseline', 'Optimised'], loc='lower right')
plt.title('Baseline Simulation - Worst Version')
plt.xlabel('Visits')
plt.ylabel('Aggregate reward')
plt.margins(0.5)
plt.show()