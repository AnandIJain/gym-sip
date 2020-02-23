import argparse
import random
import sys

import gym
from gym import wrappers, logger

import gym_sips
from sips.h import helpers as h


class RandomAgent(object):
    """The world's simplest agent!"""

    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "env_id", nargs="?", default="Sips-v0", help="Select the environment to run"
    )
    args = parser.parse_args()
    logger.set_level(logger.INFO)
    env = gym.make(args.env_id)
    env.seed(0)
    agent = RandomAgent(env.action_space)
    episode_count = 1

    reward = 0
    done = False
    r_sum = 0
    for i in range(episode_count):
        ob = env.reset()
        ep_r = 0
        j = 0
        while True:
            action = agent.act(ob, reward, done)
            ob, reward, done, info = env.step(action)
            ep_r += reward

            print(f"{j}: r: {reward}, info: {info}")
            j += 1
            if done:
                break
            
        print(f"ep_r: {ep_r}")
        print(f"info: {i}")
        r_sum += ep_r
    # Close the env and write monitor result info to disk
    print(f"r_sum: {r_sum}")
    env.close()
