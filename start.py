# Generic improts
import os
import sys
import collections

# Custom imports
from gym_lorenz.envs.lorenz_env import *

########################
# Run Lorentz attractor
########################

# Nb of iterations
n_imgs = 300

# Initialize attractor
lorenz = LorenzEnv()

# Evolve attractor
done = False
while (not done):
    _, _, done, _ = lorenz.step()

# Plot
os.system('gnuplot -c plot.gnu '+str(lorenz.path)+' '+str(len(lorenz.lst_t))+' '+str(n_imgs))
