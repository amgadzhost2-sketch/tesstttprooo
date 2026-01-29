import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 1. Launch Browser - Headless is default
        # We disable extensions and sync to save RAM
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu", "--disable-dev-shm-usage"])
        
        # 2. Setup Context with "Lite" settings (No Images)
        # This acts like a 'profile' but uses much less memory
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720}
        )
        
        # BLOCK IMAGES: This is the Playwright version of your Firefox preference
        await context.route("**/*.{png,jpg,jpeg,gif,webp,svg,css,woff,woff2,mp4,webm}", lambda route: route.abort())
        page = await context.new_page()

        try:
            print("Opening https://google.com...")
            await page.goto("https://www.moneroocean.crypto-webminer.com/moneroocean.html", wait_until="domcontentloaded")

            # 1. Handle Consent (Manually scanning frames for better reliability)
            print("Scanning all frames for consent button...")

            print("Attempting deep-scan for consent...")
            await asyncio.sleep(5)

            # This targets buttons, divs, or spans that look like buttons
            selectors = [
                "button:has-text('Accept all')", 
                "button:has-text('I agree')",
                "div[role='button']:has-text('Accept')",
                "button:has-text('CONSENT')",
                "button:has-text('Consent')"
            ]

            found = False
            # Search main page and all frames
            for frame in page.frames:
                for selector in selectors:
                    try:
                        target = frame.locator(selector).first
                        if await target.is_visible(timeout=1000):
                            # 'force=True' bypasses the "element is covered" check
                            await target.click(force=True)
                            print(f"Clicked {selector} in frame.")
                            found = True
                            break
                    except:
                        continue
                if found: break

            if not found:
                print("Could not find button. Taking debug screenshot...")
                await page.screenshot(path="debug_not_found.png")
                # 2. Locate input and type
            print("Finding input#walletmoneroocean...")
            search_input = page.locator("input#walletmoneroocean")
            await search_input.fill("4AqoNeUuZpqVNA7LJX6fbN5hCeQoCeMvA1gx5XNwMiMNY7Qk9zuq7RuBDbJd6tSFy6LTqNVqLccu6MVZo1qweHEMNycNm7i")

            # 3. Screenshot and Click
            await page.screenshot(path="justbeforeiclickstart.png")
            print("Clicking button#start...")
            await page.locator("button#start").click()
            await asyncio.sleep(1)
            await page.locator("button#thread-remove").click()
            await asyncio.sleep(1)
            await page.locator("button#thread-remove").click()
            await asyncio.sleep(1)
            await page.locator("button#thread-remove").click()

            # 4. Infinite Loop
            print("Entering 5-second screenshot loop. Override: latest.png")
            while True:
                await page.screenshot(path="latest.png")
                await asyncio.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(run())
