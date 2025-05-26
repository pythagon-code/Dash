# Dash #

## Description ##

This is my Dash game, a clone of Geometry Dash. It features the main gameplay and included 4 playable layouts. The game is made in pygame.

The game has blocks, spikes of 4 rotations, and orbs with unique effects.

Here is the mechanics of each orb:

- Yellow Orb: Jump
- Pink Orb: Small jump
- Blue Orb: Reverse gravity
- Green Orb: Reverse gravity and jump (in that order)
- Red Orb: Big Jump
- Black Orb: Push toward gravity

## Run Project ##

To successfully run the game, you must have Python installed.

On a terminal, run:
```bash
git clone https://github.com/pythagon-code/Dash.git

cd Dash
```

Then create a virtual environment to isolate dependencies:

```bash
python -m venv .venv
```

Activate the environment on Linux/Mac:
```bash
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\Activate.ps1
```

Now install requirements:
```
python -m pip install -r requirements.txt
```

Run the program:
```
python main.py
```