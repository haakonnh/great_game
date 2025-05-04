# gamestate.py
import pymunk
import random 
import asyncio


class GameState:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.time = 0
        self.is_running = True
        self.score = 0
        self.ammo = 50
        self.lives = 5
        self.last_time_hit = -999
        self.radar_radius = 500
        
        self.bullets = []
        self.enemies = []
        self.obstacles = []
    
        
        self.obstacles = generate_random_obstacles(self.space, count=2000, size_range=(40, 300), map_bounds=(10000, 10000))
        
        # Add a triangle ship
        self.ship_triangle_points = [(-12, -8), (0, 12), (12, -8)]
        ship_moment = pymunk.moment_for_poly(1, self.ship_triangle_points)
        self.ship_body = pymunk.Body(1, ship_moment)
        self.ship_body.position = (0, 0)
        self.ship_shape = pymunk.Poly(self.ship_body, self.ship_triangle_points)
        self.ship_shape.elasticity = 0.3
        self.ship_shape.friction = 0.5
        self.ship_shape.collision_type = 1  # Set a collision type for the ship
        
        self.space.add(self.ship_body, self.ship_shape)
        
        # Add more balls
        for _ in range(125):
            enemy_body = pymunk.Body(1, 100)
            enemy_body.position = (random.randint(-10000, 10000), random.randint(-10000, 10000))
            enemy_shape = pymunk.Circle(enemy_body, 50)
            enemy_shape.elasticity = 0.8
            enemy_shape.collision_type = 3  # Set a collision type for the enemy balls
            self.enemies.append((enemy_body, enemy_shape))  # Store reference if needed
            self.space.add(enemy_body, enemy_shape)
        

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
        
        # Ceeate collision handlers
        self.bullet_wall = self.space.add_collision_handler(2, 4)
        self.bullet_wall.post_solve = self._handle_bullet_wall
        
        # Bullet hits red ball
        self.bullet_enemy = self.space.add_collision_handler(2, 3)
        self.bullet_enemy.post_solve = self._handle_bullet_enemy
        
        """ # Ship hits red ball
        self.ship_enemy = self.space.add_collision_handler(1, 3)
        self.ship_enemy.post_solve = self._handle_ship_object """
        
        # Ship hits wall
        self.ship_wall = self.space.add_collision_handler(1, 4)
        self.ship_wall.post_solve = self._handle_ship_object

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
        fy = act.get('fy', 0)
        shoot = act.get('shoot', False)
        clockwise_rotate = act.get('clockwise_rotate', False)
        counter_clockwise_rotate = act.get('counter_clockwise_rotate', False)
        if shoot:
            self.fire_bullet()
        
        if clockwise_rotate:
            self.ship_body.apply_force_at_local_point((0, -100), (-12, -8))
        
        if counter_clockwise_rotate:
            self.ship_body.apply_force_at_local_point((0, -100), (12, -8))
        
        self.ship_body.apply_force_at_local_point((0, fy))
            
    def fire_bullet(self):
        # Bullet settings
        radius = 5
        mass = 0.1
        speed = 1200

        # Get ship tip in world coordinates
        local_tip = (0, -25)  # Same as tip in ship_triangle_points
        tip_world = self.ship_body.local_to_world(local_tip)
        angle = self.ship_body.angle
        velocity = pymunk.Vec2d(0, -speed).rotated(angle)  # forward in ship direction

        # Create bullet body & shape
        moment = pymunk.moment_for_circle(mass, 0, radius)
        bullet_body = pymunk.Body(mass, moment)
        bullet_body.position = tip_world
        bullet_body.velocity = velocity

        bullet_shape = pymunk.Circle(bullet_body, radius)
        bullet_shape.elasticity = 0.5
        bullet_shape.collision_type = 2  # Set your own collision type for bullets

        # Add to space
        self.space.add(bullet_body, bullet_shape)
        self.bullets.append((bullet_body, bullet_shape))
        
        self.ammo = self.ammo - 1
        
    def _handle_bullet_wall(self, arbiter, space, data):
        bullet_shape = arbiter.shapes[0]  # bullets are always first
        self._remove_bullet(bullet_shape)
        return True

    def _handle_bullet_enemy(self, arbiter, space, data):
        bullet_shape, enemy_shape = arbiter.shapes
        self._remove_bullet(bullet_shape)
        self._remove_enemy(enemy_shape)
        self.score += 1  # Increment score on hit
        return True

    def _remove_bullet(self, bullet_shape):
        for body, shape in self.bullets:
            if shape == bullet_shape:
                self.space.remove(body, shape)
                self.bullets.remove((body, shape))
                break

    def _remove_enemy(self, enemy_shape):
        for body, shape in self.enemies:
            if shape == enemy_shape:
                self.space.remove(body, shape)
                self.enemies.remove((body, shape))
                break
    
            
    def _handle_ship_object(self, arbiter, space, data):
        cooldown = 0.5  # 1 second cooldown
        if self.time - self.last_time_hit >= cooldown:
            self.lives -= 1
            self.last_time_hit = self.time
        return True

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
        shape.collision_type = 4

        space.add(body, shape)
        obstacles.append((body, shape))  # Store reference if needed
    return obstacles
