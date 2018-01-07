PyRadar
=========
>PyRadar is a model of radar implemented in python.

![enter image description here](https://user-images.githubusercontent.com/35064209/34639194-ee96ee82-f2eb-11e7-9890-598162e584cb.gif)

Requirements
------------------
- numpy (1.13.1)
- pyopengl(3.1.0)
-  pyqt5(5.9)
- scipy(0.19.1)


First Test
----
To make a test run of the application simply use:
> python GUI.py

Organisation
---
 - SNG.py - implements signals, used in radar computations. Here i defined a pack of rectangular signal. You can use whatever you want, but the class you use shold be inherited from Signal.

 - antenna.py - implements a class of radar antenna. I use a simple reflector antenna with a narrow beam directional diagram.

 - common,py - contains a class coords to represent a posision and velocity of radar and targets. It also has a target control class Traectory, which uses Euler-Lagrange method to control target movements.

 - primaryproc.py - Implements primary processing of radar data.

 - propagation.py - contains classes of targets and class for modeling signal propagation in space between radar and target.

 - radar.py - radar main settings  
