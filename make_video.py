import cv2
import os

# Directory where PNG files are stored
png_dir = '/frames/'

# Function to sort files numerically
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return sorted(data, key=convert)

# Get list of PNG files in directory
png_files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
png_files = sorted_alphanumeric(png_files)

# Determine the width and height from the first image
img = cv2.imread(os.path.join(png_dir, png_files[0]))
height, width, channels = img.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
out = cv2.VideoWriter('genealogy_map.mp4', fourcc, 10.0, (width, height))

# Loop through all PNG files (assuming they are named frame_0.png, frame_1.png, ...)
num_frames = len(png_files)
for i in range(num_frames):
    png_file = os.path.join(png_dir, f'frame_{i}.png')
    img = cv2.imread(png_file)
    out.write(img)  # Write out frame to video

out.release()
cv2.destroyAllWindows()