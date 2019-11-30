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
    "a_team",
    "h_team",
    "last_mod",
    "num_markets",
    "live",
    "quarter",
    "secs",
    "a_pts",
    "h_pts",
    "status",
    "a_ml",
    "h_ml",
    "a_tot",
]


class SipsEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, dfs=None):
        self.game_idx = -1  # gets incr to 0 on init

        if dfs is None:
            dfs = h.get_dfs()
            dfs = h.apply_min_then_filter(dfs, verbose=True)

        self.dfs = s.serialize_dfs(
            dfs, in_cols=ENV_COLS, to_numpy=False, astype=np.float32
        )
        self.last_game_idx = len(self.dfs) - 1
        self.action_space = spaces.Discrete(3)  # buy_a, buy_h, hold
        self.reset()
        self.observation_space = get_obs_size(self.data)

    def step(self, action):
        self.row_idx += 1

        if self.row_idx == self.last_row_idx:
            return None, 0, True, None

        obs = self.data.iloc[self.row_idx]
        reward, done = self.act(obs, action)
        info = [obs.a_ml, obs.h_ml]
        return obs, reward, done, info

    def act(self, obs, act):
        """
        obs (pd.Series)
        act (int)
        """
        reward = 0.0
        if obs.GAME_END:
            return self.tally_reward(obs), True
        if act == BUY_A:
            reward -= 1
            self.a_bets.append(int(obs.a_ml))
        elif act == BUY_H:
            reward -= 1
            self.h_bets.append(int(obs.h_ml))
        return reward, False

    def tally_reward(self, obs):

        if obs.a_pts == obs.h_pts:
            print(f"{obs.game_id}: {obs.a_team} tied with {obs.h_team}")
            profit = 0
        elif obs.a_pts < obs.h_pts:
            profit = sum(list(map(calc.eq, self.a_bets)))
        else:
            profit = sum(list(map(calc.eq, self.h_bets)))

        print(f'profit: {profit}')
        return profit

    def reset(self):
        self.a_bets = []
        self.h_bets = []
        self.game_idx += 1
        if self.game_idx == self.last_game_idx:
            self.close()
        self.data = self.dfs[self.game_idx]
        self.last_row_idx = len(self.data)
        self.row_idx = -1

    def render(self, mode="human"):
        pass

    def close(self):
        print("ran thru all games")
        return


def get_obs_size(df):
    state_size = (1, df.shape[0])
    return spaces.Box(-np.inf, np.inf, state_size)


if __name__ == "__main__":
    env = SipsEnv()
    print(env.dfs)
    print(len(env.dfs))
