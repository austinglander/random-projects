# Some more code from my friend, slightly modified

from vector import vector
from cube_control import send_frame
from time import time, sleep
from random import randint, choice
from math import ceil, sqrt

coordinate_grid = [[[vector(x, y, z) for x in range(8)] for y in range(8)] for z in range(8)]

radius = 1.5
gravity = 200
floor_elasticity = 0.999
wall_elasticity = 0.995
collision_tolerance = 1

center = vector(3.5, 3.5, 3.5)
ball_pos = vector(4, 4, radius - collision_tolerance)
ball_velocity = vector(randint(5, 15)*choice([-1,1]), randint(5, 15)*choice([-1,1]), sqrt(2*gravity*(7 + collision_tolerance - 2*radius)))
acceleration = vector(0, 0, -gravity)

def show_ball():
    frame = []

    for layer in coordinate_grid:
        for row in layer:
            byte = 0

            for coord in row:
                byte |= is_in_ball(coord) << coord.x
                
            frame.append(byte)
    
    send_frame(frame)

def is_in_ball(p: vector):
    p -= ball_pos
    return p.x**2 + p.y**2 + p.z**2 <= radius**2

def animate_bouncy_ball(anim_time):
    global ball_pos
    global ball_velocity
    global acceleration
    global radius
    
    last_t = time()
    last_fling = time()
    t0 = time()
    while time() - t0 < anim_time:
        dt = time() - last_t
        last_t = time()
        next_pos = ball_pos + ball_velocity.scale(dt)

        if time() - last_fling > 10:
            last_fling = time()
            ball_velocity = vector(randint(5, 15)*choice([-1,1]), randint(5, 15)*choice([-1,1]), sqrt(2*gravity*(7 + collision_tolerance - 2*radius)))
        if next_pos.z - radius < 0 - collision_tolerance or next_pos.z + radius > 7 + collision_tolerance:
            ball_velocity.z *= -1
        else:
            ball_velocity += acceleration.scale(dt)
            ball_velocity.z *= floor_elasticity
        if next_pos.x - radius < 0 - collision_tolerance or next_pos.x + radius > 7 + collision_tolerance:
            ball_velocity.x *= -wall_elasticity
        if next_pos.y - radius < 0 - collision_tolerance or next_pos.y + radius > 7 + collision_tolerance:
            ball_velocity.y *= -wall_elasticity

        ball_pos += ball_velocity.scale(dt)

        show_ball()
            
if __name__ == "__main__":
    print("1")
    animate_bouncy_ball(999999)