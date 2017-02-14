import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        # Add following class parameters to optimization control
        self.optimized = False

        # Track the total number of training trials, for an optimized epsilon decay
        self.trial_cnt = 0


    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0

        if testing:
            self.epsilon = 0.0
            self.alpha = 0.0
        else:
            # training vs. testing
            if self.optimized:
                # optimized epsilon decay
                self.trial_cnt += 1
                self.epsilon = 1.0 / self.trial_cnt
            else:
                # default linear decay
                if self.epsilon >= 0.05:
                    self.epsilon -= 0.05

        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        if self.optimized:
            #
            # Observation: Smartcab's action is NOT relevant to its `right` vehicle at cross (according traffic rule):
            #   - If `light is GREEN`, agent's `right` side vehicle must be in STOP so not interference with Smartcab
            #   - If `light is RED`, agent can only turn `right`, so its `right` side vehicle would only be a concern if it's in U-Turn
            #   - U-Turn is not a valid action in the problem
            # N.B. I have used some environment dynamics to compress the agent state in this case, to the benefit of training viability
            #   Strictly speaking, it is not a pure model-free approach, but it seems appropriate to this project.
            #
            # Optimized Q-learning State Space size of  3x2x4x4=96, 4 times smaller
            state = (waypoint, inputs['light'], inputs['oncoming'], inputs['left'])
        else:
            # Initial Q-learning State Space size of 3x2x4x4x4=384
            state = (waypoint, inputs['light'], inputs['left'], inputs['right'], inputs['oncoming'])

        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state
        # N.B. I have refactored this function to return both max Q-value keys and maximum Q-value itself,
        #      to more efficient choose_action implementation.
        # Return: (maxAs, maxQ)
        #          maxAs: list of Q[state] action keys of maxQ
        #          maxQ:  maximum Q-value of a state  

        # slight refactor - return both argmax actions, and max Q-value of state
        maxAs = [k for k,v in self.Q[state].iteritems() if v == max(self.Q[state].values())]
        maxQ = self.Q[state][maxAs[0]]

        return (maxAs, maxQ) 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0

        if self.learning:
            if state not in self.Q.keys():
                # Add state to Q-table
                self.Q[state] = dict()

                for action in self.valid_actions:
                    # Init Q-value for new state
                    self.Q[state][action] = 0.0

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state

        if not self.learning:
            action = random.choice(self.valid_actions)
        else:
            dice = random.random()
            if dice <= self.epsilon:
                action = random.choice(self.valid_actions)
            else:
                actions, _ = self.get_maxQ(state)
                action = random.choice(actions)
 
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')

        if self.learning:
            self.Q[state][action] += self.alpha * (reward - self.Q[state][action])

        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent, learning=True)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=0.01, log_metrics=True, optimized=True)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0

    # default tolerance, used for default Q-learning Agent
    threshold = 0.05
    num_tests = 10

    # instruct Q-learning agent optimized vs. default
    if sim.optimized:
        agent.optimized = True
        # Recall we have 96 states in Optimized Q-learning Agent, best to keep
        # total training trials > 500, since epsilon=1/t we have: 
        threshold = 0.001
        num_tests = 100

    sim.run(n_test=num_tests, tolerance=threshold)

if __name__ == '__main__':
    run()
