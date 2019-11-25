from gym.envs.registration import register
# from gym_sips.envs.sips_extrahard_env import FooExtraHardEnv

register(
    id='sips-v0',
    entry_point='gym_sips.envs:SipsEnv',
)
