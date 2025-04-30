# gamestate.py
import pymunk
import random 


class GameState:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.time = 0
        self.is_running = True
        
        self.obstacles = generate_random_obstacles(self.space, count=750, size_range=(40, 300), map_bounds=(5000, 5000))

        # Add a ball
        self.ball_body = pymunk.Body(1, 100)
        self.ball_body.position = (300, 300)
        self.ball_shape = pymunk.Circle(self.ball_body, 25)
        self.ball_shape.elasticity = 0.8
        self.space.add(self.ball_body, self.ball_shape)
        
        pymunk.im
        
        
        """ # Ground obstacle
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, (0, 580), (800, 580), 5)
        floor_shape.friction = 1.0
        floor_shape.elasticity = 0.9
        self.space.add(floor_body, floor_shape)
        
        # Top Wall
        wall_t = pymunk.Segment(floor_body, (0, 0), (800, 0), 5)
        wall_t.elasticity = 0.9
        self.space.add(wall_t)
        
        

        # --- Right wall ---
        wall_r = pymunk.Segment(floor_body, (800, 0), (800, 600), 5)
        wall_r.elasticity = 0.9
        self.space.add(wall_r) """

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


# Function to generate randomly placed and sized obstacles
def generate_random_obstacles(space, count=10, map_bounds=(1200, 800), size_range=(50, 500)):
    obstacles = []

    for _ in range(count):
        width = random.randint(*size_range)
        height = random.randint(*size_range)
        x = random.randint(-map_bounds[0] + width // 2, map_bounds[0] - width // 2)
        y = random.randint(-map_bounds[1] + height // 2, map_bounds[1] - height // 2)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (x, y)
        shape = pymunk.Poly.create_box(body, (width, height))
        shape.elasticity = 0.8

        space.add(body, shape)
        obstacles.append((body, shape))  # Store reference if needed
    return obstacles
