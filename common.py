import numpy as np
import math


coord_sys = {"spherical": 1, "cartesian": 2}

tf = 60 #sec
u_tax = 1000
default_r = 10000

class coords():
    def __init__(self, X ,Y ,Z, cs):
        self.x = X
        self.y = Y
        self.z = Z
        self.cs = cs

    def __str__(self):
        if self.cs == coord_sys["spherical"]:
            return """coords: spherical,
r = {r},
th = {th},
phi = {ph}""".format(r = self.r, th = self.th, ph = self.phi)

        else:
            return """coords: cartesian,
x = {r},
y = {th},
z = {ph}""".format(r=self.r, th=self.th, ph=self.phi)


    def __getattr__(self, item):
        if item == "r" or item == "x": return self.x
        if item == "th" or item == "y": return self.y
        if item == "phi" or item == "z": return self.z

    def to_spherical(self):
        if self.cs == coord_sys["spherical"]: return
        if self.x == 0 and self.y == 0 and self.z == 0:
            self.cs = coord_sys["cartesian"]
            return

        r = math.pow(math.pow(self.x ,2) + math.pow(self.y ,2) + math.pow(self.z ,2), 0.5)
        th = math.asin(self. z /r)
        if self.x == 0:
            if self.y >0: ph = math.pi / 2
            if self.y < 0: ph = 3 / 2 * math.pi
            if self.y == 0: ph = 0
        else:
            ph = math.atan(self.y / self.x)
            if self.y > 0 and self.x < 0: ph = math.pi - math.atan(-self.y / self.x)
            if self.y < 0 and self.x > 0: ph = 2 * np.pi - math.atan(-self.y / self.x)
            if self.y < 0 and self.x < 0: ph = math.pi + math.atan(self.y / self.x)

        self.cs = coord_sys["spherical"]
        self.r = r
        self.th = th
        self.phi = ph

    def to_cartesian(self):
        if self.cs == coord_sys["cartesian"]: return
        x = self.r * math.cos(self.th) * math.cos(self.phi)
        y = self.r * math.cos(self.th) * math.sin(self.phi)
        z = self.r * math.sin(self.th)

        self.x = x
        self.y = y
        self.z = z
        self.cs = coord_sys["cartesian"]

    def spheric(self):
        if self.cs == coord_sys["spherical"]: return self.get_copy()
        if self.x == 0 and self.y == 0 and self.z == 0:
            return coords(0, 0, 0, coord_sys["spherical"])

        r = math.pow(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2), 0.5)
        th = math.asin(self.z / r)
        if self.x == 0:
            if self.y > 0: ph = math.pi / 2
            if self.y < 0: ph = 3 / 2 * math.pi
            if self.y == 0: ph = 0
        else:

            ph = math.atan(self.y / self.x)
            if self.y > 0 and self.x < 0: ph = math.pi - math.atan(-self.y / self.x)
            if self.y < 0 and self.x > 0: ph = 2 * np.pi - math.atan(-self.y / self.x)
            if self.y < 0 and self.x < 0: ph = math.pi + math.atan(self.y / self.x)

        return coords(r, th, ph, coord_sys["spherical"])

    def get_copy(self):
        return coords(self.x, self.y, self.z, self.cs)

    def cartes(self):
        if self.cs == coord_sys["cartesian"]: return self.get_copy()
        x = self.r * math.cos(self.th) * math.cos(self.phi)
        y = self.r * math.cos(self.th) * math.sin(self.phi)
        z = self.r * math.sin(self.th)
        return coords(x, y, z, coord_sys["cartesian"])

    def distance_to(self, point):
        temp2 = point.cartes()
        temp1 = self.cartes()
        # print(temp1)
        return math.pow(math.pow(temp1.x - temp2.x, 2) + \
                        math.pow(temp1.y - temp2.y, 2) + \
                        math.pow(temp1.z - temp2.z, 2), 0.5)


