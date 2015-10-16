__author__ = 'li'

from random import choice
import gc
from SmartLearning.smartlearn import LearnSDN

# Define number of hidden nodes per layer with a list.
# For instance, [20, 10] means 2 hidden layers: the first with 20 nodes and the second with 10 nodes.
number_hidden_nodes_per_layer = [20, 20]
# Define type of activation function:
# 0 for logistic, 1 for tanh, 2 for soft plus, 3 for rectified linear unit and 4 for identity.
activation_function_type = 0
# Define exploration type. 0 for fixed epsilon and 1 for varying epsilon.
exploration_type = 1
# Define learning method. 0 for Q-learning, and 1 for R-learning.
learning_method = 0
# Define exploration probability from 0 to 1.
epsilon = 0.05
# Define learning rate from 0 to 1.
alpha = 0.1
# Define discount factor from 0 to 1.
gamma = 0.9
# Define learning parameter for average reward in R-learning.
beta = 0.1
# Define learning rate of neural network.
learning_rate = 0.3


class Allocator(object):
    def __init__(self):
        self.topo.numOfCores = 2
        self.topo.numOfToRs = 4
        self.topo.numOfServers = 4
        self.QLearner = LearnSDN(self.topo.numOfCores, self.topo.numOfToRs, self.topo.numOfToRs,
                                 2 * self.topo.numOfToRs * self.topo.numOfCores,
                                 number_hidden_nodes_per_layer, activation_function_type, exploration_type,
                                 epsilon, alpha, gamma, beta, learning_rate, learning_method)

    def select_action(self, state, source_ip, destination_ip):
        return self.QLearner.select_action(state, source_ip, destination_ip)

    def update(self, previous_state, source_ip, destination_ip, previous_action, current_state, reward):
        return self.QLearner.update(previous_state, source_ip, destination_ip, previous_action, current_state, reward)

    def placeFlow(self, fid, paths, flowdb):
        action = self.findPath(fid, paths, flowdb)
        path = self.convert_to_core(action)
        flowdb.setPath(fid, path)
        return flowdb

    def findPath(self, paths, flowdb):
        return self.select_action()

    def placeAllCoflows(self, paths, flowdb):
        cids = flowdb.getAllCoflow()
        for c in cids:
            coflow = flowdb.getAllInCoflow(c)
            pathCount = dict(zip(paths, len(paths) * [0]))
            for f in coflow:
                path = self.findPath(paths, flowdb)
                pathCount[path] += 1
            mostChosenPath = max(pathCount, key=pathCount.get)
            for f in coflow:
                return self.placeFlow(f['id'], mostChosenPath, flowdb)

    def genCandidatePaths(self, paths, flowdb):
        # use q learning to generate candidate paths
        # interface with RL module
        # TODO: add RL support. NOTE: there is also a pathing function in Controller.py
        return paths

    def convert_to_core(self, action):
        if action == 0:
            return "192.168.1.208"
        if action == 1:
            return "192.168.1.209"
        print "error"
