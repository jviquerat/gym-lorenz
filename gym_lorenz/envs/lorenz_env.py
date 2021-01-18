# Generic imports
import os
import sys
import time
import gym
import math
import random
import numpy           as     np
from   gym             import error, spaces, utils
from   gym.utils       import seeding
from   scipy.integrate import odeint

###############################################
### Generic class
class Lorenz(gym.Env):
    metadata = {'render.modes': ['human']}

    # Initialize instance
    def __init__(self):

        # Main parameters
        self.name       = 'lorenz'
        self.sigma      = 10.0
        self.rho        = 28.0
        self.beta       = 8.0/3.0
        self.dt_act     = 1.0
        self.int_steps  = 50
        self.dt         = self.dt_act/(self.int_steps - 1)
        self.act        = [-1.0, 0.0, 1.0]
        self.norm       = 100.0
        self.t_max      = 25.0
        self.init_time  = 5.0
        self.init_steps = math.floor(self.init_time/self.dt_act)
        self.t0         =-self.init_time

        # Other attributes
        self.idx        =-1
        self.cpu        = 0
        self.n_cpu      = 1

        # Observation and action spaces
        self.observation_space = spaces.Box(low=-self.norm,
                                            high=self.norm,
                                            shape=(6,))
        self.action_space      = spaces.Discrete(len(self.act))

    # Set cpus and paths
    def set_cpu(self, cpu, n_cpu):

        # Set nb of cpus and index
        self.cpu   = cpu
        self.n_cpu = n_cpu
        self.idx   =-cpu-1

        # Handle paths
        res_path = self.name
        if (self.cpu == 0):
            if (not os.path.exists(res_path)):
                os.makedirs(res_path)
        t         = time.localtime()
        path_time = time.strftime("%H-%M-%S", t)
        self.path = res_path+'/'+str(path_time)
        if (self.cpu == 0):
            if (not os.path.exists(self.path)):
                os.makedirs(self.path)

    # Reset variables
    def reset(self):

        # Update index for output
        self.idx  += self.n_cpu

        # Initial point
        self.x0    = 10.0
        self.y0    = 15.0
        self.z0    =-15.0

        # Init values and lists
        self.t     = self.t0
        self.x     = self.x0
        self.y     = self.y0
        self.z     = self.z0

        self.x_prv = self.x
        self.y_prv = self.y
        self.z_prv = self.z

        self.vx    = 0.0
        self.vy    = 0.0
        self.vz    = 0.0

        self.lst_t = []
        self.lst_x = []
        self.lst_y = []
        self.lst_z = []
        self.lst_a = []

        # Run several steps before starting control
        for _ in range(self.init_steps):
            self.step()

        return self.get_obs()

    # Lorenz attractor
    def lorenz(self, xv, t, a, sigma, rho, beta):

        x, y, z = xv
        dxdt    = sigma*(y - x)
        dydt    = x*(rho - z) - y + a
        dzdt    = x*y - beta*z

        return dxdt, dydt, dzdt

    # Stepping with possible action
    def step(self, a=1):

        # Integrate and compute reward
        rwd = 0.0
        t   = np.linspace(self.t, self.t+self.dt_act, self.int_steps)
        act = self.act[a]
        f   = odeint(self.lorenz,
                     (self.x, self.y, self.z), t,
                     args=(act, self.sigma, self.rho, self.beta))

        for i in range(1,self.int_steps-1):
            self.lst_t.append(self.t)
            self.lst_x.append(self.x)
            self.lst_y.append(self.y)
            self.lst_z.append(self.z)
            self.lst_a.append(act)

            self.x_prv = self.x
            self.y_prv = self.y
            self.z_prv = self.z

            self.x  = float(f.T[0,i])
            self.y  = float(f.T[1,i])
            self.z  = float(f.T[2,i])
            self.t += self.dt

            rwd += self.get_rwd(self.x_prv, self.x)

        # Compute velocities
        self.vx = (self.x - self.x_prv)/self.dt
        self.vy = (self.y - self.y_prv)/self.dt
        self.vz = (self.z - self.z_prv)/self.dt

        # Get observation
        obs = self.get_obs()

        # Handle termination
        done = False
        if (self.t+self.dt >= self.t_max):
            done = True
            self.dump(self.idx)
            self.lst_t.append(self.t)
            self.lst_x.append(self.x)
            self.lst_y.append(self.y)
            self.lst_z.append(self.z)
            self.lst_a.append(act)

        return obs, rwd, done, None

    # Compute reward
    def get_rwd(self, x_prv, x):

        rwd = 0.0

        return rwd

    # Get observations
    def get_obs(self):

        x  = self.x
        y  = self.y
        z  = self.z
        vx = self.vx
        vy = self.vy
        vz = self.vz

        obs = [x, y, z, vx, vy, vz]

        return obs

    # Dump
    def dump(self, idx=None):

        addstr = ''
        if (idx is not None):
            addstr = '_'+str(idx)

        filename = self.path+'/lorenz'+addstr+'.dat'
        np.savetxt(filename,
                   np.hstack([np.reshape(self.lst_t, (-1,1)),
                              np.reshape(self.lst_x, (-1,1)),
                              np.reshape(self.lst_y, (-1,1)),
                              np.reshape(self.lst_z, (-1,1)),
                              np.reshape(self.lst_a, (-1,1))]),
                   fmt='%.5e')

    # Rendering
    def render(self, mode='human'):
        pass

    # Closing
    def close(self):
        pass
