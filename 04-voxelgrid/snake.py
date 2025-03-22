# Simulate a snake game on the cube
# First attempt at working with user input on the cube

from cube_control import send_frame
from cube_utils import to_protocol, empty_frame, write_string
from time import time
from random import randint, choice
from math import ceil
from bitarray import bitarray
import keyboard


DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)) # w s a d q e
direction = (0, 0, 0) # Initialize direction to 0 to wait for player input to start moving

def get_bot_direction(head: tuple) -> tuple:
    """
    Returns a new direction for the snake to travel given its current direction and head position\n
    Implements a very naive traversal of the board that scores exactly 63 points before losing.
    """
    # Naive snake algorithm of traversing the whole board for each apple
    # I'm not boutta go into algorithm hell for snake (i ain't code bullet) 💀
    # The edgiest cases need to come earliest in the if chain because less restrictive cases would take over for the edge cases
    # Current best: 63 - limited by current strategy of returning to origin constantly. Need to find a hamiltonian cycle for a 3D space

    # Choose starting direction based on parity of x (need to get on a specific cycle)
    x, y, z = head
    if direction == (0, 0, 0):
        if x % 2 == 0:
            return DIRECTIONS[3]
        else:
            return DIRECTIONS[2]
    
    
    # Return to origin from (0,0,7)
    if direction == DIRECTIONS[1] and x == 0 and y == 0 and z == 7: # End of grid. Traverse to origin
        return DIRECTIONS[5]
    if direction == DIRECTIONS[5] and x == 0 and y == 0 and z == 0: # Cycle finished
        return DIRECTIONS[3]

    # Return to origin corner from (7,1,z)
    if direction == DIRECTIONS[2] and x == 7 and y == 0: # End of layer. Traverse back to origin corner
        return DIRECTIONS[1]
    if direction == DIRECTIONS[1] and x == 0 and y == 0 and z != 7: # Move up
        return DIRECTIONS[4]

    # Deprecated by starting parity logic
    # # Return to origin corner from (7,7,z) (technically not necessary if starting at even x val, but including this case is more exhaustive in case starting point moves)
    # if direction == DIRECTIONS[3] and x == 7 and y == 7: # End of layer. Traverse back to origin corner
    #     return DIRECTIONS[1]
    # if direction == DIRECTIONS[1] and x == 0 and y == 7: # Turn right to continue traversal to origin corner
    #     return DIRECTIONS[2]
    # if direction == DIRECTIONS[2] and x == 0 and y == 0 and z != 7: # Move up
    #     return DIRECTIONS[4]

    # Traverse layer, skipping one row to avoid running into self
    if direction == DIRECTIONS[4]: # Begin layer
        return DIRECTIONS[3]
    if direction == DIRECTIONS[3] and x != 7 and y == 7: # About to hit right wall, turn left
        return DIRECTIONS[0]
    if direction == DIRECTIONS[0] and y == 7: # If I just turned left, turn left again
        return DIRECTIONS[2]
    if direction == DIRECTIONS[2] and x != 7 and y == 1: # About to hit left wall, turn right
        return DIRECTIONS[0]
    if direction == DIRECTIONS[0] and y == 1: # If I just turned right, turn right again
        return DIRECTIONS[3]
    
    return direction

def update_direction(e: keyboard.KeyboardEvent) -> None:
    """
    Callback function to update direction on keypress
    """
    global direction
    if e.name == "w" and direction not in DIRECTIONS[0:2]:
        direction = DIRECTIONS[0]
    if e.name == "s" and direction not in DIRECTIONS[0:2]:
        direction = DIRECTIONS[1]
    if e.name == "a" and direction not in DIRECTIONS[2:4]: 
        direction =  DIRECTIONS[2]
    if e.name == "d" and direction not in DIRECTIONS[2:4]:
        direction =  DIRECTIONS[3]
    if e.name == "q" and direction not in DIRECTIONS[4:6]:
        direction =  DIRECTIONS[4]
    if e.name == "e" and direction not in DIRECTIONS[4:6]:
        direction =  DIRECTIONS[5]

def play_snake(tickrate: float = 0.3, invincible: bool = False, coyote_time_ticks: int = 2, bot = False):
    """
    Starts an interactive game of snake\n
    tickrate: number of seconds between movements\n
    invincible: when set to true, collisions that normally end the game instead pause the game and wait for a valid input to continue\n
    bot: when set to true, ignores user input and plays the game with a naive bot\n
    coyote_time: dictates the number of frames that can be spent in a losing position before ending the game
    """
    global direction
    # Register a keypress event handler if the player should be in control
    if not bot:
        keyboard.on_press(update_direction)

    snake = [(4, 4, 4)] # Initialize snake position
    apple = (randint(0,7), randint(0,7), randint(0,7)) # Initialize apple
    score = 0
    coyote_time = 0 # Give a grace period when running into obstacles
    bounds = {(x,y,z) for x in range(8) for y in range(8) for z in range(8)}

    while True:
        t = time()
        # Generate a new head position for the snake based on current direction
        if bot:
            direction = get_bot_direction(snake[-1])
        head = snake[-1]
        new_head = (head[0] + direction[0], head[1] + direction[1], head[2] + direction[2])


        # If our new head is out of bounds or in the snake, we have collided (assuming the game has already started!)
        collided = not (new_head in bounds) or new_head in snake and direction != (0, 0, 0)

        if collided and not invincible:
            if coyote_time >= coyote_time_ticks:
                break # End game
            coyote_time += 1

        if not collided:
            coyote_time = 0 # reset coyote_time upon valid move
            snake.append(new_head) # Only extend the snake if it won't collide with something

        # Now that we've moved forward, check if we ate the apple and generate a new one
        if snake[-1] == apple:
            score += 1
            apple = choice(tuple(bounds - set(snake)))
        # If we ate the apple, don't pop the end of the snake (thus extending its size)
        elif not collided:
            snake.pop(0)

        # Render logic
        frame = empty_frame()
        frame[apple[0]][apple[1]][apple[2]] = 1 # render apple
        for segment in snake: # render snake
            frame[segment[0]][segment[1]][segment[2]] = 1
        protocol_frame = to_protocol(frame)

        # Make each game tick take roughly tickrate seconds without capping frame rate
        send_frame(protocol_frame)
        while time() - t < tickrate:
            send_frame(protocol_frame)
    
    # Game over logic
    # Maybe I could have some fun physics animations at the end? Fireworks maybe?
    print(f"Score: {score}")
    end_frame = empty_frame()
    write_string(end_frame, str(min(99, score))) # Cap score display at 99
    while True:
        send_frame(to_protocol(end_frame))


if __name__ == "__main__":
    play_snake(tickrate=0.3, coyote_time_ticks=2, invincible=False, bot=False)