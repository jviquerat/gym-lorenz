# Custom imports
from gym_lorenz.envs.lorenz_env import Lorenz

###############################################
### Lorenz stabilizer class
class LorenzStabilizerEasy(Lorenz):

    # Compute reward
    def get_rwd(self, x_prv, x):

        rwd = (x < 0.0)*1.0 - (x > 0.0)*1.0

        return rwd
