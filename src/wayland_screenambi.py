import subprocess
import io
from PIL import Image
import paramiko
from time import sleep
import socket

# Send new Data to Pi per SSH
def modify_remote_file(hostname, port, username, password, filepath, new_content):
    """
    Connects to a remote server via SSH, replaces the content of a file, and closes the connection.

    Args:
        hostname (str): The hostname or IP address of the remote server.
        port (int): The SSH port number (usually 22).
        username (str): The username for SSH authentication.
        password (str): The password for SSH authentication.
        filepath (str): The absolute path to the file on the remote server.
        new_content (str): The new content to write to the file.
    """
    ssh_client = None  # Initialize ssh_client to None
    try:
        # Create a new SSH client object
        ssh_client = paramiko.SSHClient()
        # Set SSH key parameters to auto accept unknown hosts
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)

        # Open an SFTP (Secure File Transfer Protocol) session
        sftp_client = ssh_client.open_sftp()

        # Write the new content to the file
        with sftp_client.open(filepath, 'w') as remote_file:
            remote_file.write(new_content)

        # Close the SFTP session
        sftp_client.close()

    except Exception as e:
        print(f"An error occurred during SSH file modification: {e}")
    finally:
        # Ensure the SSH connection is closed
        if ssh_client:
            ssh_client.close()

def get_wayland_screenshot():
    """
    Captures a screenshot on Wayland using grim and returns it as a PIL Image object.
    Requires 'grim' to be installed and available in the system's PATH.
    """
    try:
        # Execute grim to capture the screen and output PNG data to stdout
        # '-t png' specifies PNG format, '-' indicates stdout
        result = subprocess.run(['grim', '-t', 'png', '-'], capture_output=True, check=True)
        # Load the PNG data from stdout into a PIL Image
        im = Image.open(io.BytesIO(result.stdout))
        return im
    except FileNotFoundError:
        print("Error: 'grim' command not found. Please install grim for Wayland screenshots (e.g., 'sudo apt install grim' or 'sudo pacman -S grim').")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error taking screenshot with grim: {e}")
        print(f"grim stderr: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during screenshot capture: {e}")
        return None

computer_name = socket.gethostname()
samples = 10 # Number of samples to take across the screen width

while True:
    im = get_wayland_screenshot()
    if im is None:
        sleep(1) # Wait a bit before retrying if screenshot failed
        continue

    width, height = im.size
    y = height // 2 # Use integer division for pixel coordinates

    content = ""
    
    #Get Coloursamples
    for i in range(samples + 1): # Loop from 0 to samples inclusive
        currentx = int((width - 1) / samples * i)
        try:
            pixel_color = im.getpixel((currentx, y))
            # Ensure pixel_color is a tuple of 3 (R, G, B) even if it's RGBA
            if len(pixel_color) == 4:
                content += f"{pixel_color[0]},{pixel_color[1]},{pixel_color[2]}\n"
            else:
                content += f"{pixel_color[0]},{pixel_color[1]},{pixel_color[2]}\n"
            #print(f"The color of the pixel at ({currentx}, {y}) is: {pixel_color}")
        except IndexError:
            print(f"The coordinates ({currentx}, {y}) are outside the screenshot bounds for current image size ({width}, {height}).")
        except Exception as e:
            print(f"An error occurred while getting pixel color: {e}")
    
    # Only attempt to modify remote file if content was successfully generated
    if content:
        # Replace with your actual Pi's IP, username, password, and file path
        modify_remote_file("192.168.178.34", 22, "jeremy", "wüsstest du gern :/", "led-control/color_" + computer_name, content)
        
        # This part writes to a local file, useful for debugging or local logging
        if content.count("\n") == samples + 1:
            with open("color_testpc.txt", "w") as f:
                    f.write(content)
    
    sleep(0.1)