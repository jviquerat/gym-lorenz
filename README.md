# gym-lorenz

A simple gym environment to control the behavior of the ```lorenz-63``` attractor.

## Usage

To use this repository as a ```gym``` environment, clone it and then ```pip install -e gym-lorenz```. The control-less environment can also be run using ```python3 start.py```. At the end of the computation, the timestep and coordinates history will be dumped in a ```.dat``` file, and plots will be automatically generated using ```gnuplot```.

## Description of the environments

There are two environments available, strongly inspired from <a href="https://research.tue.nl/files/146730787/Beintema_afstudeerverslag.pdf">this thesis</a>. In both cases, control is applied to the Lorenz attractor on the y derivative: 

<p align="center">
  <img width="200" alt="Capture d’écran 2020-08-14 à 10 52 06" src="https://user-images.githubusercontent.com/44053700/90231962-3c47a400-de1c-11ea-80c6-2f089047e7ff.png">
</p>

The control value can take only discrete values (-1, 0 and 1), and control is applied every unit of time (which is much coarser than what is presented in the reference above, although it allows to train the controller within minutes on a standard laptop). The system is evolved from an initial condition for 5 units of time, after which control kicks in for 25 units of time.

### ```gym_lorenz:lorenz-oscillator-v0```

The first environment aims at maximizing the number of sign changes of the x component. Reward is consistently 0, except when x sign changes, in which case it is +1. The control-less environments has a reward of 14. Below is a sample of controlled vs uncontrolled environment, processed with an in-house PPO code.




### ```gym_lorenz:lorenz-stabilizer-v0```

The second environment aims at minimizing the number of sign changes of the x component. Reward is consistently 0, except when x sign changes, in which case it is -1. The control-less environments has a reward of -14. Below is a sample of controlled vs uncontrolled environment, processed with an in-house PPO code.


