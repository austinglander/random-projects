# 3D Pong

import keyboard
from cube_utils import to_protocol, write_string, empty_frame
from cube_control import send_frame
from vector import vector
from time import time, sleep
from random import uniform, choice
from bitarray import bitarray

PADDLE_SIZE = 4
BALL_SPEED = 7
COLLISION_TOLERANCE = 0.5 # High tolerance to avoid getting screwed by rounding

left_paddle_pos = [2, 0, 2] # AKA P1
right_paddle_pos = [2, 7, 2] # AKA P2
left_moved = False
right_moved = False
def update_paddles(e: keyboard.KeyboardEvent) -> None:
    """
    Callback function to update paddle position on keypress
    """
    global left_moved, right_moved
    # Paddle positions are stored as the coordinate nearest to (0,y,0)
    key = e.name
    # Left player
    if key == "w": # Move paddle up
        left_paddle_pos[2] = max(0, min(8-PADDLE_SIZE, left_paddle_pos[2]+1))
        left_moved = True
    if key == "a":
        left_paddle_pos[0] = max(0, min(8-PADDLE_SIZE, left_paddle_pos[0]+1))
        left_moved = True
    if key == "s":
        left_paddle_pos[2] = max(0, min(8-PADDLE_SIZE, left_paddle_pos[2]-1))
        left_moved = True
    if key == "d":
        left_paddle_pos[0] = max(0, min(8-PADDLE_SIZE, left_paddle_pos[0]-1))
        left_moved = True
    
    # Right player
    if key == "up":
        right_paddle_pos[2] = max(0, min(8-PADDLE_SIZE, right_paddle_pos[2]+1))
        right_moved = True
    if key == "left":
        right_paddle_pos[0] = max(0, min(8-PADDLE_SIZE, right_paddle_pos[0]-1))
        right_moved = True
    if key == "down":
        right_paddle_pos[2] = max(0, min(8-PADDLE_SIZE, right_paddle_pos[2]-1))
        right_moved = True
    if key == "right":
        right_paddle_pos[0] = max(0, min(8-PADDLE_SIZE, right_paddle_pos[0]+1))
        right_moved = True

def score_frame(frame: list[list[bitarray]], left_score: int, right_score: int) -> None:
    """
    Writes the game score onto the given frame in the plane x=0
    """
    write_string(frame, str(right_score))
    # Insert dashed line
    frame[0][3][3] = 1
    frame[0][4][3] = 1
    write_string(frame, str(left_score), pos=(0,2,5))

def game_frame(frame: list[list[bitarray]], ball: vector = None) -> None:
    """
    Loads paddles and ball into the frame (ball is optional)
    """
    for i in range(PADDLE_SIZE):
        for j in range(PADDLE_SIZE):
            frame[left_paddle_pos[0]+i][left_paddle_pos[1]][left_paddle_pos[2]+j] = 1
            frame[right_paddle_pos[0]+i][right_paddle_pos[1]][right_paddle_pos[2]+j] = 1
    if ball is not None:
        rounded_ball = ball.get_rounded_pos()
        frame[rounded_ball[0]][rounded_ball[1]][rounded_ball[2]] = 1

def win_animation(winner: bool) -> None:
    """
    Play a win animation for the winner\n
    winner - False -> left wins; True -> right wins
    """
    frame = empty_frame()
    count = 0
    for y in (range(8) if not winner else reversed(range(8))):
        for x in range(8):
            for z in range(8):
                frame[x][y][z] = 1
        send_frame(to_protocol(frame))
        sleep(0.4) # "Accelerate" the moving wall
        count += 1
    sleep(2)


