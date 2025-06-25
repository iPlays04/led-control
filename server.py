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
      background-color: #40513B;
      margin: 0;
    }
    .container {
      background: #EDF1D6;
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
      background-color: #9DC08B;
      color: white;
      cursor: pointer;
    }
    button:hover {
      background-color: #609966;
    }
    .hidden {
            display: none;
        }
  </style>
</head>
<body>
  <div class="container">
    <h1>LED Control</h1>
    <form method="POST">

      <label>Red:</label>
      <input type="range" id="red" name="red" min="0" max="255" value="{{ red }}">
      <input type="number" id="numred" name="red" min="0" max="255" value="{{ red }}"><br>

      <label>Green:</label>
      <input type="range" id="green" name="green" min="0" max="255" value="{{ green }}">
      <input type="number" id="numgreen" name="green" min="0" max="255" value="{{ green }}"><br>

      <label>Blue:</label>
      <input type="range" id="blue" name="blue" min="0" max="255" value="{{ blue }}">
      <input type="number" id="numblue" name="blue" min="0" max="255" value="{{ blue }}">
      
      <br><br>

      <label>Select Effect:</label><br>
      <input type="radio" id="loading" name="color_mode" value="0" {% if color_mode == 0 %}checked{% endif %} onclick="showInputs()">
      <label for="loading">Loading</label><br>

      <input type="radio" id="pulse" name="color_mode" value="1" {% if color_mode == 1 %}checked{% endif %} onclick="showInputs()">
      <label for="pulse">Pulse</label><br>

      <input type="radio" id="hex" name="color_mode" value="2" {% if color_mode == 2 %}checked{% endif %} onclick="showInputs()">
      <label for="hex">HEX</label>
      
      <br><br>

      <div id="loadingInputs" class="hidden">
          
      </div>

      <div id="pulseInputs" class="hidden">
          <label>Pulse Length:</label>
          <input type="range" id="rangepulseo1" name="o1" min="1" max="50" value="{{ o1 }}">
          <input type="number" id="numpulseo1" name="o1" min="1" max="50" value="{{ o1 }}"><br>
          <label>Pulse Brightness:</label>
          <input type="range" id="rangepulseo2" name="o2" min="0" max="30" value="{{ o2 }}">
          <input type="number" id="numpulseo2" name="o2" min="0" max="30" value="{{ o2 }}"><br>
      </div>

      <div id="hexInputs" class="hidden">
          <label>HEX Code:</label>
          <input type="text" id="hexCode" name="hexCode" value="#000000"><br>
      </div>    

      <br><br>

      <button type="submit" name="toggle" value="1">{{ button_text }}</button>
    </form>
    <script>
        function showInputs() {
            document.getElementById('loadingInputs').classList.add('hidden');
            document.getElementById('pulseInputs').classList.add('hidden');
            document.getElementById('hexInputs').classList.add('hidden');

            if (document.getElementById('loading').checked) {
                document.getElementById('loadingInputs').classList.remove('hidden');
            } else if (document.getElementById('pulse').checked) {
                document.getElementById('pulseInputs').classList.remove('hidden');
            } else if (document.getElementById('hex').checked) {
                document.getElementById('hexInputs').classList.remove('hidden');
            }
        }
        window.onload = showInputs;
        function syncValues(rangeInput, numberInput) {
            rangeInput.addEventListener('input', function() {
                numberInput.value = rangeInput.value;
            });

            numberInput.addEventListener('input', function() {
                rangeInput.value = numberInput.value;
            });
        }

        syncValues(document.getElementById('red'), document.getElementById('numred'));
        syncValues(document.getElementById('green'), document.getElementById('numgreen'));
        syncValues(document.getElementById('blue'), document.getElementById('numblue'));
        syncValues(document.getElementById('rangepulseo1'), document.getElementById('numpulseo1'));
        syncValues(document.getElementById('rangepulseo2'), document.getElementById('numpulseo2'));
    </script>
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
    current_color = "2,2,10,0,0,0"
    if os.path.exists(color_path):
        current_color = open(color_path).read().strip()

    red, green, blue, color_mode, o1, o2 = map(int, current_color.split(','))

    if request.method == 'POST':
        # Update color
        red = int(request.form.get('red', red))
        green = int(request.form.get('green', green))
        blue = int(request.form.get('blue', blue))
        color_mode = int(request.form.get('color_mode', color_mode))
        o1 = int(request.form.get('o1', o1))
        o2 = int(request.form.get('o2', o2))
        with open(color_path, "w") as f:
            f.write(f"{red},{green},{blue},{color_mode},{o1},{o2}")

        # Toggle running state
        running = not running
        with open(check_path, "w") as f:
            f.write("1" if running else "0")

    return render_template_string(HTML, red=red, green=green, blue=blue,
                                  button_text="Stop" if running else "Start", color_mode=color_mode, o1=o1, o2=o2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
