# Simulate a snake game on the cube
from vector import vector
from cube_control import send_frame
from time import time, sleep
from random import randint
from math import ceil
from bitarray import bitarray
from protocol_conversion import to_protocol
import keyboard

def get_direction():
    if keyboard.is_pressed("w"): return (1, 0, 0)
    if keyboard.is_pressed("s"): return (-1, 0, 0)
    if keyboard.is_pressed("a"): return (0, -1, 0)
    if keyboard.is_pressed("d"): return (0, 1, 0)
    if keyboard.is_pressed("q"): return (0, 0, 1)
    if keyboard.is_pressed("e"): return (0, 0, -1)
    return None

def animate_snake(anim_time):
    snake = [(4, 4, 4)] # Initialize snake position
    direction = (0, 0, 0) # Initialize direction to 0 to wait for player input to start moving
    apple = (randint(0,7), randint(0,7), randint(0,7)) # Initialize apple
    eaten = False

    t0 = time()
    t = time()

    while t - t0 < anim_time:
        # Generate an apple if the last one was eaten
        if eaten:
            apple = (randint(0,7), randint(0,7), randint(0,7))
        eaten = False

        # Control the snake's direction
        new_direction = get_direction()
        if new_direction and new_direction != -1 * direction: # Don't allow switching direction
            direction = new_direction

        # We store the snake as a list of tuples with the head at the end
        head = snake[-1]
        new_head = (head[0] + direction[0], head[1] + direction[1], head[2] + direction[2])
        bounded_new_head = (max(0, min(7, new_head[0])),
                    max(0, min(7, new_head[1])),
                    max(0, min(7, new_head[2])))

        # If bounded_new_head is not the same as new_head, we went out of bounds. To keep things a sandbox for now, I don't want to continue moving when I hit an edge!
        hit_edge = new_head != bounded_new_head
        # Maybe to balance difficulty I could only make it a game over if you collide with yourself? It would make it more of a strategy game because you can use walls for time
        if not hit_edge:
            snake.append(bounded_new_head) # Only extend the snake if we're in bounds

        # Now that we've extended the snake, check if we ate the apple
        if snake[-1] == apple:
            eaten = True
        # If we ate the apple, don't pop the end of the snake (thus extending its size)
        if not hit_edge and not eaten:
            snake.pop(0)

        # Check if the snake has collided with itself (overlapping segments)
        if len(set(snake)) != len(snake):
            print("Game over!") # TODO: game over logic
        else:
            print("Doing good!")

        # Render
        frame = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(8)]
        frame[apple[0]][apple[1]][apple[2]] = 1 # render apple
        for segment in snake: # render snake
            frame[segment[0]][segment[1]][segment[2]] = 1
        protocol_frame = to_protocol(frame)

        # Make each game tick take about 0.2 seconds without capping frame rate
        t1 = time()
        while t1 - t < 0.2:
            send_frame(protocol_frame)
            t1 = time()
        t = time()

if __name__ == "__main__":
    animate_snake(999999)