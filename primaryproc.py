import numpy as np
from antenna import Antenna
from SGN import Signal
from radar import settings
from scipy.signal import convolve
from scipy.special import erfinv
import math

complex_i = np.sqrt(-1+0j)
light_vel = 299792458

def erfinv1(x, power):
    out = 0
    c = []
    for i in range(power): c.append(0)
    c[0] = 1
    for k in range(power):
        if k!=0:
            for m in range(k):
                c[k] +=c[m]*c[k-1-m]/((m+1)*(2*m+1))
        out+=c[k]*pow(pow(math.pi,0.5)*x/2,2*k+1)/(2*k+1)
    return out


class PrimaryProc():
    def __init__(self):
        self.q = self.thress(0, settings["sigma"] * math.sqrt(settings["signal"].energy()) / 10000, 1 - settings["F"])
        print("q = ", self.q)
    def compute_corr(self, signal):
        assert settings["signal"].sampleRate == signal.sampleRate
        assert signal.samples.size - settings["signal"].samples.size >0

        return convolve(signal.samples, settings["signal"].samples, mode="same") / signal.sampleRate

    def thress(self, mean, sigma, p):
        return mean + sigma*math.pow(2,0.5)*erfinv(2*p-1)

    def compute(self, signal):
        targets = []
        c  = self.compute_corr(signal)

        mat = c.reshape((settings["signal"].pack_num, -1))

        w = mat.shape[1] / settings["signal"].sampleRate

        freq = np.fft.fftfreq(settings["signal"].pack_num, d=w)

        ids = np.argsort(freq)
        sorted_freq = np.take(freq, ids)

        q = 0.4
        out = list()
        for i in range(mat.shape[1]):
            f = np.abs(np.fft.fft(mat[:, i]))
            if np.any(f > q):
                f = np.take(f, ids)
                # args = np.argwhere(f > q)
                # taked = np.take(f, args)
                # arg = np.int(np.sum(taked*args)/np.sum(taked))
                arg = np.argmax(f)
                out.append((i, sorted_freq[arg]))

        if not len(out) == 0:
            for t in out:
                arg = t[0]
                freq = t[1]
                mean_vel = freq * light_vel / (2 * settings["signal"].ctrF)
                if mean_vel < 20: continue
                mean_dist = (arg - settings["signal"].samples.size) / settings["signal"].sampleRate * light_vel / 2    
                
                print("mean_vel = ", mean_vel)
                #print("mean_dist = ", mean_dist)
                targets.append({"azimuth": settings["antenna"].cur_dir["phi"],
                            "elevation": settings["antenna"].cur_dir["th"],
                            "range": mean_dist,
                            "velocity": mean_vel})
            
            
            #mean_vel = np.mean(freqs) * light_vel / (2 * settings["signal"].ctrF)
            #print("mean_vel = ", mean_vel)

            #if np.all(freqs == 0):
            #    mean_d = np.mean(args) - int(settings["signal"].samples.size / 2)
            #else:
            #    mean_d = np.sum(freqs * args) / np.sum(freqs) - int(settings["signal"].samples.size / 2)
            #mean_dist = (mean_d - settings["signal"].samples.size) / settings["signal"].sampleRate * light_vel / 2
            #print("mean_dist = ", mean_dist)
            #targets.append({"azimuth": settings["antenna"].cur_dir["phi"],
            #                "elevation": settings["antenna"].cur_dir["th"],
            #                "range": mean_dist,
            #                "velocity": mean_vel})

        return targets

