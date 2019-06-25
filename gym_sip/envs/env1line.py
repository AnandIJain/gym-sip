
import gym

class env1(gym.Env):

	def __init__(self, df):
		self.df = df
		self.money = AUM
		self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)
		#observation space is a 1 by xcolumns shape thing need to define here later

	def next(self):
		self.cur_state = self.df.iloc[self.index, 0:]
        self.index += 1


    def step(self, action):
    	self.action = action
    	obs = self.next()
    	reward = self.act()
    	return obs, reward, done

    def act():
    	action_type = action[0]
    	amount = action[1]
    	#need a function for calculating profit based on whether the team we took won or not