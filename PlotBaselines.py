import matplotlib.pyplot as plt
import sys, pandas

# file_baseline = sys.argv[1]
file_ucb = sys.argv[1]
simulations = int(sys.argv[2])
# col_names = ["date","clicks","time","reward"]
col_names = ["date","version1","version2","version3","version4","version5","version6","version7","version8","clicks","time","reward","std_dev"]
# data_baseline = pandas.read_csv(file_baseline, names=col_names)
data_ucb = pandas.read_csv(file_ucb, names=col_names)

# rewards_baseline = data_baseline.reward.tolist()
rewards_ucb = map(float, data_ucb.reward.tolist()[1:])
stddev_ucb = map(float, data_ucb.std_dev.tolist()[1:])
v1 = map(float, data_ucb.version1.tolist()[1:])
v2 = map(float, data_ucb.version2.tolist()[1:])
v3 = map(float, data_ucb.version3.tolist()[1:])
v4 = map(float, data_ucb.version4.tolist()[1:])
v5 = map(float, data_ucb.version5.tolist()[1:])
v6 = map(float, data_ucb.version6.tolist()[1:])
v7 = map(float, data_ucb.version7.tolist()[1:])
v8 = map(float, data_ucb.version8.tolist()[1:])
# print rewards_ucb
# print stddev_ucb

plt.plot([i*200 for i in range(simulations)], v1)
plt.plot([i*200 for i in range(simulations)], v2)
plt.plot([i*200 for i in range(simulations)], v3)
plt.plot([i*200 for i in range(simulations)], v4)
plt.plot([i*200 for i in range(simulations)], v5)
plt.plot([i*200 for i in range(simulations)], v6)
plt.plot([i*200 for i in range(simulations)], v7)
plt.plot([i*200 for i in range(simulations)], v8)
# plt.errorbar([i*200 for i in range(simulations)], rewards_ucb, [s/2.0 for s in stddev_ucb], linestyle='None', marker='^')
# plt.axis([0, (simulations-1)*200, 0.3, 0.7])
plt.axis([0, (simulations-1)*200, 0, 100])
# plt.legend(['Baseline', 'Optimised'], loc='lower right')
plt.legend(['Version1', 'Version2', 'Version3', 'Version4', 'Version5', 'Version6', 'Version7', 'Version8'], loc='upper left')
plt.title('Baseline Simulation - Worst Version')
plt.xlabel('Visits')
plt.ylabel('Aggregate reward')
plt.margins(0.5)
plt.show()