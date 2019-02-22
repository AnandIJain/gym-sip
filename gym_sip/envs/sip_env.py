import gym
import random
import pandas as pd
import numpy as np
from gym import spaces
from sklearn.preprocessing import RobustScaler

ACTION_SKIP = 0
ACTION_BUY_A = 1
ACTION_BUY_H = 2


class SippyState:
    def __init__(self, game):
        self.game = game  # df for game
        print(game)
        self.id = self.game.iloc[0, 2]  # first row, second column
        self.index = 0

        print("Imported data from {}".format(self.id))

    def fit_data(self):
        transformer = RobustScaler().fit(self.game)
        transformer.transform(self.game)

    def reset(self):
        self.index = 0

    def next(self):
        if self.index >= len(self.game) - 1:
            return None, True

        values = self.game.iloc[self.index, 0:]
        # print(values)
        self.index += 1

        return values, False

    def shape(self):
        return self.game.shape

    def a_odds(self):
        return int(self.game.iloc[self.index, 9])

    def h_odds(self):
        return int(self.game.iloc[self.index, 10])

    def num_games(self):
        return len(self.game['game_id'].unique())


class SipEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, file_name):

        self.fn = 'data/' + file_name + '.csv'
        self.df = None

        self.headers = ['a_team', 'h_team', 'league', 'game_id',
                        'a_pts', 'h_pts', 'secs', 'status', 'a_win', 'h_win', 'last_mod_to_start',
                        'num_markets', 'a_odds_ml', 'h_odds_ml', 'a_hcap_tot', 'h_hcap_tot']
        self.dtypes = {
                    'a_team': 'category',
                    'h_team': 'category',
                    'league': 'category',
                    'game_id': 'Int64',
                    'a_pts': 'Int16',
                    'h_pts': 'Int16',
                    'secs': 'Int16',
                    'status': 'Int16',
                    'a_win': 'Int16',
                    'h_win': 'Int16',
                    'last_mod_to_start': 'Float64',
                    'num_markets': 'Int16',
                    'a_odds_ml': 'Int32',
                    'h_odds_ml': 'Int32',
                    'a_hcap_tot': 'Int32',
                    'h_hcap_tot': 'Int32'
        }
        self.read_csv()
        self.states = {}
        self.ids = []
        self.chunk_df()
        self.max_bets = 1  # MAX NUM OF HEDGED BETS. TOTAL BET COUNT = 2N

        self.bet_amt = 100
        self.money = 0  # DOESN'T MATTER IF IT RUNS OUT OF MONEY AND MAX BETS IS HELD CONSTANT
        self.bound = 16

        self.eq_a = 0
        self.eq_h = 0
        self.a_odds = 0
        self.h_odds = 0
        self.adj_a_odds = 0
        self.adj_h_odds = 0

        self.state = None

        self.observation_space = spaces.Box(low=--100000000., high=100000000., shape=(537, ))
        self.action_space = spaces.Discrete(3)

        if len(self.states) == 0:
            raise NameError('Invalid empty directory {}'.format(self.fn))

    def step(self, action):
        assert self.action_space.contains(action)

        portfolio = self.money + (self.eq_a * self.a_odds) + (self.eq_h * self.h_odds)
        price = self.a_odds + self.h_odds
        prev_portfolio = self.money + self.eq_a + self.eq_h

        self.actions(action)

        state, done = self.state.next()

        new_price = price
        if not done:
            self.get_odds()
            new_price = self.a_odds + self.h_odds

        reward = self.money + self.eq_a + self.eq_h - prev_portfolio

        return state, reward, done, None

    def read_csv(self):
        raw = pd.read_csv(self.fn, usecols=self.headers)
        raw = raw.dropna()
        raw = pd.get_dummies(data=raw, columns=['a_team', 'h_team', 'league'])

        self.df = raw.copy()

    def chunk_df(self):
        self.ids = self.df['game_id'].unique().tolist()
        self.states = {key: val for key, val in self.df.groupby('game_id')}

    def get_odds(self):
        self.a_odds = self.state.a_odds()
        self.h_odds = self.state.h_odds()
        self.adj_a_odds = eq_calc(self.a_odds)
        self.adj_h_odds = eq_calc(self.h_odds)

    def actions(self, action):
        if action == ACTION_BUY_A:
            if self.a_odds != 0:
                self.money -= self.bet_amt
                self.eq_a += self.adj_a_odds
            else:
                print(str(self.a_odds) + ' a')
        if action == ACTION_BUY_H:
            if self.h_odds != 0:
                self.money -= self.bet_amt
                self.eq_h += self.adj_h_odds
            else:
                print('forced skip')

    def reset(self):
        cur_id = random.choice(self.ids)
        self.state = SippyState(self.states[cur_id])

        self.money = 0
        self.eq_a = 0
        self.eq_h = 0

        state, done = self.state.next()
        return state

    def _render(self, mode='human', close=False):
        pass


def act_name(act):
    if act == 0:
        return 'SKIP'
    elif act == 1:
        return 'BUY AWAY'
    elif act == 2:
        return 'BUY HOME'


def eq_calc(odd):
    if odd == 0:
        return 0
    if odd >= 100:
        return odd/100.
    elif odd < 100:
        return abs(100/odd)