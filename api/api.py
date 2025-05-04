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
        # Radar
        ship_pos = game_state.ship_body.position
        ship_angle = game_state.ship_body.angle
        
        # Enemies
        nearby_enemies = []
        for (body, shape) in game_state.enemies:
            query = shape.point_query(ship_pos)
            if abs(query.distance) < game_state.radar_radius:
                nearby_enemies.append({
                    "x": body.position.x,
                    "y": body.position.y,
                    "radius": shape.radius if hasattr(shape, "radius") else None
                })
        
        # Static obstacles
        nearby_obstacles = []
        for (body, shape) in game_state.obstacles:
            query = shape.point_query(ship_pos)
            if abs(query.distance) <= game_state.radar_radius:
                size = shape.bb.right - shape.bb.left, shape.bb.top - shape.bb.bottom
                nearby_obstacles.append({
                    "x": body.position.x,
                    "y": body.position.y,
                    "width": size[0],
                    "height": size[1]
                })
        
        return {
            "ship": {
                "x": ship_pos.x,
                "y": ship_pos.y,
                "angle": ship_angle,
                "angular_velocity": game_state.ship_body.angular_velocity,
                "velocity": game_state.ship_body.velocity,
                "ammo": game_state.ammo,
                "lives": game_state.lives,
                "score": game_state.score
            },
            "enemies": nearby_enemies,
            "obstacles": nearby_obstacles,
            "radar_radius:": game_state.radar_radius,
            "time": game_state.time,

        }

    @app.post("/act")
    def act(action: dict):
        game_state.apply_action(action)
        return {"status": "action taken"}

    return app
