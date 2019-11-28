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

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id, dfs=h.get_full_games())

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    # outdir = '/tmp/random-agent-results'
    # env = wrappers.Monitor(env, directory=outdir, force=True)

    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 100
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()
        while True:
            action = agent.act(ob, reward, done)
            ob, reward, done, info = env.step(action)
            print(f"r: {reward}, info: {info}")
            if done:
                break
            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.

    # Close the env and write monitor result info to disk
    env.close()


if __name__ == "__main__":
    env = gym.make('Sips-v0')
    MAX_STEPS = 1000
    PRINT_FREQ = MAX_STEPS / 20
    r_sum = 0
    for i in range(MAX_STEPS):
        o, r, d, info = env.step(random.randint(0, 2))
        r_sum += r
        # print(f'GAME_END: {o.GAME_END}')
        if i % PRINT_FREQ == 0:
            print(f'r_sum: {r_sum}')
            # print(f'info: {i[0]}')

        # print("action_spec:", env.action_spec())
        # print("time_step_spec.observation:", env.time_step_spec().observation)
        # print("time_step_spec.step_type:", env.time_step_spec().step_type)
        # print("time_step_spec.discount:", env.time_step_spec().discount)
        # print("time_step_spec.reward:", env.time_step_spec().reward)
