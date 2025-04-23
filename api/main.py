from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Command(BaseModel):
    agent_name: str
    move_x: float = 0.0
    move_y: float = 0.0

@app.get("/agent/status")
def get_status():
    return {"status": "ok", "position": [0, 0], "angle": 0}

@app.post("/agent/command")
def send_command(cmd: Command):
    from engine.state import agent_state, obstacles
    print("Command received:", cmd)
    ag1 = agent_state.get(cmd.agent_name)
    x, y = ag1["position"]
    agent_state.get(cmd.agent_name)["position"] = [x + cmd.move_x, y + cmd.move_y]
    print("Updated position:", agent_state.get("agent1")["position"])
    return {"ack": True}

@app.get("/world/objects")
def get_all_objects():
    from engine.state import agent_state, obstacles
    return {
        "agents": agent_state,
        "obstacles": obstacles
    }