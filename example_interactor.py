import asyncio
import httpx
import random

async def run_interactor():
    async with httpx.AsyncClient() as client:
        while True:
            # call get /act
            fx = random.randint(-25000, 25000)
            fy = random.randint(-50000, 0)
            try:
                resp = await client.post("http://localhost:8000/act", json={
                    "action": {
                        "fx": fx,
                        "fy": fy
                    }
                })
                if resp.status_code == 200:
                    print("[Interactor] Response:", resp.json())
            except Exception as e:
                print("[Interactor] Error:", e)
            await asyncio.sleep(1.5)

if __name__ == "__main__":
    asyncio.run(run_interactor())