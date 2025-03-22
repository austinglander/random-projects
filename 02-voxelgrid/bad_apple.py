from cube_control import send_frame
from time import time, sleep
from cube_utils import to_protocol, empty_frame, write_string
import numpy as np

# https://www.youtube.com/watch?v=FtutLA63Cp8
LAST_FRAME = 6571

def display_count_down(seconds: int):
    """
    Displays a countdown on the cube for "seconds" seconds.\n
    The last digit displayed in the countdown will be a 1\n
    Inputs larger than 99 will be counted properly but displayed as 99 until the count falls low enough.
    """
    count_down = seconds
    while (count_down > 0):
        t0 = time()
        out_frame = empty_frame()
        right = 7
        for digit in reversed(str(min(count_down, 99))):
            write_string(out_frame, digit)
            right -= 4
        send_frame(to_protocol(out_frame))
        count_down -= 1
        # Sleep for 1 second, factoring in the time it took for the above operations
        sleep(1 - (time() - t0))


def bad_apple():
    """
    Plays bad apple on the front 8x8 plane of the cube
    """
    # Requires frames to be stored in the relative path bad_apple_frames/frame_0000.npy
    # T-up the first frame before starting our rendering loop
    frame_count = 0
    t0 = time()
    while frame_count <= LAST_FRAME:
        # Ready up our next frame
        frame = empty_frame()
        frame[0] = np.load(f"bad_apple_frames/frame_{frame_count:04}.npy").tolist()
        send_frame(to_protocol(frame))
        frame_count += 1

        # Use current frame number to compute how long to sleep for.
        # This prevents floating point errors from accumulating throughout the video.
        # Max to prevent passing a negative to sleep if above operations take too long
        # Sleep the difference between how long we want to have passed and how long has actually passed
        sleep(max(0, 1/30*frame_count - (time() - t0)))

    # Send the last frame
    send_frame(to_protocol(frame))
        
    print("Done!")


if __name__ == "__main__":
    display_count_down(3)
    bad_apple()