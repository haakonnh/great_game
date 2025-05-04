import asyncio
import httpx
import random

async def run_interactor():
    async with httpx.AsyncClient() as client:
        while True:
            # call get /act
            fy = random.randint(-3000, 0)
            try:
                resp = await client.post("http://localhost:8000/act", json={
                    "action": {
                        "fy": fy,
                        "clockwise_rotate": True if random.randint(0, 1) == 1 else False,
                        "counter_clockwise_rotate": True if random.randint(0, 1) == 1 else False,
                        "shoot": True if random.randint(1, 1) == 1 else False
                    }
                })
                if resp.status_code == 200:
                    print("[Interactor] Response:", resp.json())
            except Exception as e:
                print("[Interactor] Error:", e)
            await asyncio.sleep(0.35)

if __name__ == "__main__":
    asyncio.run(run_interactor())