import random

class Robot(object):

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon0=0.5):

        self.maze = maze
        self.valid_actions = self.maze.valid_actions
        self.state = None
        self.action = None

        # Set Parameters of the Learning Robot
        self.alpha = alpha
        self.gamma = gamma

        self.epsilon0 = epsilon0
        self.epsilon = epsilon0
        self.t = 0

        self.Qtable = {}
        self.reset()

    def reset(self):
        """
        Reset the robot
        """
        self.state = self.sense_state()
        self.create_Qtable_line(self.state)

    def set_status(self, learning=False, testing=False):
        """
        Determine whether the robot is learning its q table, or
        exceuting the testing procedure.
        """
        self.learning = learning
        self.testing = testing

    def update_parameter(self):
        """
        Some of the paramters of the q learning robot can be altered,
        update these parameters when necessary.
        """
        if self.testing:
            # TODO 1. No random choice when testing
            self.epsilon = 0
        else:
            # TODO 2. Update parameters when learning
            self.epsilon = self.epsilon*0.9

        return self.epsilon

    def sense_state(self):
        """
        Get the current state of the robot. In this
        """

        # TODO 3. Return robot's current state 
        return self.maze.sense_robot()

    def create_Qtable_line(self, state):
        """
        Create the qtable with the current state
        """
        # TODO 4. Create qtable with current state
        # Our qtable should be a two level dict,
        # Qtable[state] ={'u':xx, 'd':xx, ...}
        # If Qtable[state] already exits, then do
        # not change it.
        if state not in self.Qtable:
            self.Qtable[state] = {'u':0.0, 'd':0.0,'l':0.0,'r':0.0}
        else:
            pass
        

    def choose_action(self):
        """
        Return an action according to given rules
        """
        def is_random_exploration():

            # TODO 5. Return whether do random choice
            # hint: generate a random number, and compare
            # it with epsilon
            
            #random_rate = random.uniform(0,1)
            # action = None
            if random.uniform(0,1) < self.epsilon: # 以某一概率
                return 1 
            else:
                return 0
            #    action = random.choice(actions) # 实现对动作的随机选择
            #else: 
            #    action = max(qline, key=qline.get) # 否则选择具有最大 Q 值的动作
            #pass
        

        if self.learning:
            if is_random_exploration():
                # TODO 6. Return random choose aciton
                return random.choice(self.valid_actions)
            else:
                # TODO 7. Return action with highest q value
                return max(self.Qtable[self.state], key=self.Qtable[self.state].get)
        elif self.testing:
            # TODO 7. choose action with highest q value
            return max(self.Qtable[self.state], key=self.Qtable[self.state].get)
        else:
            # TODO 6. Return random choose aciton
            return random.choice(self.valid_actions)

    def update_Qtable(self, r, action, next_state):
        """
        Update the qtable according to the given rule.
        """
        if self.learning:
            
            # TODO 8. When learning, update the q table according
            # to the given rules
            
            #这里应当是公式的实现
            #q(s_{t},a) = (1-alpha) * q(s_{t},a) + alpha * (R_{t+1} + gamma * max_a q(a,s_{t+1}))
            
            self.Qtable[self.state][action] = ( 1 - self.alpha ) * (self.Qtable[self.state][action]) + ( self.alpha * ( r + self.gamma * float(max(self.Qtable[next_state].values())) ) )
            pass
            

    def update(self):
        """
        Describle the procedure what to do when update the robot.
        Called every time in every epoch in training or testing.
        Return current action and reward.
        """
        self.state = self.sense_state() # Get the current state
        self.create_Qtable_line(self.state) # For the state, create q table line 为当前的位置创建q table，包含了当前状态要去的下一个状态以及对应的q值

        #随机选一个动作，然后计算按照动作移动之后的奖励
        action = self.choose_action() # choose action for this state
        reward = self.maze.move_robot(action) # move robot for given action

        #得到移动之后的状态值，然后更新对应状态值的 qtable，qtable中没有这个状态值就去创建它，有这个状态值 就跳过
        next_state = self.sense_state() # get next state
        self.create_Qtable_line(next_state) # create q table line for next state

        #当前的过程是学习而不是测试，转入到学习状态中，按照公式提供的方法去更新qtable
        if self.learning and not self.testing:
            self.update_Qtable(reward, action, next_state) # update q table
            self.update_parameter() # update parameters

        return action, reward
