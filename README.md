# 🚀 Game Simulation Engine – Phase 1 Delivery

A modular 2D game simulation framework for real-time agent-based interaction. Includes a physics engine, FastAPI interface, simple dummy bot, and Pygame-based visualization.

# Objective
The objective of the game is to shoot as many red ball enemies as possible before losing all 5 lives or going out of ammo (later on, ammo pickups will be added to the game). Hitting walls or getting hit by balls take one life away.

## 📁 Project Structure

### API
The API exposes certain endpoints that can be accessed by the other parts of the project and external agents. Some endpoints are HTTP GET's which provide certain state information about the game, while HTTP POST endpoints make it possible for agents to actually dynamically interact with the game.

#### GET
/state is the endpoint which will give the agent useful information about the world and the ship. The response will contain the following ship information:
* x and y coordinates
* ship angle
* ship angular velocity
* ship velocity
* remaining ammo
* remaining lives
* score (amount of enemies shot)

Additionally, the agent will get radar information including:
* radar radius
* nearby enemies (their cooordinates and radius)
* nearby obstacles (coordinates, width and height)

#### POST
The game is currently single-player so it will be run locally, where an agent can connect to the localhost and POST to the API with the following parameters:
* fy (force in y direction = thrust)
* clockwise rotation force 
* counter clockwiser rotation force
* shoot (true or false)

Clockwise and counter clockwise rotation force is passed by a tuple on this form: (Boolean (true or false), force). If no force is passed in, no force is applied rotationally. For example, if the angular velocity is very high one way, the agent can restabilize by applying a rotational force the other way.

### Agents
Reserved for code implementing an agent for playing the game. The agent should use the API to GET and POST to interact with the game.

### Visualizer 
Runs a loop in 60 frames per second, visualizing the current state of the game.

### Engine
Implements physics and keeps track of state in the GameWorld object, exposed on the API.

# RUN
Install requirements.
python run_demo.py
