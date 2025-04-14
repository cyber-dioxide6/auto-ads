import random
import asyncio
from playwright.async_api import async_playwright

URL = "https://cyberninja-1.blogspot.com/2023/02/simple-python-program.html"
WAIT_BETWEEN_CLICKS = 30  # 30 seconds

async def simulate_valid_click(playwright, url: str, click_number: int):
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

        print(f"✅ Click {click_number} completed at ({x}, {y})")

    except Exception as e:
        print(f"❌ Error on click {click_number}: {e}")

    finally:
        await browser.close()

async def continuous_clicks():
    click_number = 1
    async with async_playwright() as playwright:
        while True:
            await simulate_valid_click(playwright, URL, click_number)
            click_number += 1
            print(f"⏳ Waiting {WAIT_BETWEEN_CLICKS} seconds before next click...")
            await asyncio.sleep(WAIT_BETWEEN_CLICKS)

def run():
    asyncio.run(continuous_clicks())

# Start the loop
run()
