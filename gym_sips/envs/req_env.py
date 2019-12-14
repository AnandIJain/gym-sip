"""
TODO:
    - on reset, acquire general market data,
    - for game in sport_df, make action on whether to request the new data or not.
    - make request anyways to accurately return reward


"""
import random

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pandas as pd
import numpy as np

from sips.lines.bov import bov
from sips.h import helpers as h
from sips.h import serialize as s
from sips.h import fileio as fio
from sips.h import calc

from sips.macros import bov as bm
from sips.macros import tfm

# Macros for actions
MAKE_REQUEST = 0
SKIP_REQUEST = 1


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


class ReqEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, sports=["nba"]):
        self.sports = sports

        self.action_space = spaces.Discrete(3)

        self.reset()

        self.observation_space = get_obs_size(self.data)

    def step(self, action):

        reward, done = self.act(obs, action)
        
        info = [obs.a_ml, obs.h_ml]

        self.step_counter += 1
        self.counter += 1
        if self.counter == 
        return obs, reward, done, info

    def act(self, obs, act):
        """
        obs (pd.Series)
        act (int)
        """
        reward = 0.0


        return reward, False

    def reset(self):
        df = bov.lines(self.sports, output='dict')
        self.data_dict = s.serialize_df(
            df, in_cols=ENV_COLS, to_numpy=False, astype=np.float32
        )
        self.number_of_games = len()
        self.step_counter = 0
        self.game_ids = self.data_dict.keys()
        self.current_game = 0
        self.data = list(self.data_dict.values())


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



