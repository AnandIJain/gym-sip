import random

import gin
import gym

from tf_agents.environments import suite_gym

import gym_sips

MAX_STEPS = 1000
PRINT_FREQ = MAX_STEPS / 20

if __name__ == "__main__":
    env = suite_gym.load("Sips-v0", max_episode_steps=MAX_STEPS)
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
