# gym-lorenz

A simple gym environment to control the behavior of the ```lorenz-63``` attractor.

## Usage

To use this repository as a ```gym``` environment, clone it and then ```pip install -e gym-lorenz```. The control-less environment can also be run using ```python3 start.py```. At the end of the computation, the timestep and coordinates history will be dumped in a ```.dat``` file, and plots will be automatically generated using ```gnuplot```.

## Results

Below are a few visuals of the control-less environment:

#### ```x0 = 0```, ```y0 = 1```, ```z0 = 1```

<p align="center">
  <img width="900" alt="" src="https://user-images.githubusercontent.com/44053700/88798155-c2b98000-d1a4-11ea-99b2-8c4fc7b30815.png">
</p>

<p align="center">
  <img width="500" alt="" src="https://user-images.githubusercontent.com/44053700/88798657-833f6380-d1a5-11ea-9750-c0faf0fa29c7.gif">
</p>
