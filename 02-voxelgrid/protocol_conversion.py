# Contains functions to convert to and from sane coordinate storing to the protocol

from bitarray import bitarray

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
                
