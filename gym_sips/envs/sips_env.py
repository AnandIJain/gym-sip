"""
load tf datasets from sips
start with no teams, but one hots for status.

reset on game end

"""
import random

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pandas as pd
import numpy as np

import sips.h.helpers as h
import sips.h.serialize as s
import sips.h.fileio as fio
from sips.macros import tfm


class SipsEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.game_idx = -1  # gets incr to 0 on init

        self.dfs = h.get_dfs()
        self.last_game_idx = len(self.dfs) - 1
        self.action_space = spaces.Discrete(3)  # buy, sell, hold
        self.get_obs_size()

        self.reset()

    def step(self, action):
        reward = 0.0
        observation = self.data[self.row_idx]

        return observation, reward, done, info

    def reset(self):
        self.game_idx += 1
        if self.game_idx == self.last_game_idx:
            self.close()
        df = self.dfs[self.game_idx]
        self.get_game(df)
        self.row_idx = 0

    def get_obs_size(self):
        df = self.dfs
        self.get_game(df)
        state_size = len(self.data[0])
        self.observation_space = spaces.Box(-np.inf, np.inf, state_size)

    def get_game(self, df):
        self.data = np.array(s.serialize_df(df), dtype=np.float32)

    def render(self, mode="human"):
        pass

    def close(self):
        print("ran thru all games")
        return


if __name__ == "__main__":
    env = SipsEnv()
