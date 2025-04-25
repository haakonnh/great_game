# run_demo.py
from engine.game_state import GameState
from game.game import run_game_loop
from api.api import create_api
import threading
import uvicorn

def start_api(app):
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def main():
    game_state = GameState()
    app = create_api(game_state)

    # Start API in background thread
    api_thread = threading.Thread(target=start_api, args=(app,), daemon=True)
    api_thread.start()

    # Start game loop in main thread
    run_game_loop(game_state)

if __name__ == "__main__":
    main()
