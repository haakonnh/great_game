# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_api(game_state):
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/state")
    def get_state():
        return game_state.to_dict()

    @app.post("/act")
    def act(action: dict):
        game_state.apply_action(action)
        return {"status": "force applied"}

    return app
