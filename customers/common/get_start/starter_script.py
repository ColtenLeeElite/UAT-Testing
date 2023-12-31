import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://azara-ai-dev-server.vercel.app")
        title = await page.title()
        print(f"Title: {title}")
        await browser.close()

asyncio.run(main())
