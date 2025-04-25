# gamestate.py
import pymunk

class GameState:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.time = 0
        self.is_running = True

        # Add a ball
        self.ball_body = pymunk.Body(1, 100)
        self.ball_body.position = (100, 100)
        self.ball_shape = pymunk.Circle(self.ball_body, 25)
        self.ball_shape.elasticity = 0.8
        self.space.add(self.ball_body, self.ball_shape)

    def step(self, dt):
        self.space.step(dt)
        self.time += dt

    def to_dict(self):
        return {
            "time": self.time,
            "ball_position": [self.ball_body.position.x, self.ball_body.position.y]
        }

    def apply_action(self, action):
        # Simple action: apply force to ball
        fx, fy = action.get("fx", 0), action.get("fy", 0)
        self.ball_body.apply_force_at_local_point((fx, fy))