class Traectory():
    def __init__(self, delta_t =0.05):
        self.tf = tf  # sec
        self.delta_t = delta_t
        self.u_tax = 1000
        self.t = self.tf/delta_t
        self.coord_stack = []

    @staticmethod
    def get_new_aim(pos, r = default_r):
        p = pos.cartes()
        x = np.random.uniform(p.x - r, p.x + r)
        y = np.random.uniform(np.sqrt(r ** 2 - (x - p.x) ** 2) + p.y, -np.sqrt(r ** 2 - (x - p.x) ** 2) + p.y)
        z = p.z
        print("new aim posinion: x =", x," y = ", y, " z = ", z)

        out_pos =  coords(x,y,z,coord_sys["cartesian"])
        x = np.random.uniform(50, 200)
        y = np.random.uniform(50, 200)
        z = 0

        out_vel = coords(x,y,z,coord_sys["cartesian"])

        return (out_pos, out_vel)


    def move(self, pos, vel):
        #print("pos = ", pos, " vel = vel")
        if self.t*self.delta_t < tf:
            out = self.coord_stack[0]
            self.coord_stack.remove(self.coord_stack[0])
            self.t +=1
            return out
        else:
            self.t = 0
            pos_t = pos.cartes()
            vel_t = vel.cartes()

            aim = Traectory.get_new_aim(pos)
            aim_pos = aim[0]
            aim_vel = aim[1]

            delta_pos_x = aim_pos.x - pos_t.x
            delta_pos_y = aim_pos.y - pos_t.y
            delta_pos_z = aim_pos.z - pos_t.z

            delta_vel_x = aim_vel.x - vel_t.x
            delta_vel_y = aim_vel.y - vel_t.y
            delta_vel_z = aim_vel.z - vel_t.z

            c1_x = 4 * u_tax * (3 * delta_pos_x - self.tf * (2 * aim_vel.x + delta_vel_x)) / np.power(self.tf, 3)
            c1_y = 4 * u_tax * (3 * delta_pos_y - self.tf * (2 * aim_vel.y + delta_vel_y)) / np.power(self.tf, 3)
            c1_z = 4 * u_tax * (3 * delta_pos_z - self.tf * (2 * aim_vel.z + delta_vel_z)) / np.power(self.tf, 3)

            c2_x = 4 * u_tax * (3 * delta_pos_x - self.tf * aim_vel.x) / np.power(self.tf, 2)
            c2_y = 4 * u_tax * (3 * delta_pos_y - self.tf * aim_vel.y) / np.power(self.tf, 2)
            c2_z = 4 * u_tax * (3 * delta_pos_z - self.tf * aim_vel.z) / np.power(self.tf, 2)

            for i in range(int(self.tf/self.delta_t)):
                t = i*self.delta_t
                pos_x = -c1_x * (t ** 3) / (12 * u_tax) + c2_x * (t ** 2) / (4 * u_tax) + vel_t.x * t + pos_t.x
                pos_y = -c1_y * (t ** 3) / (12 * u_tax) + c2_y * (t ** 2) / (4 * u_tax) + vel_t.y * t + pos_t.y
                pos_z = -c1_z * (t ** 3) / (12 * u_tax) + c2_z * (t ** 2) / (4 * u_tax) + vel_t.z * t + pos_t.z

                vel_x = -c1_x * (t ** 2) / (4 * u_tax) + c2_x * t / (2 * u_tax) + vel_t.x
                vel_y = -c1_y * (t ** 2) / (4 * u_tax) + c2_y * t / (2 * u_tax) + vel_t.y
                vel_z = -c1_z * (t ** 2) / (4 * u_tax) + c2_z * t / (2 * u_tax) + vel_t.z

                p = coords(pos_x, pos_y, pos_z, coord_sys["cartesian"])
                v = coords(vel_x, vel_y, vel_z, coord_sys["cartesian"])
                self.coord_stack.append((p,v))

            out = self.coord_stack[0]
            self.coord_stack.remove(self.coord_stack[0])
            self.t += 1
            return out