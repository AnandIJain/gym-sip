import torch
import gym
from gym import wrappers, logger

from spinup import ppo_pytorch as ppo

import gym_sips
from sips.h import helpers as h


def env_fn(): return gym.make("Sips-v0")

ac_kwargs = dict(hidden_sizes=[64, 64], activation=torch.nn.ReLU)

logger_kwargs = dict(output_dir='/home/sippycups/absa/gym-sips/experiments/torch_ppo/',
                     exp_name='torch_ppo')

ppo(env_fn=env_fn, ac_kwargs=ac_kwargs, steps_per_epoch=5000,
    epochs=250, logger_kwargs=logger_kwargs)

