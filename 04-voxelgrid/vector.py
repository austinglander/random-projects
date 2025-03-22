# My friend's vector class
from dataclasses import dataclass
from math import sin, cos, sqrt

@dataclass
class vector:
    x: float
    y: float
    z: float

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def scale(self, factor):
        return vector(self.x * factor, self.y * factor, self.z * factor)

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def mag(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def x_rotate(self, angle):
        yr = self.y*cos(angle) - self.z*sin(angle)
        zr = self.z*cos(angle) + self.y*sin(angle)
        return vector(self.x, yr, zr)
    
    def y_rotate(self, angle):
        xr = self.x*cos(angle) - self.z*sin(angle)
        zr = self.z*cos(angle) + self.x*sin(angle)
        return vector(xr, self.y, zr)
    
    def z_rotate(self, angle):
        xr = self.x*cos(angle) + self.y*sin(angle)
        yr = self.y*cos(angle) - self.x*sin(angle)
        return vector(xr, yr, self.z)
    
    def get_rounded_pos(self) -> tuple:
        """
        Returns a tuple of the vector's rounded coordinates
        """
        return round(self.x), round(self.y), round(self.z)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"