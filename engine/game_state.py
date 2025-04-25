# gamestate.py
import pymunk

class GameState:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.time = 0
        self.is_running = True

        # Add a ball
        self.ball_body = pymunk.Body(1, 100)
        self.ball_body.position = (300, 300)
        self.ball_shape = pymunk.Circle(self.ball_body, 25)
        self.ball_shape.elasticity = 0.8
        self.space.add(self.ball_body, self.ball_shape)
        
        # Ground obstacle
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, (0, 580), (800, 580), 5)
        floor_shape.friction = 1.0
        floor_shape.elasticity = 0.9
        self.space.add(floor_body, floor_shape)
        
        # Top Wall
        wall_t = pymunk.Segment(floor_body, (0, 0), (800, 0), 5)
        wall_t.elasticity = 0.9
        self.space.add(wall_t)
        
        # --- Left wall ---
        wall_l = pymunk.Segment(floor_body, (0, 0), (0, 600), 5)
        wall_l.elasticity = 0.9
        self.space.add(wall_l)

        # --- Right wall ---
        wall_r = pymunk.Segment(floor_body, (800, 0), (800, 600), 5)
        wall_r.elasticity = 0.9
        self.space.add(wall_r)

        # --- Platform ---
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_body.position = (400, 400)
        platform = pymunk.Poly.create_box(platform_body, (300, 20))

        platform.elasticity = 0.8
        self.space.add(platform_body, platform)

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
        act = action.get('action')
        fx, fy = act.get('fx'), act.get('fy')
        print(f"Applying force: {fx} {fy}")
        self.ball_body.apply_force_at_local_point((fx, fy))
