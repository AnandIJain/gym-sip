"""
load tf datasets from sips
start with no teams, but one hots for status.

reset on game end

"""
import random

import gym
import numpy as np
import pandas as pd
from gym import error, spaces, utils
from gym.utils import seeding

from sips.h import calc
from sips.h import fileio as fio
from sips.h import helpers as h
from sips.h import serialize as s
from sips.macros import bov as bm
from sips.macros import tfm

# Macros for actions
BUY_A = 0
BUY_H = 1
SKIP = 2


ENV_COLS = [
    "sport",
    "game_id",
    # "a_team",
    # "h_team",
    "last_mod",
    "num_markets",
    "live",
    "quarter",
    "secs",
    "a_pts",
    "h_pts",
    "a_ml",
    "h_ml",
    "a_tot",
]


class SipsEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    # todo fix last_n and windowing

    def __init__(self, last_n = 1):
        self.last_n = last_n
        self.game_idx = -1  # gets incr to 0 on init
        df = h.all_lines()
        self.dfs = h.get_games_parsed(df, ENV_COLS)
        self.last_game_idx = len(self.dfs) - 1
        self.reset()
        self.action_space = spaces.Discrete(3)  # buy_a, buy_h, hold
        self.observation_space = get_obs_size(self.data, last_n=last_n)

    def step(self, action):
        self.row_idx += 1

        if self.row_idx > self.last_row_idx:
            return None, 0, True, None

        obs = self.data.iloc[self.row_idx]

        reward, done = self.act(obs, action)
        info = [obs.a_ml, obs.h_ml]
        return np.array(obs), reward, done, info

    def act(self, obs, act):
        """
        obs (pd.Series)
        act (int)
        """
        reward = 0.0
        if self.row_idx == self.last_row_idx:
            return tally_reward(obs, self.a_bets, self.h_bets), True
        if act == BUY_A:
            reward -= 1
            self.a_bets.append(int(obs.a_ml))
        elif act == BUY_H:
            reward -= 1
            self.h_bets.append(int(obs.h_ml))
        return reward, False


    def reset(self):
        self.a_bets = []
        self.h_bets = []
        self.game_idx += 1
        if self.game_idx == self.last_game_idx:
            self.close()

        try:
            self.data = self.dfs[self.game_idx]
        except IndexError:
            self.close()

        # print(f"game_data shape: {self.data.shape}")
        self.last_row_idx = self.data.shape[0] - 1
        self.row_idx = -1
        g = self.data
        return np.array(g.iloc[0])


    def render(self, mode="human"):
        pass

    def close(self):
        print("ran thru all games")
        self.game_idx = -1



def tally_reward(obs, a_bets, h_bets):

    num_bets = len(a_bets) + len(h_bets)
    if obs.a_pts == obs.h_pts:
        print(f"tied game")  # {obs.a_team} tied with {obs.h_team}")
        reward = num_bets
        net = -1 * num_bets
    elif obs.a_pts < obs.h_pts:
        reward = sum(list(map(calc.eq, a_bets)))
        net = reward - num_bets
    else:
        reward = sum(list(map(calc.eq, h_bets)))
        net = reward - num_bets

    print(f"net: {net} reward: {reward}")
    return reward

def get_obs_size(df, last_n=1):
    # state_size = (1, df.shape[0])
    return spaces.Box(-np.inf, np.inf, [df.shape[1] * last_n])


if __name__ == "__main__":
    env = SipsEnv()
    print(env.dfs)
    print(len(env.dfs))
