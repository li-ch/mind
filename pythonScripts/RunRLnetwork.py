import numpy as np
import MDP
import RLnetwork
import requests
import json

groups = {'external':['0.0.0.0/0'],'internal':['10.0.0.0/8']}
flows = {'keys':'ipsource,ipdestination','value':'frames','filter':'sourcegroup=external&destinationgroup=internal'}
threshold = {'metric':'incoming','value':1000}
sFlowURL = 'http://localhost:8008'

#define address internal and external address groups
r = requests.put(sFlowURL + '/group/json',data=json.dumps(groups))
#define flows
r = requests.put(sFlowURL + '/flow/incoming/json',data=json.dumps(flows))
#define thresholds (1000 pkt per sec)
r = requests.put(sFlowURL + '/threshold/incoming/json',data=json.dumps(threshold))


''' Construct simple network of N hosts and M switches such that each host is connected to each switch, but hosts are not directly connected and switches are not directly connected. Hence, there are NxN source/destination pairs and exactly M paths between each source/destination pair. Each source/destination pair is a state and each path is an action. For this simple network we assume that traffic is generated in such a way that the next flow will be for the same source destination pair as the previous flow with probability 0.5 and some other source/destination pair with uniform distribution. The reward function consists of the number of flows that terminates in a time step.  Since this is difficult to simulate without a proper simulator, we use arbitrary rewards for now. 
'''
# number of hosts
N = 2
# number of switches
M = 2
# transition function
T = np.ones((M,N*N,N*N),float)
for actId in xrange(M):
    T[actId,:,:] += N*N*np.identity(N*N)
T /= T.sum(axis=2).reshape(M,N*N,1)
# reward function
np.random.seed(0)
R = 10*np.random.rand(M,N*N)
np.random.seed()
discount = 0.95        
mdp = MDP.MDP(T,R,discount)
rlProblem = RLnetwork.RL(mdp,np.random.normal)

# Test Q-learning 
#[Q,policy] = rlProblem.qLearning(s0=0,initialQ=np.zeros([mdp.nActions,mdp.nStates]),nEpisodes=1,nSteps=100000,epsilon=0.3)
#print "\nQ-learning results"
#print Q
#print policy

# Test model-based active RL
[V,policy] = rlProblem.modelBasedActiveRL(s0=0,defaultT=np.ones([mdp.nActions,mdp.nStates,mdp.nStates])/mdp.nStates,initialR=np.zeros([mdp.nActions,mdp.nStates]),nEpisodes=1,nSteps=10,epsilon=0.3)
print "\nmodel-based active RL results"
print V
print policy

