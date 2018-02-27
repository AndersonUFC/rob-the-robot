import numpy as np
from random import random
import math

class Brain:
	def __init__(self, number_of_actions=0, number_of_features=0, gamma=0.99, n=0.01):
		self.number_of_actions = number_of_actions
		self.number_of_features = number_of_features
		self.probability = 1.
		self.gamma=gamma
		self.n = n
		self.action1 = 0
		self.action2 = 0
		self.Qvalue1 = 0
		self.Qvalue2 = 0
		self.Fvalue1 = 0
		self.Fvalue2 = 0

	def train(self, robot, labirint, system):
		collision = robot.map_actions(self.action1, labirint, system)
		robot.map_actions(4, labirint, system)

		reward = 0.


		# wall collision
		if collision:
			reward = -0.01


		# eat
		if robot.act_mouth.eated:
			reward = 1.

		self.Fvalue2 = self.sense(robot, labirint, system)
		self.action2, self.Qvalue2 = self.get_action(self.Fvalue2)
		delta = reward + self.gamma*self.Qvalue2 - self.Qvalue1

		for i in range(0, self.number_of_features+1):
			self.weights[self.action1][i] += self.n*delta*self.Fvalue1[i]
		
		for w in self.weights:
			print("						{}".format(w))
		print("						{}".format(self.Fvalue1))
		print("						{} | {}".format(self.Qvalue1,self.Qvalue2))
		
		self.Fvalue1 = self.Fvalue2
		self.Qvalue1 = self.Qvalue2
		self.action1 = self.action2

	def predict(self, robot, labirint, system):
		self.probability = 0.

		robot.map_actions(self.action1, labirint, system)
		robot.map_actions(4, labirint, system)

		self.Fvalue2 = self.sense(robot, labirint, system)
		self.action2, self.Qvalue2 = self.get_action(self.Fvalue2)

		print("						{}".format(self.Fvalue1))

		self.Fvalue1 = self.Fvalue2
		self.Qvalue1 = self.Qvalue2
		self.action1 = self.action2						

	def sense(self, robot, labirint, system):
		F1 = robot.sensor_fruit.sense(robot, labirint, system)
		F2 = robot.sensor_wall.sense(robot,labirint,system)

		if math.fabs(sum(F2)) > 0:
			for i in range(0, len(F1)):
				F1[i] = 0.
		

		F = [1.] + F1 + F2
		return F

	def set_weights(self, sense):
		if self.number_of_features == 0:
			self.number_of_features = len(sense)-1
		self.weights = np.random.random((self.number_of_actions, self.number_of_features+1))*0.01

	def observe(self, robot, labirint, system, reset_weights=True):
		self.Fvalue1 = self.sense(robot, labirint, system)
		if reset_weights:
			self.set_weights(self.Fvalue1)
		self.action1, self.Qvalue1 = self.get_action(self.Fvalue1)

	def get_action(self, sense):
		sense_np = np.array(sense)
		action = int(random()*100)%self.number_of_actions
		Q = np.dot(sense, self.weights[action])
		rand_prob = int(random()*1000)%100

		# random probability
		if rand_prob < self.probability:
			return action, Q

		# greedy action
		for a in range(0, 4):
			new_Q = np.dot(sense, self.weights[a])

			if new_Q > Q:
				Q = new_Q
				action = a

		return action, Q