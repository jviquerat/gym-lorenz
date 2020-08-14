# gym-lorenz

A simple gym environment to control the behavior of the ```lorenz-63``` attractor.

<p align="center">
  <img width="500" alt="gif" src="https://user-images.githubusercontent.com/44053700/90248026-1defa180-de38-11ea-9bee-098a9af9d56d.gif">
</p>

## Usage

To use this repository as a ```gym``` environment, clone it and then ```pip install -e gym-lorenz```. The control-less environment can also be run using ```python3 start.py```. At the end of the computation, the timestep and coordinates history will be dumped in a ```.dat``` file, and plots will be automatically generated using ```gnuplot```.

## Description of the environments

There are two environments available, strongly inspired from <a href="https://research.tue.nl/files/146730787/Beintema_afstudeerverslag.pdf">this thesis</a>. In both cases, control is applied to the Lorenz attractor on the y derivative: 

<p align="center">
  <img width="200" alt="lorenz" src="https://user-images.githubusercontent.com/44053700/90231962-3c47a400-de1c-11ea-80c6-2f089047e7ff.png">
</p>

The control value can take only discrete values (-1, 0 and 1), and control is applied every unit of time (which is much coarser than what is presented in the reference above). The system is evolved from an initial condition for 5 units of time, after which control kicks in for 25 units of time.

**Warning** : the environment currently works in parallel, but the ```lorenz_*.dat``` are not consistent when using multiple environments. Still, the environment can be learned using a single environment within less than 3 to 4 minutes on a modern laptop.

### ```gym_lorenz:lorenz-oscillator-v0```

The first environment aims at maximizing the number of sign changes of the x component. Reward is consistently 0, except when x sign changes, in which case it is +1. The control-less environments has a reward of 14. Below is a sample of controlled vs uncontrolled environment, processed with an in-house PPO code. As can be seen, the control significantly increases the number of sign changes, while constraining the trajectory.

<p align="center">
  <img width="900" alt="oscillator_2D" src="https://user-images.githubusercontent.com/44053700/90250978-4c23b000-de3d-11ea-9dca-1f5194ed4754.png">
</p>

<p align="center">
  <img width="300" alt="uncontrolled_3D" src="https://user-images.githubusercontent.com/44053700/90246972-f1d32100-de35-11ea-883f-7476d6082e4d.png"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
  <img width="300" alt="controlled_3D" src="https://user-images.githubusercontent.com/44053700/90246970-f0095d80-de35-11ea-9726-332167676a1c.png">
</p>

<p align="center">
  <img width="800" alt="oscillator_2D" src="https://user-images.githubusercontent.com/44053700/90244347-de718700-de30-11ea-8cb1-a9e6b297b0fc.png">
</p>

### ```gym_lorenz:lorenz-stabilizer-v0```

The second environment aims at minimizing the number of sign changes of the x component. Reward is consistently 0, except when x sign changes, in which case it is -1. The control-less environments has a reward of -14. Below is a sample of controlled vs uncontrolled environment, processed with an in-house PPO code. As can be seen, the control significantly decreases the number of sign changes.

<p align="center">
  <img width="900" alt="oscillator_2D" src="https://user-images.githubusercontent.com/44053700/90250987-4ded7380-de3d-11ea-99a3-69769bc4e781.png">
</p>

<p align="center">
  <img width="300" alt="uncontrolled_3D" src="https://user-images.githubusercontent.com/44053700/90246972-f1d32100-de35-11ea-883f-7476d6082e4d.png"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
  <img width="300" alt="controlled_3D" src="https://user-images.githubusercontent.com/44053700/90248296-bbe36c00-de38-11ea-9b53-4a9b8d688dd8.png">
</p>

<p align="center">
  <img width="800" alt="stabilizer_2D" src="https://user-images.githubusercontent.com/44053700/90248437-fc42ea00-de38-11ea-9d2a-ebf60eae53e7.png">
</p>
