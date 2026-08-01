import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on('console', lambda msg: print('CONSOLE:', msg.text))
        await page.goto('http://localhost:3000')
        await page.wait_for_timeout(2000)
        print(await page.content())
        await browser.close()

asyncio.run(run())
