# Simulate a snake game on the cube
# First attempt at working with user input on the cube

from vector import vector
from cube_control import send_frame
from time import time, sleep
from random import randint, choice
from math import ceil
from bitarray import bitarray
from protocol_conversion import to_protocol, empty_frame
import keyboard

def get_direction(current_direction: tuple, bot: bool = False, head: tuple = None) -> tuple:
    """
    Returns a new direction for the snake to travel given it's current direction and what keys are being pressed"
    If bot is set to True, direction is chosen automatically without considering user input.
    Head is only required if bot is set to True (needed to make movement decisions)
    """
    directions = ((1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)) # w s a d q e
    if bot:
        # Naive snake algorithm of traversing the whole board for each apple
        # I'm not boutta go into algorithm hell for snake (i ain't code bullet) 💀
        # The edgiest cases need to come earliest in the if chain because less restrictive cases would take over for the edge cases
        # Current best: 63 - limited by current strategy of returning to origin constantly. Need to find a hamiltonian cycle for a 3D space

        # Choose starting direction based on parity of x (need to get on a specific cycle)
        x, y, z = head
        if current_direction == (0, 0, 0):
            if x % 2 == 0:
                return directions[3]
            else:
                return directions[2]
        
        
        # Return to origin from (0,0,7)
        if current_direction == directions[1] and x == 0 and y == 0 and z == 7: # End of grid. Traverse to origin
            return directions[5]
        if current_direction == directions[5] and x == 0 and y == 0 and z == 0: # Cycle finished
            return directions[3]

        # Return to origin corner from (7,1,z)
        if current_direction == directions[2] and x == 7 and y == 0: # End of layer. Traverse back to origin corner
            return directions[1]
        if current_direction == directions[1] and x == 0 and y == 0 and z != 7: # Move up
            return directions[4]

        # Deprecated by starting parity logic
        # # Return to origin corner from (7,7,z) (technically not necessary if starting at even x val, but including this case is more exhaustive in case starting point moves)
        # if current_direction == directions[3] and x == 7 and y == 7: # End of layer. Traverse back to origin corner
        #     return directions[1]
        # if current_direction == directions[1] and x == 0 and y == 7: # Turn right to continue traversal to origin corner
        #     return directions[2]
        # if current_direction == directions[2] and x == 0 and y == 0 and z != 7: # Move up
        #     return directions[4]

        # Traverse layer, skipping one row to avoid running into self
        if current_direction == directions[4]: # Begin layer
            return directions[3]
        if current_direction == directions[3] and x != 7 and y == 7: # About to hit right wall, turn left
            return directions[0]
        if current_direction == directions[0] and y == 7: # If I just turned left, turn left again
            return directions[2]
        if current_direction == directions[2] and x != 7 and y == 1: # About to hit left wall, turn right
            return directions[0]
        if current_direction == directions[0] and y == 1: # If I just turned right, turn right again
            return directions[3]
        
        return current_direction

    # We don't want to immediately return a direction being held if it is the current direction as that can block some maneuvers
    if keyboard.is_pressed("w") and current_direction not in directions[0:2]:
        return directions[0]
    if keyboard.is_pressed("s") and current_direction not in directions[0:2]:
        return directions[1]
    if keyboard.is_pressed("a") and current_direction not in directions[2:4]: 
        return directions[2]
    if keyboard.is_pressed("d") and current_direction not in directions[2:4]:
        return directions[3]
    if keyboard.is_pressed("q") and current_direction not in directions[4:6]:
        return directions[4]
    if keyboard.is_pressed("e") and current_direction not in directions[4:6]:
        return directions[5]
    # If no conditions matched, maintain course
    return current_direction

