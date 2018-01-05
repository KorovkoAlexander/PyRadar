
import numpy as np
from akima import interpolate
import matplotlib.pyplot as plt


i = np.sqrt(-1+0j)
light_vel = 299792458

class Signal():
    def __init__(self, ctrF, sampleRate, samples, pack_num = 1):
        self.ctrF = ctrF
        self.sampleRate = sampleRate
        self.samples = samples
        self.resol = 0
        self.pack_num = pack_num


    def freqShift(self, newFreq):
         if newFreq <0: return
         if newFreq == self.ctrF: return
         if newFreq > self.ctrF:
             f2 = newFreq - self.ctrF

             newSize = self.samples.size *newFreq/self.ctrF
             newSR = self.sampleRate*newSize/self.samples.size
             T = 1/newSR
             x = np.linspace(0, 1, self.samples.size)
             new_x = np.linspace(0, 1, newSize)

             interp_r = interpolate(x, self.samples.real, new_x)
             interp_i = interpolate(x, self.samples.imag, new_x)

             out = (interp_r + i*interp_i)*np.exp(-i*T*f2*np.arange(interp_i.size))

             self.ctrF = newFreq
             self.sampleRate = newSR
             self.samples = out
             return out
         if newFreq < self.ctrF:
             f2 = self.ctrF - newFreq
             T = 1/self.sampleRate

             newSize = self.samples.size*newFreq/self.ctrF
             newSR = self.sampleRate*newFreq/self.ctrF

             k = (np.arange(newSize)*self.ctrF/newFreq).astype(np.int)
             out = np.take(self.samples, k)*np.exp(i*f2*T*np.arange(newSize))

             self.samples = out
             self.sampleRate = newSR
             self.ctrF = newFreq
             return out

    def shift_freq(self, deltaf):
        if deltaf == 0: return
        if deltaf > 0:
            newFreq = self.ctrF + deltaf
            newSize = self.samples.size * newFreq / self.ctrF
            newSR = self.sampleRate * newSize / self.samples.size
            T = 1 / newSR
            x = np.linspace(0, 1, self.samples.size)
            new_x = np.linspace(0, 1, newSize)

            interp_r = interpolate(x, self.samples.real, new_x)
            interp_i = interpolate(x, self.samples.imag, new_x)

            out = (interp_r + i * interp_i) * np.exp(-i * T * deltaf * np.arange(interp_i.size))

            s = Signal(newFreq, newSR, out)
            return s
        if deltaf < 0:
            newFreq = self.ctrF + deltaf
            T = 1 / self.sampleRate

            newSize = self.samples.size * newFreq / self.ctrF
            newSR = self.sampleRate * newFreq / self.ctrF

            k = (np.arange(newSize) * self.ctrF / newFreq).astype(np.int)
            out = np.take(self.samples, k) * np.exp(-i * deltaf * T * np.arange(newSize))

            s = Signal(newFreq, newSR, out)

    def energy(self):
        return (np.power(np.abs(self.samples),2)).sum()/self.sampleRate

    def ref_area(self):
        return np.abs(self.samples).sum()/self.sampleRate


class Rect(Signal):
    def __init__(self, ctrF, amplitude, width):
        sampleRate = 5*ctrF
        samples = amplitude * np.exp(-i * 2*np.pi*ctrF * np.linspace(0, width, np.int(width* sampleRate)))
        print(np.linspace(0, width, np.int(width / sampleRate)))
        super().__init__(ctrF, sampleRate, samples)
        self.resol = light_vel*width/2

class PacketRect(Signal):
    def __init__(self,ctrF, amplitude, width, pack_num):
        sampleRate = 0.1 * ctrF   # даже не смотри сюда, пидор
        samples = amplitude * np.exp(-i * 2 * np.pi * ctrF * np.linspace(0, width, np.int(width * sampleRate)))
        print(np.linspace(0, width, np.int(width / sampleRate)))
        super().__init__(ctrF, sampleRate, samples, pack_num= pack_num)
        self.resol = light_vel * width / 2
