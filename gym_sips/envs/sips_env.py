"""
load tf datasets from sips
start with no teams, but one hots for status.

reset on game end

"""

import gym
from gym import error, spaces, utils
from gym.utils import seeding




class SipsEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    pass

  def step(self, action):
    pass

  def reset(self):
    pass

  def render(self, mode='human'):
    pass

  def close(self):
    pass
