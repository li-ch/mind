import numpy as np
import MDP
import requests
import json

class RL:
    def __init__(self,mdp,sampleReward):
        '''Constructor for the RL class

        Inputs:
        mdp -- Markov decision process (T, R, discount)
        sampleReward -- Function to sample rewards (e.g., bernoulli, Gaussian).
        This function takes one argument: the mean of the distributon and 
        returns a sample from the distribution.
        '''

        self.mdp = mdp
        self.sampleReward = sampleReward
        self.eventID = -1
        self.events = np.empty(0)
        self.sFlowURL = 'http://localhost:8008'
        self.floodLightURL = 'http://localhost:8080'

    def sampleRewardAndNextState(self,state,action):
        '''Procedure to sample a reward and the next state
        reward ~ Pr(r)
        nextState ~ Pr(s'|s,a)

        Inputs:
        state -- current state
        action -- action to be executed

        Outputs: 
        reward -- sampled reward
        nextState -- sampled next state
        '''

        reward = self.sampleReward(self.mdp.R[action,state])
        #cumProb = np.cumsum(self.mdp.T[action,state,:])
        #nextState = np.where(cumProb >= np.random.rand(1))[0][0]

        while len(self.events) == 0:
            r = requests.get(self.sFlowURL + '/events/json?maxEvents=1000&timeout=60&eventID=' + str(self.eventID))
            if r.status_code != 200: break
            events = r.json()
        self.eventID = self.events[0]["eventID"]
        e = self.events[0]
        self.events = self.events[1:]
        if 'incoming' == e['metric']:
            r = requests.get(self.sFlowURL + '/metric/' + e['agent'] + '/' + e['dataSource'] + '.' + e['metric'] + '/json')
            metric = r.json()
        if len(metric) > 0:
            ippair=metric[0]["topKeys"][0]["key"]
            ippair=ippair.split(',')
        srcip = int(ippair[0].split('.')[-1])
        dstip = int(ippair[1].split('.')[-1])
        nextState = srcip*2 + dstip

        return [reward,nextState]

    def qLearning(self,s0,initialQ,nEpisodes,nSteps,epsilon=0,temperature=0):
        '''qLearning algorithm.  Epsilon exploration and Boltzmann exploration
        are combined in one procedure by sampling a random action with 
        probabilty epsilon and performing Boltzmann exploration otherwise.  
        When epsilon and temperature are set to 0, there is no exploration.

        Inputs:
        s0 -- initial state
        initialQ -- initial Q function (|A|x|S| array)
        nEpisodes -- # of episodes (one episode consists of a trajectory of nSteps that starts in s0
        nSteps -- # of steps per episode
        epsilon -- probability with which an action is chosen at random
        temperature -- parameter that regulates Boltzmann exploration

        Outputs: 
        Q -- final Q function (|A|x|S| array)
        policy -- final policy
        '''

        Q = initialQ
        cumActProb = np.cumsum(np.ones(self.mdp.nActions)/self.mdp.nActions)
        sFreq = np.zeros(self.mdp.nStates)
        for episId in xrange(nEpisodes):
            state = s0
            for iterId in xrange(nSteps):
                sFreq[state] += 1
                alpha = 1/sFreq[state]

                # choose action
                if epsilon > np.random.rand(1):
                    action = np.where(cumActProb >= np.random.rand(1))[0][0]
                else: 
                    if temperature == 0:
                        action = Q[:,state].argmax(0)
                    else:
                        boltzmannVal = exp(Q[:,state]/temperature)
                        boltzmannProb = boltzmannVal / boltzmannVal.sum()
                        cumBoltzmannProb = np.cumsum(boltzmannProb)
                        action = np.where(cumBoltzmannProb >= np.random.rand(1))[0][0]

                # sample reward and next state
                [reward,nextState]=self.sampleRewardAndNextState(state,action)

                # update Q value
                Q[action,state] += alpha * (reward + self.mdp.discount * Q[:,nextState].max() - Q[action,state])
                state = nextState

        policy = Q.argmax(0)
        return [Q,policy]    

    def modelBasedActiveRL(self,s0,defaultT,initialR,nEpisodes,nSteps,epsilon=0):
        '''Model-based Active Reinforcement Learning with epsilon greedy 
        exploration

        Inputs:
        s0 -- initial state
        defaultT -- default transition function when a state-action pair has not been vsited
        initialR -- initial estimate of the reward function
        nEpisodes -- # of episodes (one episode consists of a trajectory of nSteps that starts in s0
        nSteps -- # of steps per episode
        epsilon -- probability with which an action is chosen at random

        Outputs: 
        V -- final value function
        policy -- final policy
        '''

        cumActProb = np.cumsum(np.ones(self.mdp.nActions)/self.mdp.nActions)
        freq = np.zeros([self.mdp.nActions,self.mdp.nStates,self.mdp.nStates])
        T = defaultT
        R = initialR
        model = MDP.MDP(T,R,self.mdp.discount)
        [policy,V,_] = model.policyIteration(np.zeros(model.nStates,int))
        for episId in xrange(nEpisodes):
            state = s0
            for iterId in xrange(nSteps):

                # choose action
                if epsilon > np.random.rand(1):
                    action = np.where(cumActProb >= np.random.rand(1))[0][0]
                else: 
                    action = policy[state] 

                srcip = '10.0.0.'+str(state/2)
                dstip = '10.0.0.'+str(state%2)
                elephant = {'src-ip':srcip,'dst-ip':dstip,'action':'enqueue='+str(action+1)+':1'}
                r = requests.put(self.floodLightURL + '/wm/staticflowpusher/json',data=json.dumps(elephant))


                # sample reward and next state
                [reward,nextState]=self.sampleRewardAndNextState(state,action)

                # update counts
                freq[action,state,nextState] += 1
                asFreq = freq[action,state,:].sum()

                # update transition
                T[action,state,:] = freq[action,state,:]/asFreq

                # update reward
                R[action,state] = (reward + (asFreq-1)*R[action,state])/asFreq

                # update policy
                [policy,V,_] = model.policyIteration(policy)

                state = nextState
        return [V,policy]    
