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
    active_puddles = []
    t0 = time()
    t = time()
    while t - t0 < anim_time:
        # Initialize empty frame as 3D 8x8x8 list, using bits to store data
        # Indexed by: frame[x][y][z]
        frame = [[bitarray([0 for k in range(8)]) for j in range(8)] for i in range(8)]
        

        # Modified random number generation
        if randint(1, chance) == 1:
            x = randint(0, 7)
            y = randint(0, 7)
            z = 7
            active_raindrops.append((t, vector(x, y, z)))

        for drop in active_raindrops:
            drop_t0, pos = drop
            if pos.z < -1:
                active_raindrops.remove(drop)
                # Create small puddle around the drop
                active_puddles.append((t, pos, randint(0,4)))
                continue
            else:
                # Render drop
                # Drops are 2 voxels tall
                # CURSED and UGLY code (GROSS)
                # frame[8*ceil(pos.z) + pos.x] |= (1 << pos.y)
                # frame[8*ceil(pos.z - 1) + pos.x] |= (1 << pos.y)
                # Clean and happy code 😌
                frame[pos.x][pos.y][ceil(pos.z)] = 1
                frame[pos.x][pos.y][ceil(pos.z) - 1] = 1
                delta_t = t - drop_t0
                pos.z = 7 - initial_velocity*delta_t - acceleration*delta_t**2 / 2
                
        for puddle in active_puddles:
            puddle_t0, pos, size = puddle
            # Let puddle persist for 1 second
            if t - puddle_t0 > 0.1:
                active_puddles.remove(puddle)
                continue
            else:
                # Render puddle
                # Min and max for bounds checking
                # Random ints for puddle motion
                frame[pos.x][pos.y][0] = 1
                # Different sized puddle based on size value
                if size == 4:
                    frame[min(pos.x+1, 7)][pos.y][0] = 1
                if size >= 3:
                    frame[pos.x][max(pos.y-1,0)][0] = 1
                if size >= 2:
                    frame[pos.x][min(pos.y+1,7)][0] = 1
                if size >= 1:
                    frame[max(pos.x-1, 0)][pos.y][0] = 1
                    
            
        # Render the frame
        send_frame(to_protocol(frame))
        t = time()

if __name__ == "__main__":
    animate_raindrops(9999999999)