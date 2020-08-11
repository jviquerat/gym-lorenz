from gym.envs.registration import register

register(
    id='lorenz-v0',
    entry_point='gym_lorenz.envs:LorenzEnv',
)
