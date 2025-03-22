from cube_control import send_frame
from cube_utils import to_protocol, write_string, empty_frame
import keyboard

display_string = ""
def update_text(e: keyboard.KeyboardEvent) -> None:
    """
    Callback function to update the displayed string on keypress
    """
    global display_string
    if not e.name.isalnum():
        return
    if e.name == "space":
        display_string += " "
    else:
        display_string += e.name
    display_string = display_string[-2:]


def write_from_keyboard():
    """
    Displays the last two keys pressed on the keyboard to the front plane of the cube
    """
    keyboard.on_press(update_text)
    while True:
        frame = empty_frame()
        write_string(frame, display_string)
        send_frame(to_protocol(frame))

if __name__ == "__main__":
    write_from_keyboard()