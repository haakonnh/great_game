import pygame
import asyncio
import httpx  # install with: pip install httpx
import threading

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Shared data between fetcher and renderer
objects_data = {}


def start_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    color_index = 0
    running = True
    
    while running:
        screen.fill((30, 30, 30))
        agents = objects_data.get("agents", {})
        for obj_id, obj in agents.items():
            x, y = obj.get("position", [0, 0])
            pygame.draw.circle(screen, colors[color_index], (int(x), int(y)), 10)
            color_index = (color_index + 1) % len(colors)
        obstacles = objects_data.get("obstacles", [])
        for obj in obstacles:
            x, y = obj.get("position", [0, 0])
            width, height = obj.get("size", [50, 50])
            pygame.draw.rect(screen, (255, 255, 255), (int(x), int(y), width, height))    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        color_index = 0  # Reset color index for next frame
        pygame.display.flip()
        clock.tick(2)

    pygame.quit()
    os._exit(0)  # Kill asyncio loop thread

async def fetch_objects():
    global objects_data
    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.get("http://localhost:8000/world/objects")
                if resp.status_code == 200:
                    objects_data = resp.json()
            except Exception as e:
                print("[❌] Error fetching:", e)
            await asyncio.sleep(0.04)  # fetch 20 times per second

def run_visualizer():
    # Start Pygame in its own thread
    threading.Thread(target=start_pygame, daemon=True).start()

    # Run asyncio loop in main thread
    asyncio.run(fetch_objects())

run_visualizer()
