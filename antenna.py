from math import *

DnMode = {"by_func":1, "by_array": 2}

class Antenna():
    def __init__(self, func, Gain, Dth, Dph, mode):
        self.func = func
        self.gain = Gain
        self.dth = Dth
        self.dph = Dph
        self.dalpha = 1*pi/180#atan(pow(pow(tan(Dth), 2) + pow(tan(Dph),2),0.5))
        self.cur_dir = {"th":0, "phi": 0}
        self.dn_mode = mode

    def dn_value(self, th, phi):
        if self.dn_mode == DnMode["by_func"]:
            return self.func(th, phi)
        if self.dn_mode == DnMode["by array"]:
            print("Antenna:DN by array is not implemented yet!")
            exit(-1)