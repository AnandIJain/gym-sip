import random

import gin
import gym

import tensorflow as tf
import tf_agents as tfas 

from tf_agents.environments.tf_wrappers import TFEnvironmentBaseWrapper
from tf_agents.networks import actor_distribution_network
from tf_agents.environments import suite_gym
from tf_agents.agents.reinforce import reinforce_agent
from tf_agents.replay_buffers.tf_uniform_replay_buffer import TFUniformReplayBuffer
from tf_agents.drivers.dynamic_episode_driver import DynamicEpisodeDriver

import gym_sips

MAX_STEPS = 1000
PRINT_FREQ = MAX_STEPS / 20

if __name__ == "__main__":
    env = TFEnvironmentBaseWrapper(suite_gym.load(
        "Sips-v0", max_episode_steps=MAX_STEPS))
    obs_spec = env.observation_spec()
    act_spec = env.action_spec()
    actor_net = actor_distribution_network.ActorDistributionNetwork(
        obs_spec, act_spec,
        fc_layer_params=[200, 100, 50, 3]
    )

    agent = reinforce_agent.ReinforceAgent(
        env.time_step_spec(),
        env.action_spec(),
        actor_network=actor_net,
        optimizer=tf.keras.optimizers.AdamOptimizer(learning_rate=1e-3)
    )
    
    replay_buffer = TFUniformReplayBuffer([], batch_size=1)
    driver = DynamicEpisodeDriver(
        env, agent.collect_policy, 
        observers=[replay_buffer.add_batch],
        num_episodes=1
    )

    for i in range(MAX_STEPS):
        driver.run()
        experience = replay_buffer.gather_all()
        agent.train(experience)
        replay_buffer.clear()
