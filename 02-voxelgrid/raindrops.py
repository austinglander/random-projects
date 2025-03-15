# This is my friend's algorithm, modified

from vector import vector
from cube_control import send_frame
from time import time, sleep
from random import randint
from math import ceil
from bitarray import bitarray
from protocol_conversion import to_protocol


# 1 in ___ per tick
chance = 12
initial_velocity = 10
acceleration = 375

def animate_raindrops(anim_time):
    active_raindrops = []
    t0 = time()
    while time() - t0 < anim_time:
        # Initialize empty frame as 3D 8x8x8 list, using bits to store data
        # Indexed by: frame[x][y][z]
        frame = [[bitarray([0 for k in range(8)]) for j in range(8)] for i in range(8)]
        

        # Modified random number generation
        if randint(1, chance) == 1:
            x = randint(0, 7)
            y = randint(0, 7)
            z = 7
            active_raindrops.append((time(), vector(x, y, z)))

        for drop in active_raindrops:
            drop_t0, pos = drop
            if pos.z < -1:
                active_raindrops.remove(drop)
                continue
            else:
                # Drops are 2 voxels tall
                # CURSED and UGLY code (GROSS)
                # frame[8*ceil(pos.z) + pos.x] |= (1 << pos.y)
                # frame[8*ceil(pos.z - 1) + pos.x] |= (1 << pos.y)
                # Clean and happy code 😌
                frame[pos.x][pos.y][ceil(pos.z)] = 1
                frame[pos.x][pos.y][ceil(pos.z) - 1] = 1
                
            
            delta_t = time() - drop_t0
            pos.z = 7 - initial_velocity*delta_t - acceleration*delta_t**2 / 2
        send_frame(to_protocol(frame))

if __name__ == "__main__":
    animate_raindrops(9999999999)