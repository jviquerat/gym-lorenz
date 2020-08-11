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
### Class attractor
class LorenzEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    # Initialize instance
    def __init__(self):

        # Main parameters
        self.sigma      = 10.0
        self.rho        = 28.0
        self.beta       = 8.0/3.0
        self.dt_act     = 1.5
        self.dt         = 0.05
        self.int_steps  = int(self.dt_act/self.dt)
        self.act        = [-1.0, 0.0, 1.0]
        self.norm       = 100.0
        self.t_max      = 50.0
        self.hist_size  = 2
        self.init_time  = 25.0
        self.init_steps = math.floor(self.init_time/(self.dt_act))
        self.t0         =-self.init_time
        self.idx        =-1
        self.rand_range = 30.0

        # Handle paths
        res_path   = 'lorenz'
        if (not os.path.exists(res_path)):
            os.makedirs(res_path)
        t         = time.localtime()
        path_time = time.strftime("%H-%M-%S", t)
        self.path = res_path+'/'+str(path_time)
        if (not os.path.exists(self.path)):
            os.makedirs(self.path)

        # Observation and action spaces
        self.observation_space = spaces.Box(low=-self.norm,
                                            high=self.norm,
                                            shape=(3*self.hist_size,))
        self.action_space      = spaces.Discrete(len(self.act))

        # Reset env
        self.reset()

    # Reset variables
    def reset(self):

        # Update index for output
        self.idx  += 1

        # Initial point
        self.x0    = 1.0
        self.y0    = 1.0
        self.z0    = 1.0

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

        self.lst_t = [self.t0]
        self.lst_x = [self.x0]
        self.lst_y = [self.y0]
        self.lst_z = [self.z0]
        self.lst_a = [0]

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

        for i in range(self.int_steps):
            self.x_prv = self.x
            self.y_prv = self.y
            self.z_prv = self.z

            self.x  = float(f.T[0,i])
            self.y  = float(f.T[1,i])
            self.z  = float(f.T[2,i])
            self.t += self.dt_act/(self.int_steps-1)

            self.lst_t.append(self.t)
            self.lst_x.append(self.x)
            self.lst_y.append(self.y)
            self.lst_z.append(self.z)
            self.lst_a.append(act)

            rwd += self.get_rwd(self.x_prv, self.x)

        # Compute velocities
        self.vx = (self.x - self.x_prv)/self.dt
        self.vy = (self.y - self.y_prv)/self.dt
        self.vz = (self.z - self.z_prv)/self.dt

        # Get observation
        obs = self.get_obs()

        # Check termination status
        done = False
        if (self.t >= self.t_max):
            done = True
            self.dump(self.idx)

        return obs, rwd, done, None

    # Compute reward
    def get_rwd(self, x_prv, x):

        rwd = 0.0 + (x_prv*x < 0.0)*1.0

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
