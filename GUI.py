#!/home/alexander/anaconda2/envs/radar/bin/python
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *
from PyQt5.Qt import QMainWindow, QApplication
from radar import settings
from primaryproc import PrimaryProc
from propagation import Propagation, SimpleTarget, coords, coord_sys#, CloudTarget, EPRGen
import numpy as np
#from tqdm import tqdm




st = SimpleTarget(100, coords(75000, 0, 180 * math.pi / 180, coord_sys["spherical"]),
                  coords(200, 0, 0.1, coord_sys["spherical"]))

#st1 = SimpleTarget(10, coords(100000, 0, 45 * math.pi / 180, coord_sys["spherical"]),
     #             coords(0, 0, 0.1, coord_sys["spherical"]))
#cl = create_cloud(50000, 80000, 0, 0)

#gen = EPRGen()


pr = Propagation()
pr.targets = [st] #+ gen.get()
pp = PrimaryProc()

class SpiralWidget(QGLWidget):
    '''
    Widget for drawing two spirals.
    '''

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(500, 500)
        self.timerticks = 0
        self.targets = []
        self.settings = {"IKO":{"max_range": settings["max_range"], "tick_dist": 10000, "azimuth_ticks": 8,
                                "speed": 6}}

        self.ray_pos = []
        size = int(1200 / self.settings["IKO"]["speed"])
        for i in range(size):
            self.ray_pos.append(i * 2 * math.pi / size)

        self.cur_pos = 0
        self.timerId = self.startTimer(50)


    def paintGL(self):
        '''
        Drawing routine
        '''

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glColor(0.0, 1.0, 0.0)
        for i in range(int(self.settings["IKO"]["max_range"]/self.settings["IKO"]["tick_dist"])+1):
            radius = i*self.settings["IKO"]["tick_dist"]/self.settings["IKO"]["max_range"]
            glBegin(GL_LINE_STRIP)
            for j in range(201):
                glVertex2d(radius*math.cos(2*j*math.pi/200), radius*math.sin(2*j*math.pi/200))
            glEnd()

        glBegin(GL_LINES)

        #draw ray
        glVertex2d(0,0)
        glVertex2d(math.sin(self.ray_pos[self.cur_pos]),math.cos(self.ray_pos[self.cur_pos]))

        #draw azimuth ticks

        for i in range(self.settings["IKO"]["azimuth_ticks"]):
            da = 2*math.pi*i/self.settings["IKO"]["azimuth_ticks"]
            glVertex2d(0, 0)
            glVertex2d(math.cos(da), math.sin(da))

        glEnd()

        self.drawTragets()

        glFlush()

    def timerEvent(self, QTimerEvent):

        #try:
        out = pp.compute(pr.compute())
        #except Exception as e:
        #    print(e)
        #self.killTimer(self.timerId)
        if len(out) >0:
            #print("new targets:",len(out))
            for i in out: self.add_target(i)

        self.timerticks+=1
        self.paintGL()
        self.swapBuffers()

        if self.cur_pos >= len(self.ray_pos) - 1:
            self.cur_pos = 0
            for target in pr.targets:
                if isinstance(target, CloudTarget):
                    pr.targets.remove(target)

            pr.targets = pr.targets #+ gen.get()
        else: self.cur_pos += 1
        settings["antenna"].cur_dir["phi"] = self.ray_pos[self.cur_pos]

    def add_target(self, target):
        self.targets.append({"azimuth": target["azimuth"],
                             "elevation": target["elevation"],
                             "range": target["range"],
                             "live": 0})

    def drawTragets(self):
        glPointSize(5)
        glColor(1.0,0.0, 0.0)
        glBegin(GL_POINTS)
        for target in self.targets:
            azim = target["azimuth"]
            elev = target["elevation"]
            r = target["range"]
            glVertex2d(r / self.settings["IKO"]["max_range"] * math.sin(azim),
                   r / self.settings["IKO"]["max_range"] * math.cos(azim))
        glEnd()
        if self.timerticks > len(self.ray_pos):
            self.timerticks = 0
            for target in self.targets:
                if target["live"] <=0:
                    self.targets = []#.remove(target)
                #else:
                 #   target["live"]-=1

    def resizeGL(self, w, h):
        '''
        Resize the GL window
        '''

        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

    def initializeGL(self):
        '''
        Initialize GL
        '''

        # set viewing projection
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)



class SpiralWidgetDemo(QMainWindow):
    ''' Example class for using SpiralWidget'''

    def __init__(self):
        QMainWindow.__init__(self)
        widget = SpiralWidget(self)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(['Spiral Widget Demo'])
    window = SpiralWidgetDemo()

    window.show()
    app.exec_()
