# gamestate.py
import pymunk
import random 


class GameState:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.time = 0
        self.is_running = True
        
        self.obstacles = generate_random_obstacles(self.space, count=2000, size_range=(40, 300), map_bounds=(10000, 10000))

        # Add a ball
        self.ball_body = pymunk.Body(1, 100)
        self.ball_body.position = (-9000, -9000)
        self.ball_shape = pymunk.Circle(self.ball_body, 25)
        self.ball_shape.elasticity = 0.8
        self.space.add(self.ball_body, self.ball_shape)
        
        # Add more balls
        for _ in range(50):
            enemy_body = pymunk.Body(1, 100)
            enemy_body.position = (random.randint(-10000, 10000), random.randint(-10000, 10000))
            enemy_shape = pymunk.Circle(enemy_body, 100)
            enemy_shape.elasticity = 0.8
            self.space.add(enemy_body, enemy_shape)
        
        
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
        
        # Bottom boundary
        bottom_boundary_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        bottom_boundary_body.position = (0, 10000)
        bottom_boundary = pymunk.Poly.create_box(bottom_boundary_body, (20000, 50))
        bottom_boundary.elasticity = 0.8

        self.space.add(bottom_boundary_body, bottom_boundary)

        # Left boundary
        left_boundary_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        left_boundary_body.position = (-10000, 0)
        left_boundary = pymunk.Poly.create_box(left_boundary_body, (50, 20000))
        left_boundary.elasticity = 0.8
        self.space.add(left_boundary_body, left_boundary)
        
        # Right boundary
        right_boundary_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        right_boundary_body.position = (10000, 0)
        right_boundary = pymunk.Poly.create_box(right_boundary_body, (50, 20000))
        right_boundary.elasticity = 0.8
        self.space.add(right_boundary_body, right_boundary)
        
        # Top boundary
        top_boundary_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        top_boundary_body.position = (0, -10000)
        top_boundary = pymunk.Poly.create_box(top_boundary_body, (20000, 50))
        top_boundary.elasticity = 0.8
        self.space.add(top_boundary_body, top_boundary)
        self.space.add(platform_body, platform)

        """ platform.elasticity = 0.8
        self.space.add(platform_body, platform) """

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
