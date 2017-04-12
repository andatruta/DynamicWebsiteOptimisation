'use strict';

angular.module('app').constant('ALL_POSTS', [
	{
		'title' : 'Multi-objective multi-armed bandits',
		'thumbnail' : 'static/images/webdev.jpg',
		'descr': 'In real-life scenarios of website optimization, it is important to choose the right success metric that is most important for the business at hand.',
		'content': `
		In real-life scenarios of website optimization, it is important to choose the right success metric that is most important for the business at hand. 
		One potentially fatal source of increased complexity is that optimizing short-term click-through rates may destroy user retention in the long-term. <br /> <br />

		As such, I decided to modify my current bandit algorithm into a multi-objective one, that measures success based not only on simple <i>click-through rates</i>, 
		but also on the <i>time that users spend</i> on the website. These are both important metrics for my chosen market - the blogging industry.
		` 
	},
	{
		'title' : 'Upper Confidence Bound algorithm',
		'thumbnail' : 'static/images/webdev2.jpg',
		'descr': 'Both <i>Epsilon-Greedy</i> and <i>Softmax</i> have a systematic weakness: they do not account for how much they already know about any of the arms available.',
		'content': `
		Both <i>Epsilon-Greedy</i> and <i>Softmax</i> have a systematic weakness: they do not account for how much they already know about any of the arms available.
		This means that they will underexplore options that were not rewarding in the beginning, despite the fact that they do not have enough data to be confident about those arms.
		Therefore, we need an algorithm that pays attention not only to <i>what it knows</i> about the arms, but also <i>how much it knows</i>. <br /><br />

		The <i>Upper Confidence Bound</i> algorithm (UCB for short) does exactly that. It makes decisions to explore that are driven by out confidence in the estimated value of the arms 
		we've selected. This is important because the rewards we receive from the arms are rather noisy in nature. The estimated value of any arm is only a noisy estimate of the true return
		we can expect from it. Because of this, it might be just a coincidence that arm A is better than B, and we might find that if we explored more B is actually better. UCB avoids this by requiring us to keep track of our confidence in our assessments of the estimated values of all of the arms. Our confidence metric will be based on how many times
		we've already seen a particular arm. <br /><br />

		UCB presents a couple more advantages over the previous two algorithms: <br />
		- It does not use randomness at all. <br />
		- It does not have any parameters that need to be configured. This is particularly import in my situation, because it means that the clients that will use this platform will not need to deal with any configuration settings. <br /><br />

		The following code snippet shows how UCB chooses which arm to choose: <br /><br />
		<code>
		def chooseArm(self): <br />
			n_versions = len(self.versions) <br />
			# ensure that each version was shown at least once <br />
			for v in range(n_versions): <br />
				if self.counts[v] == 0: <br />
					return v <br />
			<br />
			ucb = [0.0 for version in self.versions] <br />
			sum_counts = sum(self.counts) <br />
			# calculate special UCB values <br />
			for v in range(n_versions): <br />
				ucb[v] = self.actionValues[v] + math.sqrt((2 * math.log(sum_counts)) / float(self.counts[v])) <br />
			<br />
			# return version with maximum UCB value <br />
			return maxValue(ucb)
		</code>
		` 
	},
	{
		'title' : 'Softmax algorithm',
		'thumbnail' : 'static/images/egreedy_softmax_reward300.png',
		'descr': 'After experimenting with the <i>Epsilon-Greedy</i> algorithm, it becomes apparent that it has some problems: it explores options completely at random without any concern for their merits.',
		'content': `
		After experimenting with the <i>Epsilon-Greedy</i> algorithm, it becomes apparent that it has some problems: it explores options completely at random without any concern for their merits.
		For instance, say in Scenario A you have two arms, one of which rewards you 10% of the time and the other rewards you 13% of the time. In Scenario B, the two arms might reward you 10% and 99%
		of the time. In both of these scenarios, the probability that the <i>Epsilon-Greedy</i> explores the worse arm is exactly the same, despite the fact that, the worse arm in Scenario B is relatively
		much worse than the inferior arm in A. Therefore, we need to have more structured exploration rather than the almost random exploration that this algorithm provides.<br /><br />

		As such, I decided to implement a new algorithm called <i>Softmax</i>. This tries to cope with arms differing in estimated value by explicitly incorporating information about the reward rates
		of the available arms into its action-selection method. In a naive two arms (A and B) scenario, the algorithm would choose arm A with probability <i>rA / (rA + rB)</i> and arm B with probability  <i>rB / (rA + rB)</i>,
		where <i>rA</i> and <i>rB</i> are the success rates of the two arms. <br /><br />

		This algorithm also introduces a new parameter <i>tau</i>, called the temperature. This is essentially a scaling factor, and it based on an analogy with physics where at high temperatures systems then to 
		behave randomly, while at low temeperatures they have more structure. <br /><br />

		The following <i>Python</i> code snippet illustrates the implementation of the Softmax action-selection.<br /><br />

		<code>
		def chooseVersion(p): <br />
			r = rand.random() <br />
			cumulative_p = 0.0 <br />
			for i in range(len(p)): <br />
				p_i = p[i] <br />
				cumulative_p += p_i <br />
				if cumulative_p > r: <br />
					return i <br />
		<br /> <br />
		def getVersion(self): <br />
			nominator = sum([math.exp(v / self.temperature) for v in self.actionValues]) <br />
			probabilities = [math.exp(v / self.temperature) / nominator for v in self.actionValues] <br />
			v = chooseVersion(probabilities) <br />
			return v <br />
		</code>
		` 
	},
	{
		'title' : 'Variations on the exploration rate',
		'thumbnail' : 'static/images/epsilon_sim_25.png',
		'descr': 'In order to find out what the best trade-off between exploration and exploitation is, I decided to run some simulations on the Epsilon-Greedy algorithm with different values of <i>epsilon</i>.',
		'content': `
		In order to find out what the best trade-off between exploration and exploitation is, I decided to run some simulations on the Epsilon-Greedy algorithm with different values of <i>epsilon</i>. <br /><br />
		A simple approach to measuring the algorithm's performance is to use the average reward that the algorithm receives on each trial. This method of measuring performance is particularly suitable
		for scenarios when there are many arms similar to the best, each of which is just a little worse than the best. Website optimization is one of these scenarios, as usually no version is significantly better 
		than all others. <br /><br />

		As such, I ran the algorithm with values of <i>epsilon = [0.1, 0.2, 0.3]</i> for a relatively small number of trials on the same distribution of user preferences. A trial would get a reward of 1 if at least one user click occurred.
		The results are displayed in the graph presented. The curves on the graph are rather noisy due to the low number of trials that each simulation consisted of. Running the simulation for longer would have resulted in smoother curves.<br /> <br />

		Despite this, we can still gather that larger values of <i>epsilon</i> perform better in the sort term, however they do not learn as much over time. <i>Epsilon = 0.1</i> starts off worse, as it explores less in the beginning.
		However, as the algorithm accumulates sufficient knowledge about the arms, exploiting the best arm more often yields better results in the long term.
		` 
	},
	{
		'title' : 'Initial Epsilon-greedy algorithm',
		'thumbnail' : 'static/images/pic05.jpg',
		'descr': 'Epsilon-greedy is the simplest form of multi-armed bandit, its main feature being the fact that it alternates between exploration and exploitation at a constant exploration rate <i>epsilon</i>.',
		'content': `
		Epsilon-greedy is the simplest form of multi-armed bandit, its main feature being the fact that it alternates between exploration and exploitation at a constant exploration rate <i>epsilon</i>. <br />
		The Epsilon-greedy handles selecting an arm in two parts: <br /><br />
		- We flip a coin to see if we'll choose the best arm we know about <br />
		- Then, if the coin comes up tails, we'll select an arm completely at random. <br /><br />
		In the code implementation of this algorithm, I am checking if a randomly generated number is smaller than <i>1 - epsilon</i>. If so, the algorithm selects the arm with the current highest value. Otherwise,
		we select an arm completely at random. <br /><br />
		The following code snippet presents the <i>Python</i> implementation of the arm selection part of the algorithm: <br /><br />
		<code>
		def chooseArm(self): <br />
		&#9;if rand.random() < 1 - self.epsilon: <br />
			&#9;&#9;return self.greedyAction() <br />
		&#9;else: <br />
			&#9;&#9;return rand.randint(0, len(self.actionValues) - 1) <br />
		</code>
		`
	}
]);