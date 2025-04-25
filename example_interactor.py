import asyncio
import httpx

async def run_interactor():
    async with httpx.AsyncClient() as client:
        while True:
            # call get /act
            try:
                resp = await client.get("http://localhost:8000/state")
                if resp.status_code == 200:
                    print("[Interactor] Response:", resp.json())
            except Exception as e:
                print("[Interactor] Error:", e)
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_interactor())