import pymunk
import asyncio
from .objects import GameObject
from engine.state import agent_state, obstacles



class GameWorld:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.agent_objects = {}
        self.agent_state = {}

    def add_object(self, obj):
        obj.add_to_space(self.space)
        self.objects.append(obj)
        
    def add_agent(self, agent_name, position):
        obj = GameObject(position)
        self.agent_objects[agent_name] = obj
        self.agent_state[agent_name] = {
            "position": position,
            "angle": 0,
            "body": obj.body
        }
        self.space.add(obj.body, obj.shape)
    async def run(self, tick_rate=60):
        dt = 1.0 / tick_rate
        while True:
            self.space.step(dt)

            # Update state from body positions
            for agent_name, agent in agent_state.items():
                body = agent.get("body")
                if body:
                    agent["position"] = list(body.position)
                    agent["angle"] = body.angle

            await asyncio.sleep(dt)
