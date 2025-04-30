# run_demo.py
from engine.game_state import GameState
from game.game import run_game_loop
from api.api import create_api
import threading
import uvicorn
import asyncio

def start_api(app):
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
# This function runs the dummy interactor in a separate process
async def run_dummy():
    proc = await asyncio.create_subprocess_exec(
        "python", "example_interactor.py"
    )
    return proc

async def main():
    game_state = GameState()
    
    # Create API and run it in a separate thread
    app = create_api(game_state)
    api_thread = threading.Thread(target=start_api, args=(app,), daemon=True)
    api_thread.start()
    
    # Run the dummy interactor 
    dummy_proc = await run_dummy()

    # Start game loop in main thread
    run_game_loop(game_state)
    
    dummy_proc.terminate()

# Asyncio is used to run asynchronous functions in main
if __name__ == "__main__":
    asyncio.run(main())
