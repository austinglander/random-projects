# My own script from scratch

from vector import vector
from cube_control import send_frame
from time import time, sleep
from random import randint
from math import ceil
from bitarray import bitarray
from protocol_conversion import to_protocol, empty_frame

def animate_lsu():
    LSU = empty_frame()
    # Configure the letters to appear in back of box from top left to bottom right
    # L
    LSU[5][0][7] = 1
    LSU[5][0][6] = 1
    LSU[5][0][5] = 1
    LSU[5][0][4] = 1
    LSU[5][1][4] = 1
    LSU[5][2][4] = 1
    LSU[5][3][4] = 1
    # S
    LSU[6][4][5] = 1
    LSU[6][3][5] = 1
    LSU[6][2][5] = 1
    LSU[6][2][4] = 1
    LSU[6][2][3] = 1
    LSU[6][3][3] = 1
    LSU[6][4][3] = 1
    LSU[6][4][2] = 1
    LSU[6][4][1] = 1
    LSU[6][3][1] = 1
    LSU[6][2][1] = 1
    # U
    LSU[7][5][3] = 1
    LSU[7][5][2] = 1
    LSU[7][5][1] = 1
    LSU[7][5][0] = 1
    LSU[7][6][0] = 1
    LSU[7][7][0] = 1
    LSU[7][7][1] = 1
    LSU[7][7][2] = 1
    LSU[7][7][3] = 1
    while True:
        send_frame(to_protocol(LSU))
    # Idea: Store L, S, and U points as vectors. Apply a linear transformation to the L points to bring them
    # Front and center. Reverse the transformation, then apply one to the S. Then to the U. Repeat.
    

if __name__ == "__main__":
    animate_lsu()