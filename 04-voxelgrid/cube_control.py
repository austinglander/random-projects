# Since I don't have all of my friend's code (or a sweet 8x8x8 voxel grid), this 
# should serve to model it so I can view my animations


import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from cube_utils import from_protocol
import time

# Set to TRUE to make background white and points blue.
# Set to FALSE to make background black and points white
WHITE_BG = True
POINT_SIZE = 30

# ChatGPT thank you for the PointRenderer 🙏
class OpenGLPointRenderer:
    def __init__(self, spacing=1.0, allow_camera_control=True):
        self.movement_keys = set()
        self.spacing = spacing
        self.points = []
        self.camera_position = [-17, 7, 7]  # Initial camera position
        self.camera_rotation = [80, 16]  # Yaw (left/right), Pitch (up/down)
        self.mouse_last_pos = None
        self.allow_camera_control = allow_camera_control
        self.init_window()
    
    def init_window(self):
        if not glfw.init():
            raise Exception("GLFW can't be initialized")
        
        self.window = glfw.create_window(1920, 1440, "3D Point Renderer", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created")
        
        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for proper 3D rendering
        glEnable(GL_POINT_SMOOTH)
        glPointSize(POINT_SIZE)
        
        # Set background color to white or black
        if WHITE_BG:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 0.0)
        
        # Set up input callbacks
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)  # Hide cursor for FPS-like control
    
    def set_camera_control(self, enabled):
        """Enable or disable camera control dynamically"""
        self.allow_camera_control = enabled

    def update_points(self, points_3d):
        """Correctly maps the coordinate system to OpenGL's format."""
        self.points = []
        for x in range(len(points_3d)):
            for y in range(len(points_3d[x])):
                for z in range(len(points_3d[x][y])):
                    if points_3d[x][y][z] == 1:
                        self.points.append((x * self.spacing, z * self.spacing, y * self.spacing))  # Correct axis mapping
    
    def move_camera(self, dx=0, dy=0, dz=0):
        """Moves the camera position by (dx, dy, dz) in local space."""
        yaw_rad = math.radians(self.camera_rotation[0])
        
        self.camera_position[0] += dx * math.cos(yaw_rad) - dz * math.sin(yaw_rad)
        self.camera_position[2] += dz * math.cos(yaw_rad) + dx * math.sin(yaw_rad)
        self.camera_position[1] += dy
    
    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        if not self.allow_camera_control:
            return # Ignore movement keys if camera control is disabled

        if action == glfw.PRESS:
            self.movement_keys.add(key)
        elif action == glfw.RELEASE:
            self.movement_keys.discard(key)
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        move_speed = 0.04  # Reduce step size for smoother motion
        if action == glfw.PRESS:
            if key == glfw.KEY_W:
                self.move_camera(dz=-move_speed)
            elif key == glfw.KEY_S:
                self.move_camera(dz=move_speed)
            elif key == glfw.KEY_A:
                self.move_camera(dx=-move_speed)
            elif key == glfw.KEY_D:
                self.move_camera(dx=move_speed)
            elif key == glfw.KEY_Q:
                self.move_camera(dy=move_speed)
            elif key == glfw.KEY_E:
                self.move_camera(dy=-move_speed)
        
        if action == glfw.REPEAT:
            if key == glfw.KEY_W:
                self.move_camera(dz=-move_speed)
            elif key == glfw.KEY_S:
                self.move_camera(dz=move_speed)
            elif key == glfw.KEY_A:
                self.move_camera(dx=-move_speed)
            elif key == glfw.KEY_D:
                self.move_camera(dx=move_speed)
            elif key == glfw.KEY_Q:
                self.move_camera(dy=move_speed)
            elif key == glfw.KEY_E:
                self.move_camera(dy=-move_speed)
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        """Handles keyboard input for camera movement."""
        move_speed = 0.5
        if action in (glfw.PRESS, glfw.REPEAT):
            if key == glfw.KEY_W:
                self.move_camera(dz=-move_speed)  # Move forward
            elif key == glfw.KEY_S:
                self.move_camera(dz=move_speed)  # Move backward
            elif key == glfw.KEY_A:
                self.move_camera(dx=-move_speed)  # Move left
            elif key == glfw.KEY_D:
                self.move_camera(dx=move_speed)  # Move right
            elif key == glfw.KEY_Q:
                self.move_camera(dy=move_speed)  # Move down
            elif key == glfw.KEY_E:
                self.move_camera(dy=-move_speed)  # Move up
    
    def mouse_callback(self, window, xpos, ypos):
        """Handles mouse movement for camera rotation."""
        if not self.allow_camera_control:
            return # Ignore mouse input if camera control is disabled

        if self.mouse_last_pos is None:
            self.mouse_last_pos = (xpos, ypos)
            return
        
        dx, dy = xpos - self.mouse_last_pos[0], ypos - self.mouse_last_pos[1]
        self.mouse_last_pos = (xpos, ypos)
        
        sensitivity = 0.1
        self.camera_rotation[0] += dx * sensitivity  # Yaw
        self.camera_rotation[1] += dy * sensitivity  # Pitch
        self.camera_rotation[1] = max(-89, min(89, self.camera_rotation[1]))  # Limit pitch to avoid flip
    
    def draw_wireframe_box(self):
        """Draws a black wireframe box from (-0.5,-0.5,-0.5) to (7.5,7.5,7.5) with a solid black bottom face."""
        # Make the frame different shades of gray
        if WHITE_BG:
            glColor3f(0.75, 0.75, 0.75)
        else:
            glColor3f(0.4, 0.4, 0.4)

        # Draw solid bottom face
        glBegin(GL_QUADS)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(7.5, -0.5, -0.5)
        glVertex3f(7.5, -0.5, 7.5)
        glVertex3f(-0.5, -0.5, 7.5)
        glEnd()
        
        # Draw wireframe

        glBegin(GL_LINES)
        for x in (-0.5, 7.5):
            for y in (-0.5, 7.5):
                glVertex3f(x, y, -0.5)
                glVertex3f(x, y, 7.5)
        
        for x in (-0.5, 7.5):
            for z in (-0.5, 7.5):
                glVertex3f(x, -0.5, z)
                glVertex3f(x, 7.5, z)
        
        for y in (-0.5, 7.5):
            for z in (-0.5, 7.5):
                glVertex3f(-0.5, y, z)
                glVertex3f(7.5, y, z)
        
        glEnd()
    
    def render(self):
        self.update_movement()
        """Renders the current frame and returns control to the caller."""
        if glfw.window_should_close(self.window):
            glfw.terminate()
            return
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Set up perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100)  # Field of view, aspect ratio, near/far plane
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glRotatef(self.camera_rotation[1], 1, 0, 0)  # Pitch (up/down)
        glRotatef(self.camera_rotation[0], 0, 1, 0)  # Yaw (left/right)
        
        glTranslatef(-self.camera_position[0], -self.camera_position[1], -self.camera_position[2])  # Apply camera position
        
        self.draw_wireframe_box()  # Draw the wireframe box
        
        # Render points
        glBegin(GL_POINTS)
        if WHITE_BG:
            glColor3f(0.0, 0.0, 1.0) # Light blue points
        else:
            glColor3f(1.0, 1.0, 1.0) # White points
        for x, y, z in self.points:
            glVertex3f(x, y, z)
        glEnd()
        
        glfw.swap_buffers(self.window)
        glfw.poll_events()
    
    def update_movement(self):
        move_speed = 0.01  # Adjust speed as needed
        for key in self.movement_keys:
            if key == glfw.KEY_W:
                self.move_camera(dz=-move_speed)
            elif key == glfw.KEY_S:
                self.move_camera(dz=move_speed)
            elif key == glfw.KEY_A:
                self.move_camera(dx=-move_speed)
            elif key == glfw.KEY_D:
                self.move_camera(dx=move_speed)
            elif key == glfw.KEY_Q:
                self.move_camera(dy=move_speed)
            elif key == glfw.KEY_E:
                self.move_camera(dy=-move_speed)

    def close(self):
        """Closes the GLFW window safely."""
        glfw.terminate()

# Usage Example:
# renderer = OpenGLPointRenderer(spacing=2.0)
# while True:
#     points = some_function_that_computes_points()
#     renderer.update_points(points)
#     renderer.render()


renderer = OpenGLPointRenderer(allow_camera_control=True)
def send_frame(frame: bytearray) -> None:
    """
    Renders a frame passed as input.\n
    Frames are bytearrays of 64 bytes with the following translation to voxel positions:\n
    Each group of 8 bytes is a z pos starting from the origin (0-7), 
    each byte in the group is an x pos starting from the origin, each 
    bit in the byte is a y pos starting from 7 (7-0) \n
    In other words:\n
    z-pos = i // 8\n
    y-pos = i % 8\n
    x-pos = byte[j] (little endian, where j is the position of a 1)
    """
    # Tell the global renderer to update with the given values
    # (I'm not going to use the protocol)
    time.sleep(0.001) # Chill for a sec so my PC doesn't blow up
    renderer.update_points(from_protocol(frame))
    renderer.render()
