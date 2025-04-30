# game.py
import pygame
import pymunk
import random



def run_game_loop(game_state):
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
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
        
        cam_x = game_state.ball_body.position.x - SCREEN_WIDTH // 2
        cam_y = game_state.ball_body.position.y - SCREEN_HEIGHT // 2
        
        def to_screen(pos):
            return int(pos.x - cam_x), int(pos.y - cam_y)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_state.is_running = False
                
                
        # Apply random forces to the balls
        for shape in game_state.space.shapes:
            if isinstance(shape, pymunk.Circle) and shape.body != game_state.ball_body:
                fx = random.randint(-12500, 12500)
                fy = random.randint(-50000, -10000)
                shape.body.apply_force_at_local_point((fx, fy), (0, 0))

        game_state.step(dt)

        # Drawing
        screen.fill((30, 30, 30))
        x, y = int(game_state.ball_body.position.x), int(game_state.ball_body.position.y)
        pygame.draw.circle(screen, (0, 255, 0), to_screen(game_state.ball_body.position), 25)
        
        # Draw all static shapes
        for shape in game_state.space.shapes:
            if isinstance(shape, pymunk.Segment):
                pygame.draw.line(screen, (200, 200, 200),
                                to_screen(shape.a), to_screen(shape.b), int(shape.radius))
            elif isinstance(shape, pymunk.Poly):
                points = [shape.body.local_to_world(v) for v in shape.get_vertices()]
                pygame.draw.polygon(screen, (200, 200, 200), [to_screen(p) for p in points])
            elif isinstance(shape, pymunk.Circle):
                pygame.draw.circle(screen, (255, 0, 0), to_screen(shape.body.position), int(shape.radius))
                
        # Minimap drawing
        minimap.fill((0, 0, 0))
        ball_pos = game_state.ball_body.position
        ball_minimap_pos = (int(ball_pos.x * scale_x), int(ball_pos.y * scale_y))
        pygame.draw.circle(minimap, (0, 255, 0), ball_minimap_pos, 3)

        
        
        """ for shape in game_state.space.shapes:
            if isinstance(shape, pymunk.Segment):
                pygame.draw.line(minimap, (200, 200, 200),
                                (int(shape.a.x * scale_x), int(shape.a.y * scale_y)),
                                (int(shape.b.x * scale_x), int(shape.b.y * scale_y)), int(shape.radius * scale_x))
            elif isinstance(shape, pymunk.Poly):
                points = [shape.body.local_to_world(v) for v in shape.get_vertices()]
                pygame.draw.polygon(minimap, (200, 200, 200), [(int(p.x * scale_x), int(p.y * scale_y)) for p in points])
        screen.blit(minimap, (screen.get_width() - MINIMAP_WIDTH - 10, 10))  # top-right corner """
        pygame.display.flip()

    pygame.quit()

