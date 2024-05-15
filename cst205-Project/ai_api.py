import asyncio
import aiohttp

async def fetch_data(url, session, info):
  async with session.post(url, json=info[0], headers=info[1]) as response:
    return await response.json()


async def get_ai_images(prompt):
  url = "https://stable-diffusion9.p.rapidapi.com/generate"

  payload = {
      "prompt": prompt,
      "style": "photographic",
      "seed": 0
  }

  headers = {
      "content-type": "application/json",
      "X-RapidAPI-Key": "8867e01260msha8bab1ebf526c14p17d658jsn7f3f3686d05d",
      "X-RapidAPI-Host": "stable-diffusion9.p.rapidapi.com"
  }

  async with aiohttp.ClientSession() as session:
    tasks = [fetch_data(url, session, [payload, headers]) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    return results
