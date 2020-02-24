import random

import gym
import numpy as np
import pandas as pd
from gym import error, spaces, utils
from gym.utils import seeding

from sips.h import calc
from sips.h import helpers as h

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

class ContEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.epoch = -1
        self.min_action = 0
        self.max_action = 10.0
        self.game_idx = -1  # gets incr to 0 on init

        df = h.all_lines()
        self.dfs = h.get_games_parsed(df, ENV_COLS)
        self.action_space = spaces.Box(low=self.min_action, high=self.max_action,
                                        shape=(2,), dtype=np.float32)  # buy_a, buy_h
        self.observation_space = spaces.Box(-np.inf, np.inf, [self.dfs[0].shape[1]])
        self.last_game_idx = len(self.dfs) - 1
        self.reset()

    def step(self, action):
        self.row_idx += 1
        if self.row_idx > self.last_row_idx:
            return None, 0, True, None

        obs = self.data.iloc[self.row_idx]
        info = [obs.a_ml, obs.h_ml]

        if action[0] < 0 or action[1] < 0:
            reward, done = -1000, True
        else:
            reward, done = self.act(obs, action)

        return np.array(obs), reward, done, info

    def act(self, obs, action):
        """
        obs (pd.Series)
        action (int)
        """
        reward = 0.0
        if self.row_idx == self.last_row_idx:
            net = tally_reward(obs, self.a_bets, self.a_amts,
                               self.h_bets, self.h_amts)
            df = actions_to_df(a_bets, h_amts, h_bets, h_amts)
            return net, True

        self.a_bets.append(calc.eq(obs.a_ml))
        self.a_amts.append(action[0])
        self.h_bets.append(calc.eq(obs.h_ml))
        self.h_amts.append(action[1])
        reward = -1 * sum(action)
        # reward = 0
        return reward, False

    def reset(self):
        self.a_bets = []
        self.a_amts = []
        self.h_bets = []
        self.h_amts = []
        self.game_idx += 1
        self.epoch += 1
        print(f'game_id: {self.game_idx}')
        if self.game_idx == self.last_game_idx:
            self.game_idx = 0
        self.data = self.dfs[self.game_idx]
            
        # print(f"game_data shape: {self.data.shape}")
        self.last_row_idx = self.data.shape[0] - 1
        self.row_idx = -1
        return np.array(self.data.iloc[0])

    def render(self, mode='human'):
        pass

    def close(self):
        print(f"ran thru all games {self.game_idx}")
        self.game_idx = -1


def tally_reward(obs, a_bets, a_amts, h_bets, h_amts):

    num_bets = len(a_bets) + len(h_bets)
    if obs.a_pts == obs.h_pts:
        print(f"tied game")  # {obs.a_team} tied with {obs.h_team}")
        reward = 0
        net = 0
        a_win = False
    elif obs.a_pts > obs.h_pts:
        reward = sum([amt * eq for amt, eq in zip(a_bets, a_amts)])
        net = reward - sum(h_amts)
        a_win = True
    else:
        reward = sum([amt * eq for amt, eq in zip(h_bets, h_amts)])
        net = reward - sum(a_amts)
        a_win = False

    print(f"net: {net} reward: {reward} sum(a): {sum(a_amts)} sum(h): {sum(h_amts)} a_win: {a_win}")
    return reward

def actions_to_df(a_bets, a_amts, h_bets, h_amts):
    a_odds = list(map(calc.eq_to_odd, a_bets))
    h_odds = list(map(calc.eq_to_odd, h_bets))

    d = {'a_ml': a_odds, 'a_amt': a_amts,
            'h_ml': h_odds, 'h_amt':  h_amts}
    df = pd.DataFrame(data=d)
    # df.to_csv(str(epoch) + '.csv')
    print(df)
    return df

if __name__ == "__main__":
    env = ContEnv()
    # print(env.dfs)
    print(len(env.dfs))
    act = np.array([0.3, 0.8])
    d = False
    while not d:
        o, r, d, i = env.step(act)
        print(o)
        print(r)
    print(o)
