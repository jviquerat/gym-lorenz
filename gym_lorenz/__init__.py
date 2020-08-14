from gym.envs.registration import register

register(
    id='lorenz-oscillator-v0',
    entry_point='gym_lorenz.envs:LorenzOscillator',
)

register(
    id='lorenz-stabilizer-v0',
    entry_point='gym_lorenz.envs:LorenzStabilizer',
)
