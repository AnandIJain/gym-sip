from gym.envs.registration import register

register(
    id="sips-v0", entry_point="gym_sips.envs:SipsEnv",
)
