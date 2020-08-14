# Custom imports
from gym_lorenz.envs.lorenz_env import Lorenz

###############################################
### Lorenz oscillator class
class LorenzOscillator(Lorenz):

    # Compute reward
    def get_rwd(self, x_prv, x):

        rwd = 0.0 + (x_prv*x < 0.0)*1.0

        return rwd
