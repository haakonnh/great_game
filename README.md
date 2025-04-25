# 🚀 Game Simulation Engine – Phase 1 Delivery

A modular 2D game simulation framework for real-time agent-based interaction. Includes a physics engine, FastAPI interface, simple dummy bot, and Pygame-based visualization.

## 📁 Project Structure

### API
The API exposes certain endpoints that can be accessed by the other parts of the project and external agents. Some endpoints are HTTP GET's which provide certain state information about the game, while HTTP POST endpoints make it possible for agents to actually dynamically interact with the game.

### Agents
Reserved for code implementing an agent for playing the game. The agent should use the API to GET and POST to interact with the game.

### Visualizer 
Runs a loop in 60 frames per second, visualizing the current state of the game.

### Engine
Implements physics and keeps track of state in the GameWorld object, exposed on the API.


# RUN
python run_demo.py
