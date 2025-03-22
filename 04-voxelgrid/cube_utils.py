# Utility functions to help display things on the cube
# Maybe this stuff could be refactored into a frame class 🤔

from bitarray import bitarray

PIXEL_FONT_3X5 = {
    ' ': [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    'A': [
        [0,1,0],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,0,1]
    ],
    'B': [
        [1,1,0],
        [1,0,1],
        [1,1,0],
        [1,0,1],
        [1,1,0]
    ],
    'C': [
        [0,1,1],
        [1,0,0],
        [1,0,0],
        [1,0,0],
        [0,1,1]
    ],
    'D': [
        [1,1,0],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,0]
    ],
    'E': [
        [1,1,1],
        [1,0,0],
        [1,1,0],
        [1,0,0],
        [1,1,1]
    ],
    'F': [
        [1,1,1],
        [1,0,0],
        [1,1,0],
        [1,0,0],
        [1,0,0]
    ],
    'G': [
        [0,1,1],
        [1,0,0],
        [1,0,1],
        [1,0,1],
        [0,1,1]
    ],
    'H': [
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,0,1]
    ],
    'I': [
        [1,1,1],
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [1,1,1]
    ],
    'J': [
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [1,0,1],
        [0,1,0]
    ],
    'K': [
        [1,0,1],
        [1,0,1],
        [1,1,0],
        [1,0,1],
        [1,0,1]
    ],
    'L': [
        [1,0,0],
        [1,0,0],
        [1,0,0],
        [1,0,0],
        [1,1,1]
    ],
    'M': [
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1]
    ],
    'N': [
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,0,1]
    ],
    'O': [
        [0,1,0],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [0,1,0]
    ],
    'P': [
        [1,1,0],
        [1,0,1],
        [1,1,0],
        [1,0,0],
        [1,0,0]
    ],
    'Q': [
        [0,1,0],
        [1,0,1],
        [1,0,1],
        [0,1,0],
        [0,0,1]
    ],
    'R': [
        [1,1,0],
        [1,0,1],
        [1,1,0],
        [1,0,1],
        [1,0,1]
    ],
    'S': [
        [0,1,1],
        [1,0,0],
        [0,1,0],
        [0,0,1],
        [1,1,0]
    ],
    'T': [
        [1,1,1],
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [0,1,0]
    ],
    'U': [
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1]
    ],
    'V': [
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [0,1,0]
    ],
    'W': [
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [1,0,1]
    ],
    'X': [
        [1,0,1],
        [1,0,1],
        [0,1,0],
        [1,0,1],
        [1,0,1]
    ],
    'Y': [
        [1,0,1],
        [1,0,1],
        [0,1,0],
        [0,1,0],
        [0,1,0]
    ],
    'Z': [
        [1,1,1],
        [0,0,1],
        [0,1,0],
        [1,0,0],
        [1,1,1]
    ],

    # Digits 0–9
    '0': [
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1]
    ],
    '1': [
        [0,1,0],
        [1,1,0],
        [0,1,0],
        [0,1,0],
        [1,1,1]
    ],
    '2': [
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [1,0,0],
        [1,1,1]
    ],
    '3': [
        [1,1,1],
        [0,0,1],
        [0,1,1],
        [0,0,1],
        [1,1,1]
    ],
    '4': [
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1]
    ],
    '5': [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [0,0,1],
        [1,1,1]
    ],
    '6': [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ],
    '7': [
        [1,1,1],
        [0,0,1],
        [0,1,0],
        [1,0,0],
        [1,0,0]
    ],
    '8': [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ],
    '9': [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1]
    ]
}

def write_string(frame: list[list[bitarray]], string: str, pos: tuple = (0, 7, 5)):
    """
    Writes the given alphanumeric string to the frame in a 3x5 pixel font\n
    The top right pixel of the second character is placed at pos, with the rest of the string expanding to the left\n
    Supports only 1 and 2 character strings\n
    Only supports facing +x direction\n
    Bounds checking is the job of the user if they decide to change default pos\n
    """
    # Input validation
    if len(string) > 2 or not (string.replace(" ", "").isalnum() or string.replace(" ", "") == ""):
        raise ValueError("Invalid string: Expected alphanumeric string of length <= 2")
    
    right = pos[1]
    for char in reversed(string.upper()):
        char_data = PIXEL_FONT_3X5[char]
        # i, j indexes our character data and lets us offset from pos
        for i, row in enumerate(char_data):
            for j, bit in enumerate(row):
                frame[pos[0]][right-2+j][pos[2]-i] = bit
        right -= 4 # shift starting spot for character 2 left by 4



def to_protocol(frame: list[list[bitarray]]) -> list[int]:
    """
    Converts a 3D array of bits to the standard used for outputting to the voxel grid.\n
    """
    protocol_frame = [0] * 64
    for z in range(8):
        for y in range(8):
            for x in range(8):
                # Index is based on z and y, bit position is based on x
                # We use a bitwise OR to effectively insert frame[x][y][z] at the correct position
                protocol_frame[8*z+y] |= (frame[x][y][z] << x)
    return protocol_frame

def from_protocol(protocol_frame: list[int]) -> list[list[bitarray]]:
    """
    Converts an array from the standard used for outputting to the voxel grid to a 3D array of bits
    """
    # Initialize new frame to 0
    frame = [[bitarray([0 for k in range(8)]) for j in range(8)] for i in range(8)]
    for z in range(8):
        for y in range(8):
            # Convert the integer storing the x values into a bitarray
            # This should be exception safe if protocolFrame is valid (no values > 255)
            x_vals = bitarray()
            x_vals.frombytes(protocol_frame[8*z+y].to_bytes(1, 'little'))
            for x in range(8):
                frame[x][y][z] = x_vals[(7-x)]
    return frame
                
def empty_frame() -> list[list[bitarray]]:
    """
    Returns an empty 3D 8x8x8 array to be used to store coordinates
    """
    return [[bitarray([0 for k in range(8)]) for j in range(8)] for i in range(8)]
