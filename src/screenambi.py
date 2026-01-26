from PIL import ImageGrab
import paramiko
from time import sleep
import socket
#Send new Data to Pi per SSH
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
        print(f"An error occurred: {e}")
    finally:
        # Ensure the SSH connection is closed
        if ssh_client:
            ssh_client.close()

# Grab a screenshot of the screen
try:
    im = ImageGrab.grab()
except OSError as e:
    print(f"Error grabbing screenshot: {e}")
    exit()

width, height = im.size
computer_name = socket.gethostname()

# Define the coordinates of the pixel you want to get
samples = 10
y = height / 2

while True:
    try:
        im = ImageGrab.grab()
    except OSError as e:
        print(f"Error grabbing screenshot: {e}")
        exit()
    content = ""

    #Get Coloursamples
    i=0
    while(i<=samples):
        
        currentx=int((width-1)/samples*i)
        try:
            pixel_color = im.getpixel((currentx, y))
            content += f"{pixel_color[0]},{pixel_color[1]},{pixel_color[2]}\n"
            #print(f"The color of the pixel at ({currentx}, {y}) is: {pixel_color}")
        except IndexError:
            print(f"The coordinates ({currentx}, {y}) are outside the screenshot bounds.")
        except Exception as e:
            print(f"An error occurred: {e}")
        i+=1
    sleep(0.1)
    modify_remote_file("192.168.178.34",22,"jeremy","wüsstest du gern :/","led-control/color_"+computer_name,content)
    if content.count("\n") == samples+1:
        with open("color_testpc.txt", "w") as f:
                f.write(content)