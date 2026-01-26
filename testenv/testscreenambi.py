from PIL import ImageGrab
from time import sleep
import os # Added for potential path manipulation, though not strictly necessary for this simple case

# Grab a screenshot of the screen initially to get dimensions
try:
    im = ImageGrab.grab()
except OSError as e:
    print(f"Error grabbing screenshot: {e}")
    print("Please ensure you have a display environment and necessary permissions.")
    exit()

width, height = im.size

# Define the coordinates of the pixel you want to get
samples = 10
y = height // 2 # Use integer division for pixel coordinates

# Define the local filename
local_filename = "color_testpc.txt"

print(f"Starting local color sampling. Data will be saved to '{local_filename}'.")
print("Press Ctrl+C to stop the script.")

while True:
    try:
        im = ImageGrab.grab()
    except OSError as e:
        print(f"Error grabbing screenshot: {e}")
        print("Could not grab screenshot. Exiting.")
    
    content = ""

    # Get Colour samples
    for i in range(samples + 1): # Loop from 0 to samples (inclusive)
        currentx = int((width - 1) / samples * i)
        try:
            pixel_color = im.getpixel((currentx, y))
            content += f"{pixel_color[0]},{pixel_color[1]},{pixel_color[2]}\n"
            # print(f"Sampled pixel at ({currentx}, {y}): {pixel_color}") # Uncomment for debugging
        except IndexError:
            print(f"Warning: Coordinates ({currentx}, {y}) are outside the screenshot bounds. Skipping this sample.")
        except Exception as e:
            print(f"An unexpected error occurred during pixel sampling: {e}")
            
    # Save the content to a local file
    try:
        with open(local_filename, "w") as f:
            f.write(content)
        # print(f"Saved {samples + 1} color samples to '{local_filename}'") # Uncomment for debugging
    except IOError as e:
        print(f"Error writing to local file '{local_filename}': {e}")
    
    sleep(0.1) # Pause for a short duration before the next capture