import math
from abc import ABCMeta, abstractmethod
import numpy as np
from radar import settings, RadioV, get_V
from SGN import Signal
#from cloud import CloudModel
#from tqdm import tqdm
from common import *

complex_i = np.sqrt(-1+0j)
light_vel = 299792458


gen_set = {"r":1e-3}

"""
class EPRGen():
    def __init__(self):
        self.cloud = CloudModel()
        for i in range(60):
            self.cloud.new_state()
    # return the list of cloud targets
    def get(self):
        
        out = list()
        U,V,W,R = self.cloud.new_state()
        
        
        for i in range(RadioV["max_r"]):
            for j in range(RadioV["max_p"]):
                for k in range(RadioV["max_t"]):
                    r = RadioV["range"][i]
                    th = RadioV["thetta"][k]
                    p = RadioV["phi"][j]
                    
                    if r == 0: continue
                    pos = coords(r,th,p,coord_sys["spherical"])
                    
                    x,y,z = self.cartes(r,th,p)                  
                    
                    x_i = int((x + settings["max_range"])/self.cloud.delta.x)
                    y_i = int((y + settings["max_range"])/self.cloud.delta.y)
                    z_i = int(z/self.cloud.delta.z)
                    
                    vel = coords(U[x_i,y_i,z_i], V[x_i,y_i,z_i], W[x_i,y_i,z_i], coord_sys["cartesian"])
                    Ro = R[x_i,y_i,z_i]
                    
                    V_o = get_V(i)
                    lambd = light_vel/settings["signal"].ctrF
                    
                    Sigma_sum = 64*(np.pi**4)*(gen_set["r"]**3)*0.93*Ro*V_o/((lambd**4)*998*4)
                    
                    SIGMA = np.random.exponential(Sigma_sum, size=1)
                    #print(SIGMA)
                    
                    target = CloudTarget(SIGMA, pos, vel)
                    out.append(target)
                      
        return out
                    
                    
              
                
    @staticmethod
    def cartes(r, th, phi):
            x = r*math.cos(th)*math.cos(phi)
            y = r*math.cos(th)*math.sin(phi)
            z = r*math.sin(th)
            return (x,y,z)
"""

class AbstractTarget():
    __metaclass__ = ABCMeta

    @abstractmethod
    def response(self,out):
        """Переместить объект"""

    @abstractmethod
    def pos(self):
        """Скорость объекта"""

    @abstractmethod
    def vel(self):
        """Скорость объекта"""

"""
class CloudTarget(AbstractTarget):
    def __init__(self, sigma, pos, vel):
        self.pos = pos.spheric()
        self.vel = vel.spheric()
        self.sigma = sigma


    def response(self,out):

        antenna = settings["antenna"]

        TH = self.pos.th - antenna.cur_dir["th"]
        PH = antenna.cur_dir["phi"] - self.pos.phi

        alpha = np.arctan(np.power(np.power(np.tan(TH),2) + np.power(np.tan(PH),2),0.5))

        if alpha > antenna.dalpha: return

        signal = settings["signal"].samples
        distance = self.pos.distance_to(coords(0, 0, 0, coord_sys["cartesian"]))
        lamb = light_vel / settings["signal"].ctrF

        DN_value = antenna.dn_value(TH,PH)
        magic_K = antenna.gain*math.pow(DN_value,2)*lamb*math.pow(self.sigma/4*math.pi,0.5)/(4*math.pi*math.pow(distance,2))
        tau_delay = 2*distance/light_vel

        delay_sample = tau_delay*settings["signal"].sampleRate
        max_l = int(2 * settings["max_range"] / light_vel * out.sampleRate + 3*signal.size)

        for k in range(int(delay_sample), out.samples.size):
            cnt = int(k - delay_sample)
            if cnt >= signal.size: break

            amplitude = np.abs(signal[cnt])
            phase = angle(signal[cnt])

            vel = self.vel.spheric()

            new_amplitude = amplitude * magic_K

            for i in range(settings["signal"].pack_num):
                new_phase = phase + 4 * math.pi * settings["signal"].ctrF * (distance + vel.r * (cnt + max_l*i) / out.sampleRate) / light_vel
                out.samples[signal.size + k + max_l*i]+= new_amplitude*(math.cos(new_phase)+complex_i*math.sin(new_phase))

"""

class SimpleTarget(AbstractTarget):
    def __init__(self, sigma, pos, vel):
        self.pos = pos.spheric()
        self.vel = vel.spheric()
        self.trac = Traectory()
        self.sigma = sigma

    def move(self):
        new_pos, new_vel = self.trac.move(self.pos, self.vel)
        self.pos = new_pos.spheric()
        self.vel = new_vel.spheric()


    def response(self,out):

        self.move()
        antenna = settings["antenna"]

        TH = self.pos.th - antenna.cur_dir["th"]
        PH = antenna.cur_dir["phi"] - self.pos.phi

        alpha = np.arctan(np.power(np.power(np.tan(TH),2) + np.power(np.tan(PH),2),0.5))

        if alpha > antenna.dalpha: return

        signal = settings["signal"].samples
        distance = self.pos.distance_to(coords(0, 0, 0, coord_sys["cartesian"]))
        lamb = light_vel / settings["signal"].ctrF

        DN_value = antenna.dn_value(TH,PH)
        magic_K = antenna.gain*math.pow(DN_value,2)*lamb*math.pow(self.sigma/4*math.pi,0.5)/(4*math.pi*math.pow(distance,2))
        tau_delay = 2*distance/light_vel

        delay_sample = tau_delay*settings["signal"].sampleRate
        max_l = int(2 * settings["max_range"] / light_vel * out.sampleRate + 3*signal.size)

        for k in range(int(delay_sample), out.samples.size):
            cnt = int(k - delay_sample)
            if cnt >= signal.size: break

            amplitude = np.abs(signal[cnt])
            phase = angle(signal[cnt])

            vel = self.vel.spheric()

            new_amplitude = amplitude * magic_K

            for i in range(settings["signal"].pack_num):
                new_phase = phase + 4 * math.pi * settings["signal"].ctrF * (distance + vel.r * (cnt + max_l*i) / out.sampleRate) / light_vel
                out.samples[signal.size + k + max_l*i]+= new_amplitude*(math.cos(new_phase)+complex_i*math.sin(new_phase))


def angle(sample):
    ph = 0
    if sample.real!=0: ph = math.atan2(sample.imag, sample.real)
    else:
        if sample.imag > 0: ph = math.pi/2
        if sample.imag < 0: ph = 3*math.pi / 2
        if sample.imag == 0: ph = 0
    return ph


class Propagation():
    def __init__(self):
        self.targets = []

    def compute(self):
        
        signal = settings["signal"]
        outsize = settings["signal"].pack_num*int(2 * settings["max_range"] / light_vel * signal.sampleRate + 3*signal.samples.size)
        out = np.zeros(outsize, dtype = np.complex)
        outsignal = Signal(signal.ctrF, signal.sampleRate, out)       

        for tg in self.targets:
            tg.response(outsignal)


        phase = np.angle(outsignal.samples)

        add = np.random.normal(0, settings["sigma"], phase.size)
        outsignal.samples+= add*(np.cos(phase) + complex_i* np.sin(phase))
        return outsignal



