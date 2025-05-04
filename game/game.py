# game.py
import pygame
import pymunk
import random

import math

def rotate_point(point, angle):
    """Rotates a point by angle in radians."""
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x, y = point
    return (x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta)

def transform_triangle(points, position, angle):
    """Applies rotation and translation to each point."""
    transformed = []
    for p in points:
        rp = rotate_point(p, angle)
        tp = (rp[0] + position[0], rp[1] + position[1])
        transformed.append(tp)
    return transformed

import math

# Define your ship's triangle shape (in local coordinates)
SHIP_TRIANGLE = [
    (0, -20),   # tip
    (-15, 15),  # left
    (15, 15)    # right
]

def rotate_point(point, angle):
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x, y = point
    return (
        x * cos_theta - y * sin_theta,
        x * sin_theta + y * cos_theta
    )

def draw_ship(screen, ship_body, cam_x, cam_y):
    # Get position and angle from physics body
    pos = ship_body.position  # pymunk Vec2d
    angle = ship_body.angle   # radians

    # Transform triangle points
    transformed = []
    for p in SHIP_TRIANGLE:
        rotated = rotate_point(p, angle)
        world_x = rotated[0] + pos.x
        world_y = rotated[1] + pos.y
        screen_x = int(world_x - cam_x)
        screen_y = int(world_y - cam_y)
        transformed.append((screen_x, screen_y))

    # Draw the polygon
    pygame.draw.polygon(screen, (0, 200, 255), transformed)



def run_game_loop(game_state):
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 680
    MINIMAP_WIDTH = 200
    MINIMAP_HEIGHT = 200
    scale_x = SCREEN_WIDTH / MINIMAP_WIDTH
    scale_y = SCREEN_HEIGHT / MINIMAP_HEIGHT
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    minimap = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running and game_state.is_running:
        dt = clock.tick(60) / 1000.0  # 60 FPS in seconds
        
        cam_x = game_state.ship_body.position.x - SCREEN_WIDTH // 2
        cam_y = game_state.ship_body.position.y - SCREEN_HEIGHT // 2
        
        def to_screen(pos):
            return int(pos.x - cam_x), int(pos.y - cam_y)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_state.is_running = False
                
        if game_state.ammo <= 0 or game_state.lives <= 0:
            running = False
            game_state.is_running = False
            
            # Display game over message
            font = pygame.font.SysFont("Arial", 50)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            # Show score
            score_text = font.render(f"Score: {game_state.score}", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        
                
        # Apply random forces to the balls
        for shape in game_state.space.shapes:
            if isinstance(shape, pymunk.Circle) and (shape.body, shape) not in game_state.bullets:
                fx = random.randint(-1750, 1750)
                fy = random.randint(-1750, 1750)
                shape.body.apply_force_at_local_point((fx, fy), (0, 0))

        game_state.step(dt)

        # Drawing
        screen.fill((30, 30, 30))
        
        draw_ship(screen, game_state.ship_body, cam_x, cam_y)

        
        # Draw all static shapes
        for shape in game_state.space.shapes:
            if isinstance(shape, pymunk.Segment):
                pygame.draw.line(screen, (200, 200, 200),
                                to_screen(shape.a), to_screen(shape.b), int(shape.radius))
            # If its poly but not the ship
            elif isinstance(shape, pymunk.Poly) and shape.body != game_state.ship_body:
                points = [shape.body.local_to_world(v) for v in shape.get_vertices()]
                pygame.draw.polygon(screen, (200, 200, 200), [to_screen(p) for p in points])
            elif isinstance(shape, pymunk.Circle) and (shape.body, shape) not in game_state.bullets:
                pygame.draw.circle(screen, (255, 0, 0), to_screen(shape.body.position), int(shape.radius))
        for body, shape in game_state.bullets:
            x, y = int(body.position.x - cam_x), int(body.position.y - cam_y)
            pygame.draw.circle(screen, (255, 255, 0), (x, y), int(shape.radius))
            
        font = pygame.font.SysFont("Arial", 30)
        
        score_text = font.render(f"Score: {game_state.score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() - score_text.get_width() - 20, 20))
        
        ammo_text = font.render(f"Ammo: {game_state.ammo}", True, (255, 255, 255))
        screen.blit(ammo_text, (screen.get_width() - ammo_text.get_width() - 20, 60))
        
        lives_text = font.render(f"Lives: {game_state.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (screen.get_width() - lives_text.get_width() - 20, 100))

            
        pygame.display.flip()

    pygame.quit()

