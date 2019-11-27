import random

import gin
import gym

from tf_agents.environments import suite_gym

import gym_sips

MAX_STEPS = 10

if __name__ == "__main__":
    env = suite_gym.load('Sips-v0', max_episode_steps=MAX_STEPS)
    for i in range(MAX_STEPS):
        o, r, d, i = env.step(random.randint(0, 2))
        print('action_spec:', env.action_spec())
        print('time_step_spec.observation:', env.time_step_spec().observation)
        print('time_step_spec.step_type:', env.time_step_spec().step_type)
        print('time_step_spec.discount:', env.time_step_spec().discount)
        print('time_step_spec.reward:', env.time_step_spec().reward)
