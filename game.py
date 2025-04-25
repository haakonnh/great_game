# game.py
import pygame

def run_game_loop(game_state):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running and game_state.is_running:
        dt = clock.tick(60) / 1000.0  # 60 FPS in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_state.is_running = False

        game_state.step(dt)

        # Drawing
        screen.fill((30, 30, 30))
        x, y = int(game_state.ball_body.position.x), int(game_state.ball_body.position.y)
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 25)
        pygame.display.flip()

    pygame.quit()