def write_digit(frame: list[list[bitarray]], digit: int, plane: int, right: int, top: int) -> None:
    """
    Writes a 3x5 decimal digit into the given frame (in-place) in the plane x="plane" with rightmost pixels at "right" and topmost pixels at "top"\n
    In other words, writes a digit into the frame with the top-right pixel specified by right and top. The x value for the digit is "plane"\n
    Does not currently support other orientations\n
    Input validation is the user's job
    """
    # Take intersection of frame with the plane
    # Digits are 3x5, and will be built from right to left, top to bottom
    face = frame[plane]
    match str(digit):
        case "0":
            # Column 1
            face[right][top] = 1
            face[right][top-1] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-1] = 1
            face[right-2][top-2] = 1
            face[right-2][top-3] = 1
            face[right-2][top-4] = 1
        case "1":
            # Column 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-1] = 1
            face[right-1][top-2] = 1
            face[right-1][top-3] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top-1] = 1
            face[right-2][top-4] = 1
        case "2":
            # Column 1
            face[right][top-1] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-3] = 1
            face[right-2][top-4] = 1
        case "3":
            # Column 1
            face[right][top] = 1
            face[right][top-1] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-2] = 1
            face[right-2][top-4] = 1
        case "4":
            # Column 1
            face[right][top] = 1
            face[right][top-1] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top-2] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-1] = 1
            face[right-2][top-2] = 1
        case "5":
            # Column 1
            face[right][top] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-1] = 1
            face[right-2][top-2] = 1
            face[right-2][top-4] = 1
        case "6":
            # Column 1
            face[right][top] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-1] = 1
            face[right-2][top-2] = 1
            face[right-2][top-3] = 1
            face[right-2][top-4] = 1
        case "7":
            # Column 1
            face[right][top] = 1
            face[right][top-1] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-3] = 1
            face[right-2][top-4] = 1
        case "8":
            # Column 1
            face[right][top] = 1
            face[right][top-1] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            face[right-1][top-4] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-1] = 1
            face[right-2][top-2] = 1
            face[right-2][top-3] = 1
            face[right-2][top-4] = 1
        case "9":
            # Column 1
            face[right][top] = 1
            face[right][top-1] = 1
            face[right][top-2] = 1
            face[right][top-3] = 1
            face[right][top-4] = 1
            # Column 2
            face[right-1][top] = 1
            face[right-1][top-2] = 1
            # Column 3
            face[right-2][top] = 1
            face[right-2][top-1] = 1
            face[right-2][top-2] = 1

def game_over_frame(score: int) -> list[list[bitarray]]:
    """
    Returns a frame to be displayed at the end of the game, displaying score
    """
    out_frame = empty_frame()
    if score > 99:
        score = 99 # TODO: High score easter egg
    right = 7
    top = 5
    for digit in reversed(str(score)):
        write_digit(out_frame, digit, plane=0, right=right, top=top)
        right -= 4
    return out_frame

def play_snake(tickrate: float = 0.2, invincible: bool = False, bot = False):
    """
    Starts an interactive game of snake\n
    Tickrate: number of seconds between movements. Be careful reducing this value below 0.005 as you may crash the program\n
    Invincible: when set to true, collisions that normally end the game instead pause the game and wait for a valid input to continue\n
    Bot: when set to true, ignores user input and plays the game with a naive bot
    """
    snake = [(4, 4, 4)] # Initialize snake position
    direction = (0, 0, 0) # Initialize direction to 0 to wait for player input to start moving
    apple = (randint(0,7), randint(0,7), randint(0,7)) # Initialize apple
    eaten = False
    score = 0
    coyote_time = 0 # Give a grace period when running into obstacles
    bounds = {(x,y,z) for x in range(8) for y in range(8) for z in range(8)}

    t = time()
    while True:
        # Generate an apple if the last one was eaten
        if eaten:
            apple = choice(tuple(bounds - set(snake))) # Choose apple position from points not in snake
        eaten = False

        # We store the snake as a list of tuples with the head at the end
        head = snake[-1]
        new_head = (head[0] + direction[0], head[1] + direction[1], head[2] + direction[2])


        # If our new head is out of bounds or in the snake, we have collided (assuming the game has already started!)
        collided = not (new_head in bounds) or new_head in snake and direction != (0, 0, 0)

        if collided and not invincible:
            if coyote_time > 2:
                break # End game
            coyote_time += 1

        if not collided:
            coyote_time = 0 # reset coyote_time upon valid move
            snake.append(new_head) # Only extend the snake if it won't collide with something

        # Now that we've moved forward, check if we ate the apple
        if snake[-1] == apple:
            eaten = True
            score += 1

        # If we ate the apple, don't pop the end of the snake (thus extending its size)
        if not collided and not eaten:
            snake.pop(0)

        # Render logic
        frame = empty_frame()
        frame[apple[0]][apple[1]][apple[2]] = 1 # render apple
        for segment in snake: # render snake
            frame[segment[0]][segment[1]][segment[2]] = 1
        protocol_frame = to_protocol(frame)

        # Make each game tick take about tickrate seconds without capping frame rate
        old_direction = direction
        t1 = time()
        while t1 - t < tickrate:
            send_frame(protocol_frame)
            # Poll for direction update in this portion of rapidly repeating logic to drop less inputs
            direction = get_direction(old_direction, bot, snake[-1])
            t1 = time()
        t = time()
    
    # Game over logic
    # Maybe I could have some fun physics animations at the end? Fireworks maybe?
    print(f"Score: {score}")
    end_frame = game_over_frame(score)
    while True:
        send_frame(to_protocol(end_frame))


if __name__ == "__main__":
    play_snake(tickrate=0.3, bot=False)