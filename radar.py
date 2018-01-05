from SGN import *
from antenna import Antenna, DnMode
import math
import numpy as np

def simple_antenna_rad_pattern(th, phi):
    if th == 0 and phi == 0:
        return 1

    if math.fabs(th) < 1*math.pi/180 and math.fabs(phi) < 1*math.pi/180:
        width_hor = 10 * math.pi / 180
        width_ver = 10 * math.pi / 180
        return math.sin(math.sqrt((th * 1.39156 * 2 / width_hor) * (th * 1.39156 * 2 / width_hor) + (phi * 1.39156 * 2 / width_ver) * (phi * 1.39156 * 2/width_ver))) /\
               math.sqrt((th * 1.39156 * 2 / width_hor) * (th * 1.39156 * 2 / width_hor) + (phi * 1.39156 * 2 / width_ver) * (phi * 1.39156 * 2 / width_ver))
    return 0

antenna = Antenna(simple_antenna_rad_pattern, 1000, math.pi/30, math.pi/30, DnMode["by_func"])

#signal = Rect(5000000, 200000, 5e-6)

signal = PacketRect(10000000, 100000, 5e-6, 50)


settings = {"antenna": antenna,
            "signal": signal,
            "sigma": 0.05,
            "max_range": 150000,
            "F": 0.0001}



    
max_r = int(settings["max_range"]/settings["signal"].resol) - 1
max_p = int(2*math.pi/settings["antenna"].dph) - 1
max_t = int(math.pi/(2*settings["antenna"].dth)) - 1


Range = np.arange(max_r)*settings["signal"].resol
Thetta = np.arange(max_t)*settings["antenna"].dth
Phi = np.arange(max_p)*settings["antenna"].dph


RadioV = {"max_r": max_r,
              "max_p": max_p,
              "max_t": max_t,
              "range": Range,
              "thetta": Thetta,
              "phi": Phi}





class IndexError(Exception):
    def __init__(self):
        pass
        
    def __str__(self):
        return repr("Index out of range!")
    
    
def get_V(i):
    if i >= RadioV["max_r"]: raise IndexError()
    r = i*settings["signal"].resol
    V = np.pi*(r**2)*settings["antenna"].dth*settings["antenna"].dph*settings["signal"].resol/(16*np.log(2))
    return V
    



