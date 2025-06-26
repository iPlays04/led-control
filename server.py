from flask import Flask, request, redirect, render_template_string, url_for
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
      <label for="loading">Flat Colour</label><br>

      <input type="radio" id="pulse" name="color_mode" value="1" {% if color_mode == 1 %}checked{% endif %} onclick="showInputs()">
      <label for="pulse">Colour Pulse</label><br>

      <input type="radio" id="hex" name="color_mode" value="2" {% if color_mode == 2 %}checked{% endif %} onclick="showInputs()">
      <label for="hex">Sparkles</label><br>
      
      <input type="radio" id="rng" name="color_mode" value="3" {% if color_mode == 3 %}checked{% endif %} onclick="showInputs()">
      <label for="rng">Disco</label><br>

      <input type="radio" id="rainbow" name="color_mode" value="4" {% if color_mode == 4 %}checked{% endif %} onclick="showInputs()">
      <label for="rainbow">Rainbow</label><br>

      <input type="radio" id="dyngrad" name="color_mode" value="5" {% if color_mode == 5 %}checked{% endif %} onclick="showInputs()">
      <label for="dyngrad">Dynamic Gradient</label><br>

      <input type="radio" id="grad" name="color_mode" value="6" {% if color_mode == 6 %}checked{% endif %} onclick="showInputs()">
      <label for="grad">Static Gradient</label>

      <br><br>

      <div id="loadingInputs" class="hidden">
          
      </div>

      <div id="pulseInputs" class="hidden">
          <label>Pulse Length:</label>
          <input type="range" id="rangepulseo1" name="pulse_o1" min="1" max="100" value="{{ o1 }}">
          <input type="number" id="numpulseo1" name="pulse_o1" min="1" max="100" value="{{ o1 }}"><br>
          <label>Pulse Brightness:</label>
          <input type="range" id="rangepulseo2" name="pulse_o2" min="0" max="255" value="{{ o2 }}">
          <input type="number" id="numpulseo2" name="pulse_o2" min="0" max="255" value="{{ o2 }}"><br>
      </div>

      <div id="hexInputs" class="hidden">
          <label>Sparkle Amount</label>
          <input type="range" id="rangesparkleo1" name="hex_o1" min="1" max="100" value="{{ o1 }}">
          <input type="number" id="numsparkleo1" name="hex_o1" min="1" max="100" value="{{ o1 }}"><br>
          <label>Sparkle Brightness:</label>
          <input type="range" id="rangesparkleo2" name="hex_o2" min="0" max="255" value="{{ o2 }}">
          <input type="number" id="numsparkleo2" name="hex_o2" min="0" max="255" value="{{ o2 }}"><br>
      </div>   

      <div id="rngInputs" class="hidden">
          
      </div> 

      <div id="rainbowInputs" class="hidden">
          
      </div>

      <div id="dyngradInputs" class="hidden">
          <label>Red:</label>
          <input type="range" id="redo1" name="dyngrad_o1" min="0" max="255" value="{{ o1 }}">
          <input type="number" id="numredo1" name="dyngrad_o1" min="0" max="255" value="{{ o1 }}"><br>

          <label>Green:</label>
          <input type="range" id="greeno2" name="dyngrad_o2" min="0" max="255" value="{{ o2 }}">
          <input type="number" id="numgreeno2" name="dyngrad_o2" min="0" max="255" value="{{ o2 }}"><br>

          <label>Blue:</label>
          <input type="range" id="blueo3" name="dyngrad_o3" min="0" max="255" value="{{ o3 }}">
          <input type="number" id="numblueo3" name="dyngrad_o3" min="0" max="255" value="{{ o3 }}">
      </div>

      <div id="gradInputs" class="hidden">
          <label>Red:</label>
          <input type="range" id="sredo1" name="grad_o1" min="0" max="255" value="{{ o1 }}">
          <input type="number" id="snumredo1" name="grad_o1" min="0" max="255" value="{{ o1 }}"><br>

          <label>Green:</label>
          <input type="range" id="sgreeno2" name="grad_o2" min="0" max="255" value="{{ o2 }}">
          <input type="number" id="snumgreeno2" name="grad_o2" min="0" max="255" value="{{ o2 }}"><br>

          <label>Blue:</label>
          <input type="range" id="sblueo3" name="grad_o3" min="0" max="255" value="{{ o3 }}">
          <input type="number" id="snumblueo3" name="grad_o3" min="0" max="255" value="{{ o3 }}">
      </div>

      <br><br>

      <button type="submit" name="toggle" value="1">{{button_text}}</button>
    </form>
    <script>


        document.getElementById('pulse').addEventListener('click', function() {
            document.getElementById('rangepulseo1').value = 10;
            document.getElementById('numpulseo1').value = 10;
            document.getElementById('rangepulseo2').value = 10;
            document.getElementById('numpulseo2').value = 10;
        });

        document.getElementById('hex').addEventListener('click', function() {
            document.getElementById('rangesparkleo1').value = 10;
            document.getElementById('numsparkleo1').value = 10;
            document.getElementById('rangesparkleo2').value = 10;
            document.getElementById('numsparkleo2').value = 10;
        });

        document.getElementById('dyngrad').addEventListener('click', function() {
            document.getElementById('redo1').value = 10;
            document.getElementById('numredo1').value = 10;
            document.getElementById('greeno2').value = 10;
            document.getElementById('numgreeno2').value = 10;
            document.getElementById('blueo3').value = 10;
            document.getElementById('numblueo3').value = 10;
        });

        document.getElementById('grad').addEventListener('click', function() {
            document.getElementById('sredo1').value = 10;
            document.getElementById('snumredo1').value = 10;
            document.getElementById('sgreeno2').value = 10;
            document.getElementById('snumgreeno2').value = 10;
            document.getElementById('sblueo3').value = 10;
            document.getElementById('snumblueo3').value = 10;
        });

        function disableAllInputs() {
            const allInputs = document.querySelectorAll(
              '#pulseInputs input, #hexInputs input, #dyngradInputs input, #gradInputs input'
            );
            allInputs.forEach(input => input.disabled = true);
        }

        function enableInputsIn(containerId) {
            const inputs = document.querySelectorAll(`#${containerId} input`);
            inputs.forEach(input => input.disabled = false);
        }

        function showInputs() {
            const allSections = ['loadingInputs', 'pulseInputs', 'hexInputs', 'rngInputs', 'rainbowInputs', 'dyngradInputs', 'gradInputs'];
            disableAllInputs();  // <--- wichtig
            allSections.forEach(id => document.getElementById(id).classList.add('hidden'));

            if (document.getElementById('loading').checked) {
                document.getElementById('loadingInputs').classList.remove('hidden');
            } else if (document.getElementById('pulse').checked) {
                document.getElementById('pulseInputs').classList.remove('hidden');
                enableInputsIn('pulseInputs'); // <--- wichtig
            } else if (document.getElementById('hex').checked) {
                document.getElementById('hexInputs').classList.remove('hidden');
                enableInputsIn('hexInputs');
            } else if (document.getElementById('dyngrad').checked) {
                document.getElementById('dyngradInputs').classList.remove('hidden');
                enableInputsIn('dyngradInputs');
            } else if (document.getElementById('grad').checked) {
                document.getElementById('gradInputs').classList.remove('hidden');
                enableInputsIn('gradInputs');
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
        syncValues(document.getElementById('rangesparkleo1'), document.getElementById('numsparkleo1'));
        syncValues(document.getElementById('rangesparkleo2'), document.getElementById('numsparkleo2'));
        syncValues(document.getElementById('redo1'), document.getElementById('numredo1'));
        syncValues(document.getElementById('greeno2'), document.getElementById('numgreeno2'));
        syncValues(document.getElementById('blueo3'), document.getElementById('numblueo3'));
        syncValues(document.getElementById('sredo1'), document.getElementById('snumredo1'));
        syncValues(document.getElementById('sgreeno2'), document.getElementById('snumgreeno2'));
        syncValues(document.getElementById('sblueo3'), document.getElementById('snumblueo3'));
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
    running = False
    current_color = "2,2,10,0,0,0"
    if os.path.exists(color_path):
        current_color = open(color_path).read().strip()

    red, green, blue, color_mode, o1, o2, o3 = map(int, current_color.split(','))

    if request.method == 'POST':
        # Update color and mode from form
        red = int(request.form.get('red', red))
        green = int(request.form.get('green', green))
        blue = int(request.form.get('blue', blue))
        color_mode = int(request.form.get('color_mode', color_mode))

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

        # Write updated color data
        with open(color_path, "w") as f:
            f.write(f"{red},{green},{blue},{color_mode},{o1},{o2},{o3}")

        # Toggle running state only if toggle button was pressed
        if 'toggle' in request.form:
            running = os.path.exists(check_path) and open(check_path).read().strip() == "1"
            running = not running
            with open(check_path, "w") as f:
                f.write("1" if running else "0")

        # Redirect to GET route to avoid resubmitting form on refresh
        return redirect(url_for('control'))

    # For GET requests, load the current running state
    if os.path.exists(check_path):
        running = open(check_path).read().strip() == "1"

    return render_template_string(HTML, red=red, green=green, blue=blue,
                                  button_text="Stop" if running else "Start",
                                  color_mode=color_mode, o1=o1, o2=o2, o3=o3)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
