import asyncio
import httpx
import random

async def run_interactor():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.get("http://localhost:8000/state")
                if resp.status_code == 200:
                    nearby_enemies = resp.json().get("enemies", [])
                    nearby_obstacles = resp.json().get("obstacles", [])
                    print("[Interactor] State:", len(nearby_enemies), len(nearby_obstacles), " enemies, obstacles")
                    
                else:
                    print("[Interactor] Error:", resp.status_code, resp.text)
            except Exception as e:
                print("[Interactor] Error:", e)
            # call get /act
            fy = random.randint(-3000, 0)
            # rotational force
            frot = random.randint(0, 200)
            try:
                resp = await client.post("http://localhost:8000/act", json={
                    "action": {
                        "fy": fy,
                        "clockwise_rotate": (True, frot) if random.randint(0, 1) == 1 else (False, 0),
                        "counter_clockwise_rotate": (True, frot) if random.randint(0, 1) == 1 else (False, 0),
                        "shoot": True if random.randint(0, 1) == 1 else False
                    }
                })
                if resp.status_code == 200:
                    print("[Interactor] Response:", resp.json())
            except Exception as e:
                print("[Interactor] Error:", e)
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run_interactor())