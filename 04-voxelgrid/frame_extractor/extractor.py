import cv2
import numpy as np
import os

# Extract frame data from video.mp4 and save each frame to frames_8x8_binary directory

# Load video
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Create output folder
output_folder = "frames_8x8_binary"
os.makedirs(output_folder, exist_ok=True)

frame_num = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # End of video
    
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize to 8x8
    small_frame = cv2.resize(gray_frame, (8, 8), interpolation=cv2.INTER_AREA)

    # Apply threshold (convert to 0 or 1)
    _, binary_frame = cv2.threshold(small_frame, 128, 1, cv2.THRESH_BINARY)

    # Rotate to change coordinate system
    rotated_frame = np.rot90(binary_frame, k=3)

    # Save as numpy array
    np.save(os.path.join(output_folder, f"frame_{frame_num:04d}.npy"), rotated_frame)
    
    frame_num += 1

cap.release()
print("Binary frames extracted and saved!")
