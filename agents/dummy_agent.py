import asyncio
import random
import httpx  # install with: pip install httpx

SERVER_URL = "http://localhost:8000"
AGENT_NAMES = ["agent1", "agent2"]  # Add more agent names as needed

async def run_dummy_agent(name):
    async with httpx.AsyncClient() as client:
        while True:
            move_y = random.choice([-2.5, 2.5])  # or just use -1 if you prefer
            move_x = random.choice([-2.5, 2.5])  # or just use -1 if you prefer   
            print(f"[Agent] Sending move_y: {move_y}")

            try:
                response = await client.post(
                    f"{SERVER_URL}/agent/command",
                    json={
                        "agent_name": name,
                        "move_x": move_x,
                        "move_y": move_y,
                    }
                )
                print("[Agent] Response:", response.json())
            except Exception as e:
                print("[Agent] Error:", e)


async def main():
    tasks = [run_dummy_agent(name) for name in AGENT_NAMES]
    await asyncio.gather(*tasks)

# Want to run 
if __name__ == "__main__":
    asyncio.run(main())
