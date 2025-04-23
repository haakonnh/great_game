import asyncio
import subprocess
from engine.world import GameWorld
from engine.objects import GameObject
from engine.state import agent_state, obstacles

async def run_game_engine(world: GameWorld):
    await world.run(tick_rate=60)  # Run the game engine in the background
    return world

""" async def run_agent():
    proc = await asyncio.create_subprocess_exec(
        "python", "agents/dummy_agent.py"
    )
    return proc """

async def run_visualizer():
    print("[🖼️] Starting visualizer...")
    proc = await asyncio.create_subprocess_exec(
        "python", "visualizer/visualizer.py"
    )
    return proc

async def run_api():
    proc = await asyncio.create_subprocess_exec(
        "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"
    )
    return proc

async def main():
    print("[🧠] Starting simulation engine, API, agent, and visualizer...")
    world = GameWorld()
    obj = GameObject((100, 100))
    world.add_object(obj)
    world.add_agent("agent1", (100, 100))  # Add an agent to the world
    world.add_agent("agent2", (200, 200))  # Add another agent to the world
    world.add_agent("agent3", (300, 300))  # Add another agent to the world
    world.add_agent("agent4", (400, 400))  # Add another agent to the world
    print("[🧠] World initialized with agents:", agent_state)
    api_proc = await run_api()
    #await asyncio.sleep(1)  # Let API spin up first

    visualizer_proc = await run_visualizer()
    #agent_proc = await run_agent()

    try:
        await run_game_engine(world)  # Run the game engine in the background
    except KeyboardInterrupt:
        print("\n[❌] Shutting down...")
        api_proc.terminate()
        visualizer_proc.terminate()
        #agent_proc.terminate()


if __name__ == "__main__":
    asyncio.run(main())