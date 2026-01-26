from flask import Flask, request, redirect, render_template, url_for
import os

app = Flask(__name__)
#app.template_folder = os.path.abspath('./')

@app.route('/', methods=['GET', 'POST'])
def control():
    check_path = "./check.txt"
    color_path = "./color.txt"

    # --- MODIFIED SECTION FOR color.txt ---
    # Load current values
    running = False
    current_color = "2,2,10,0,0,0,0,0,0,100" # Default value if file doesn't exist
    if os.path.exists(color_path):
        try:
            # Only attempt to read if the file exists
            file_content = open(color_path).read().strip()
            if file_content: # Ensure content is not empty
                current_color = file_content
            # You can remove the print statement here, or keep it for debugging
            # print(current_color)
        except Exception as e:
            print(f"Error reading color.txt: {e}. Using default color.")
            # Fallback to default if there's an issue reading
    else:
        # If color.txt doesn't exist, create it with default values
        with open(color_path, "w") as f:
            f.write(current_color)
    # --- END MODIFIED SECTION ---

    # Ensure current_color has enough values before splitting
    # This assumes current_color will always be a comma-separated string
    # with at least 10 values based on your default.
    try:
        red, green, blue, speed, color_mode, o1, o2, o3, isAmbi, brightness = map(int, current_color.split(','))
    except ValueError as e:
        print(f"Error parsing current_color: {e}. Using default values.")
        red, green, blue, speed, color_mode, o1, o2, o3, isAmbi, brightness = 2,2,10,0,0,0,0,0,0,100


    if request.method == 'POST':
        # Update color and mode from form
        red = int(request.form.get('red', red))
        green = int(request.form.get('green', green))
        blue = int(request.form.get('blue', blue))
        color_mode = int(request.form.get('color_mode', color_mode))
        speed = int(request.form.get('speed', speed))
        brightness = int(request.form.get('brightness', brightness)) # Corrected default for brightness

        if color_mode == 1:
            o1 = int(request.form.get('pulse_o1', o1))
            o2 = int(request.form.get('pulse_o2', o2))
            o3 = 0
        elif color_mode == 2:
            o1 = int(request.form.get('hex_o1', o1))
            o2 = int(request.form.get('hex_o2', o2))
            o3 = 0
        elif color_mode == 5:
            o1 = int(request.form.get('dyngrad_o1', o1))
            o2 = int(request.form.get('dyngrad_o2', o2))
            o3 = int(request.form.get('dyngrad_o3', o3))
        elif color_mode == 6:
            o1 = int(request.form.get('grad_o1', o1))
            o2 = int(request.form.get('grad_o2', o2))
            o3 = int(request.form.get('grad_o3', o3))
        else:
            o1 = o2 = o3 = 0

        # isAmbi needs to be handled carefully as it's a toggle
        if 'ambitoggle' in request.form:
            isAmbi = 1 if not isAmbi else 0 # Toggle the integer value

        # Write updated color data
        with open(color_path, "w") as f:
            f.write(f"{red},{green},{blue},{speed},{color_mode},{o1},{o2},{o3},{int(isAmbi)},{brightness}")

        # Toggle running state only if toggle button was pressed
        if 'toggle' in request.form:
            # Read current state safely
            if os.path.exists(check_path):
                running = open(check_path).read().strip() == "1"
            else:
                running = False # Default if file doesn't exist

            running = not running
            with open(check_path, "w") as f:
                f.write("1" if running else "0")

        # Redirect to GET route to avoid resubmitting form on refresh
        return redirect(url_for('control'))

    # For GET requests, load the current running state
    if os.path.exists(check_path):
        running = open(check_path).read().strip() == "1"
    else:
        running = False # Default if file doesn't exist

    return render_template('index.html', red=red, green=green, blue=blue,speed=speed,
                                  button_text="Stop" if running else "Start",
                                  button_text2="Enable Ambilight" if not isAmbi else "Disable Ambilight",
                                  color_mode=color_mode, o1=o1, o2=o2, o3=o3,brightness=brightness)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)