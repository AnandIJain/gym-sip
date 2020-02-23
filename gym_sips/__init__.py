from gym.envs.registration import register


register(
    id="Sips-v0",
    entry_point="gym_sips.envs:SipsEnv"
    # max_episode_steps=200
)

# register(
#     id="Req-v0",
#     entry_point="gym_sips.envs:ReqEnv"
#     # max_episode_steps=200
# )
