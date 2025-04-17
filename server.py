from flask import Flask, request, redirect, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LED Control</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background-color: #f4f4f4;
      margin: 0;
    }
    .container {
      background: #fff;
      padding: 30px 20px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      text-align: center;
      max-width: 400px;
      width: 90%;
    }
    h1 {
      margin-bottom: 20px;
    }
    input[type="number"] {
      width: 60px;
      padding: 8px;
      margin: 5px;
    }
    button {
      font-size: 1.1rem;
      padding: 10px 20px;
      margin-top: 10px;
      border: none;
      border-radius: 5px;
      background-color: #4CAF50;
      color: white;
      cursor: pointer;
    }
    button:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>LED Control</h1>
    <form method="POST">
      <label>Red:</label>
      <input type="number" name="red" min="0" max="255" value="{{ red }}"><br>
      <label>Green:</label>
      <input type="number" name="green" min="0" max="255" value="{{ green }}"><br>
      <label>Blue:</label>
      <input type="number" name="blue" min="0" max="255" value="{{ blue }}"><br><br>
      <button type="submit" name="toggle" value="1">{{ button_text }}</button>
    </form>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def control():
    check_path = "./check.txt"
    color_path = "./color.txt"

    # Load current values
    running = os.path.exists(check_path) and open(check_path).read().strip() == "1"
    current_color = "2,2,10"
    if os.path.exists(color_path):
        current_color = open(color_path).read().strip()

    red, green, blue = map(int, current_color.split(','))

    if request.method == 'POST':
        # Update color
        red = int(request.form.get('red', red))
        green = int(request.form.get('green', green))
        blue = int(request.form.get('blue', blue))
        with open(color_path, "w") as f:
            f.write(f"{red},{green},{blue}")

        # Toggle running state
        running = not running
        with open(check_path, "w") as f:
            f.write("1" if running else "0")

    return render_template_string(HTML, red=red, green=green, blue=blue,
                                  button_text="Stop" if running else "Start")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
