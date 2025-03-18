# This is a supplementary script to the snake game. I need a way to traverse the 8x8x8 grid in a repeatable cycle to avoid hitting my tail.
# A hamiltonian cycle achieves this. ChatGPT made me this script to find one

import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define grid size
N = 8
grid = np.full((N, N, N), -1)  # -1 means unvisited

# Possible movement directions in 3D (6 possible moves)
DIRECTIONS = [
    (1, 0, 0), (-1, 0, 0),  # Move in X direction
    (0, 1, 0), (0, -1, 0),  # Move in Y direction
    (0, 0, 1), (0, 0, -1)   # Move in Z direction
]

# Hamiltonian cycle storage
hamiltonian_path = []

def is_valid_move(x, y, z):
    """Check if the move is within bounds and the voxel is unvisited."""
    return 0 <= x < N and 0 <= y < N and 0 <= z < N and grid[x, y, z] == -1

def hamiltonian_dfs(x, y, z, step):
    """Recursive backtracking to find Hamiltonian cycle."""
    global hamiltonian_path

    # Mark the current voxel with the step number
    grid[x, y, z] = step
    hamiltonian_path.append((x, y, z))

    # If all voxels are visited, check if we can connect back to the start
    if step == N**3 - 1:
        start_x, start_y, start_z = hamiltonian_path[0]
        if any((x + dx, y + dy, z + dz) == (start_x, start_y, start_z) for dx, dy, dz in DIRECTIONS):
            return True  # Found a valid Hamiltonian cycle
        else:
            grid[x, y, z] = -1
            hamiltonian_path.pop()
            return False  # Backtrack

    # Shuffle directions for randomness (avoiding bias)
    random.shuffle(DIRECTIONS)

    # Try all possible moves
    for dx, dy, dz in DIRECTIONS:
        new_x, new_y, new_z = x + dx, y + dy, z + dz
        if is_valid_move(new_x, new_y, new_z):
            if hamiltonian_dfs(new_x, new_y, new_z, step + 1):
                return True  # If a valid path is found, propagate success

    # Backtrack if no move works
    grid[x, y, z] = -1
    hamiltonian_path.pop()
    return False

# Start Hamiltonian path from (0,0,0)
if hamiltonian_dfs(0, 0, 0, 0):
    print("Hamiltonian cycle found!")
else:
    print("No Hamiltonian cycle found.")

# Visualization of the Hamiltonian cycle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x_vals, y_vals, z_vals = zip(*hamiltonian_path)
ax.plot(x_vals, y_vals, z_vals, marker='o', linestyle='-', color='b', markersize=3)

# Annotate start and end
ax.scatter([x_vals[0]], [y_vals[0]], [z_vals[0]], color='green', s=100, label="Start")
ax.scatter([x_vals[-1]], [y_vals[-1]], [z_vals[-1]], color='red', s=100, label="End")

ax.set_title("Hamiltonian Cycle in 8x8x8 Grid")
ax.legend()
plt.show()
