import random
import asyncio
from playwright.async_api import async_playwright
import time

URL = "https://cyberninja-1.blogspot.com/2023/02/simple-python-program.html"
CLICKS_PER_BATCH = 100
WAIT_BETWEEN_BATCHES = 300  # 5 minutes in seconds
CONCURRENT_CLICKS = 5  # Limit concurrent browser instances

async def simulate_valid_click(playwright, url: str, simulation_number: int, semaphore):
    async with semaphore:
        browser = await playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-software-rasterizer"]
        )
        page = await browser.new_page()

        await page.route("**/*.{png,jpg,jpeg,css,svg,woff,woff2,ttf}", lambda route: route.abort())

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(2)

            x = random.randint(100, 300)
            y = random.randint(100, 500)
            await page.mouse.click(x, y)

            print(f"✅ Click {simulation_number} completed at ({x}, {y})")

        except Exception as e:
            print(f"❌ Error on click {simulation_number}: {e}")

        finally:
            await browser.close()

async def run_batch(batch_number: int):
    async with async_playwright() as playwright:
        semaphore = asyncio.Semaphore(CONCURRENT_CLICKS)
        tasks = [
            simulate_valid_click(playwright, URL, i + 1, semaphore)
            for i in range(CLICKS_PER_BATCH)
        ]
        await asyncio.gather(*tasks)
        print(f"🛑 Batch {batch_number} of {CLICKS_PER_BATCH} clicks completed.")
        print(f"⏳ Waiting 5 minutes before next batch...")

def run_forever():
    batch = 1
    while True:
        asyncio.run(run_batch(batch))
        batch += 1
        time.sleep(WAIT_BETWEEN_BATCHES)

# Start the loop
run_forever()