def hitting_paddle(pos: vector, paddle: bool) -> bool:
    """
    pos - position vector to check collision on\n
    paddle - boolean indicating which paddle to check collision for. False -> left; True -> right\n
    Returns True if pos is within the xz bounds of the paddle and False otherwise.
    """
    match paddle:
        case False: # Left
            x_bound = left_paddle_pos[0] - COLLISION_TOLERANCE <= pos.x < (left_paddle_pos[0] + PADDLE_SIZE) + COLLISION_TOLERANCE
            z_bound = left_paddle_pos[2] - COLLISION_TOLERANCE <= pos.z < (left_paddle_pos[2] + PADDLE_SIZE) + COLLISION_TOLERANCE

        case True: # Right
            x_bound = right_paddle_pos[0] - COLLISION_TOLERANCE <= pos.x < (right_paddle_pos[0] + PADDLE_SIZE) + COLLISION_TOLERANCE
            z_bound = right_paddle_pos[2] - COLLISION_TOLERANCE <= pos.z < (right_paddle_pos[2] + PADDLE_SIZE) + COLLISION_TOLERANCE
    if x_bound and z_bound:
        return True
    return False

def play_pong():
    global left_moved, right_moved
    keyboard.on_press(update_paddles)
    ball = vector(3.5, 3.5, 3.5)
    # Generate random velocity vector and scale it up to some desired speed constant
    # Guarantee we start with a significant y-velocity to keep the game moving
    velocity = vector(uniform(-1, 1), choice([uniform(-1,-0.5), uniform(0.5, 1)]), uniform(-1, 1))
    velocity = velocity.scale(BALL_SPEED / velocity.mag())

    t0 = time()
    gamestate = 0 # 0 - continue; 1 - point for left; 2 - point for right
    left_score = 8
    right_score = 8
    while True:
        # Sit here until both players have moved
        while not (left_moved and right_moved):
            frame = empty_frame()
            game_frame(frame, ball)
            send_frame(to_protocol(frame))
            t0 = time()
        # Physics logic
        dt = time() - t0
        t0 = time()
        # Look ahead to the next ball position to see if we should process a collision before next position update
        next_pos = ball + velocity.scale(dt) # velocity in grid units / second
        if next_pos.x < 0 or next_pos.x > 7:
            velocity.x *= -1
        # Ball leaving left side
        if next_pos.y < 0.5:
            if hitting_paddle(next_pos, False):
                velocity.y *= -1 # Caught ball
                # TODO: angle logic
            else:
                gamestate = 2 # Point for right
        # Ball leaving right side
        if next_pos.y > 6.5:
            if hitting_paddle(next_pos, True):
                velocity.y *= -1 # Caught ball
                # TODO: angle logic
            else:
                gamestate = 1 # Point for left
        if next_pos.z < 0 or next_pos.z > 7:
            velocity.z *= -1
        ball += velocity.scale(dt)

        frame = empty_frame()
        # Check gamestate to determine next action
        if gamestate == 0: # Continue game, render next frame
            game_frame(frame, ball)
            send_frame(to_protocol(frame))
            continue

        # Below logic only runs when someone scores
        if gamestate == 1: # Point for left
            left_score += 1
        if gamestate == 2: # Point for right
            right_score += 1
        score_frame(frame, left_score, right_score)
        send_frame(to_protocol(frame))
        sleep(2)

        # Game end logic 
        if left_score == 9:
            winner = "p1"
            win_animation(False)
            break
        if right_score == 9:
            winner = "p2"
            win_animation(True)
            break

        # Reset game state for next round
        t0 = time()
        gamestate = 0
        left_moved = False
        right_moved = False
        ball = vector(3.5, 3.5, 3.5)
        velocity = vector(uniform(-1, 1), choice([uniform(-1,-0.5), uniform(0.5, 1)]), uniform(-1, 1))
        velocity = velocity.scale(BALL_SPEED / velocity.mag())


    # Game end loop
    count = 0
    while True:
        frame = empty_frame()
        write_string(frame, winner if count % 2 else "GG")
        send_frame(to_protocol(frame))
        sleep(1)
        count += 1




if __name__ == "__main__":
    play_pong()