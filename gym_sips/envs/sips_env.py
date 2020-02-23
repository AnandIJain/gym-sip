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

from sips.h import helpers as h
from sips.h import serialize as s
from sips.h import fileio as fio
from sips.h import calc

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

def get_data_quick(df):
    s = df[ENV_COLS]
    x = s.replace({'None': np.nan, 'EVEN': 100})
    x = x.dropna()
    bb = x[x.sport == 'BASK'].copy()
    gs = h.chunk(bb)
    games =[]
    for g in gs:
        g.last_mod = g.last_mod - g.last_mod.iloc[0]
        g.drop(['game_id', 'sport'], axis=1, inplace=True)
        g = g.astype(np.float32)
        games.append(g)
    return games
    



class SipsEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.game_idx = -1  # gets incr to 0 on init
        # dfs = h.apply_min_then_filter(dfs, verbose=True)

        self.dfs = get_data_quick(pd.concat(h.get_dfs()))
        self.last_game_idx = len(self.dfs) - 1
        self.action_space = spaces.Discrete(3)  # buy_a, buy_h, hold
        self.reset()
        self.observation_space = get_obs_size(self.data)

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
            return self.tally_reward(obs), True
        if act == BUY_A:
            reward -= 1
            self.a_bets.append(int(obs.a_ml))
        elif act == BUY_H:
            reward -= 1
            self.h_bets.append(int(obs.h_ml))
        return reward, False

    def tally_reward(self, obs):

        num_bets = len(self.a_bets) + len(self.h_bets)
        if obs.a_pts == obs.h_pts:
            print(f"tied game")  # {obs.a_team} tied with {obs.h_team}")
            reward = num_bets
            net = -1 * num_bets
        elif obs.a_pts < obs.h_pts:
            reward = sum(list(map(calc.eq, self.a_bets)))
            net = reward - num_bets
        else:
            reward = sum(list(map(calc.eq, self.h_bets)))
            net = reward - num_bets

        print(f"net: {net}")
        return reward

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
        return


def get_obs_size(df):
    # state_size = (1, df.shape[0])
    return spaces.Box(-np.inf, np.inf, [df.shape[1]])


if __name__ == "__main__":
    env = SipsEnv()
    print(env.dfs)
    print(len(env.dfs))
