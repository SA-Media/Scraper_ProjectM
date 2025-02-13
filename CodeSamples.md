
+ EXMAPLE IF AN AGENTQL QUERY TO SCRAPE A LINKEDIN PROFILE:

'''

import os
import json
import asyncio
from playwright.async_api import async_playwright
from agentql import AgentQL  # AgentQL SDK for extraction
from dotenv import load_dotenv

# Load environment variables (ensure you have a .env file with your credentials)
load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")

async def login_linkedin(page):
    # Navigate to LinkedIn's login page
    await page.goto("https://www.linkedin.com/login")
    # Fill in the login credentials
    await page.fill("input#username", LINKEDIN_EMAIL)
    await page.fill("input#password", LINKEDIN_PASSWORD)
    # Click the login button
    await page.click("button[type='submit']")
    # Wait until the network is idle (login complete)
    await page.wait_for_load_state("networkidle")
    # Note: You may need additional handling for CAPTCHAs or two-factor authentication.
    
async def scrape_profile(page, profile_url):
    # Navigate to the LinkedIn profile page
    await page.goto(profile_url)
    await page.wait_for_load_state("networkidle")
    
    # Define our AgentQL query schema for the profile
    profile_query = {
        "name": "Extract the full name from the top section of the LinkedIn profile.",
        "headline": "Extract the professional headline text.",
        "location": "Extract the location information displayed near the name.",
        "about": "Extract the text from the About section of the profile.",
        "experience": "Extract a summary of the most recent experiences listed."
    }
    
    # Use AgentQL to extract the structured data (consult AgentQL docs for API specifics)
    profile_data = await AgentQL.query(page, profile_query, api_key=AGENTQL_API_KEY)
    return profile_data

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for production
        context = await browser.new_context()
        page = await context.new_page()
        
        # Log in to LinkedIn
        print("Logging into LinkedIn...")
        await login_linkedin(page)
        
        # Define the list of LinkedIn profiles to scrape
        profiles = [
            {"name": "Sample Profile", "url": "https://www.linkedin.com/in/sample-profile/"}
            # Add more profiles as needed
        ]
        
        results = {}
        for profile in profiles:
            print(f"Scraping profile data for {profile['name']}...")
            data = await scrape_profile(page, profile["url"])
            results[profile["name"]] = data
        
        # Save the scraped data to a JSON file
        with open("linkedin_profiles.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("Scraping complete. Data saved to linkedin_profiles.json")
        await browser.close()

# Run the main function asynchronously
asyncio.run(main())


''


+ EXAMPLE OF AN AGENTQL QUERY TO SCRAPE A WEBSITE:

'''
import os
import json
import asyncio
from playwright.async_api import async_playwright
from agentql import AgentQL  # Import the AgentQL SDK
from dotenv import load_dotenv

# Load environment variables (ensure you have a .env file with your AgentQL API key)
load_dotenv()
AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")

# Define our list of companies with their URLs
companies = [
    {"name": "Acme Corp", "url": "https://www.acmecorp.com"},
    {"name": "Globex Inc.", "url": "https://www.globex.com"},
    {"name": "Initech", "url": "https://www.initech.com"},
    {"name": "Umbrella Corporation", "url": "https://www.umbrellacorp.com"},
]

# Define our query schema for AgentQL
company_data_query = {
    "company_name": "Extract the main header text that represents the company name.",
    "description": "Extract the content from the About Us section.",
    "founded_year": "Extract the year the company was founded from the company history or footer.",
    "executive": "Extract the name of the CEO or primary executive mentioned on the leadership page.",
    "contact": "Extract the primary contact information (email, phone, or address) from the footer or contact page."
}

async def scrape_company(page, company):
    # Navigate to the company website
    await page.goto(company["url"])
    await page.wait_for_load_state("networkidle")
    
    # Use AgentQL to extract data with our defined query schema
    # (This function call is illustrative; consult AgentQL docs for exact usage)
    extracted_data = await AgentQL.query(page, company_data_query, api_key=AGENTQL_API_KEY)
    
    return extracted_data

async def main():
    results = {}
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)  # Use headless=True for production
        page = await browser.new_page()
        
        for company in companies:
            print(f"Scraping data for {company['name']}...")
            data = await scrape_company(page, company)
            results[company["name"]] = data
        
        # Save the aggregated data to a JSON file
        with open("company_data.json", "w") as outfile:
            json.dump(results, outfile, indent=2)
        
        print("Scraping complete. Data saved to company_data.json")
        await browser.close()

asyncio.run(main())
'''




+ EXAMPLE OF RUNNING AGENTQL IN STEALTH MODE AND AVOIDING BOT DETECTION

'''



import asyncio
import logging
import random

import agentql
from playwright.async_api import Geolocation, ProxySettings, async_playwright

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

BROWSER_IGNORED_ARGS = [
    "--enable-automation",
    "--disable-extensions",
]
BROWSER_ARGS = [
    "--disable-xss-auditor",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-infobars",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
]


LOCATIONS = [
    ("America/New_York", Geolocation(longitude=-74.006, latitude=40.7128)),  # New York, NY
    ("America/Chicago", Geolocation(longitude=-87.6298, latitude=41.8781)),  # Chicago, IL
    ("America/Los_Angeles", Geolocation(longitude=-118.2437, latitude=34.0522)),  # Los Angeles, CA
    ("America/Denver", Geolocation(longitude=-104.9903, latitude=39.7392)),  # Denver, CO
    ("America/Phoenix", Geolocation(longitude=-112.0740, latitude=33.4484)),  # Phoenix, AZ
    ("America/Anchorage", Geolocation(longitude=-149.9003, latitude=61.2181)),  # Anchorage, AK
    ("America/Detroit", Geolocation(longitude=-83.0458, latitude=42.3314)),  # Detroit, MI
    ("America/Indianapolis", Geolocation(longitude=-86.1581, latitude=39.7684)),  # Indianapolis, IN
    ("America/Boise", Geolocation(longitude=-116.2023, latitude=43.6150)),  # Boise, ID
    ("America/Juneau", Geolocation(longitude=-134.4197, latitude=58.3019)),  # Juneau, AK
]

REFERERS = ["https://www.google.com", "https://www.bing.com", "https://duckduckgo.com"]

ACCEPT_LANGUAGES = ["en-US,en;q=0.9", "en-GB,en;q=0.9", "fr-FR,fr;q=0.9"]
PROXIES: list[ProxySettings] = [
    # TODO: replace with your own proxies
    # {
    #     "server": "http://ip_server:port",
    #     "username": "proxy_username",
    #     "password": "proxy_password",
    # },
]


async def main():
    user_agent = random.choice(USER_AGENTS)
    header_dnt = random.choice(["0", "1"])
    location = random.choice(LOCATIONS)
    referer = random.choice(REFERERS)
    accept_language = random.choice(ACCEPT_LANGUAGES)
    proxy: ProxySettings | None = random.choice(PROXIES) if PROXIES else None

    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False,
        args=BROWSER_ARGS,
        ignore_default_args=BROWSER_IGNORED_ARGS,
    ) as browser:
        context = await browser.new_context(
            proxy=proxy,
            locale="en-US,en,ru",
            timezone_id=location[0],
            extra_http_headers={
                "Accept-Language": accept_language,
                "Referer": referer,
                "DNT": header_dnt,
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
            },
            geolocation=location[1],
            user_agent=user_agent,
            permissions=["notifications"],
            viewport={
                "width": 1920 + random.randint(-50, 50),
                "height": 1080 + random.randint(-50, 50),
            },
        )

        page = await agentql.wrap_async(context.new_page())

        await page.enable_stealth_mode(nav_user_agent=user_agent)

        await page.goto("https://bot.sannysoft.com/", referer=referer)
        await page.wait_for_timeout(30000)


if __name__ == "__main__":
    asyncio.run(main())

'''


+ EXAMPLE OF WAITING FOR THE PAGE TO LOAD COMPLETELY BEFORE QUERYING THE PAGE

'''

"""This example demonstrates how to wait for the page to load completely before querying the page."""

import agentql
from playwright.sync_api import sync_playwright

# Duckduckgo URL to demonstrate the example for loading more videos on the page
URL = "https://duckduckgo.com/?q=machine+learning+lectures+mit&t=h_&iar=videos&iax=videos&ia=videos"

QUERY = """
{
    videos(first 10 videos)[] {
        video_title
        length
        views
    }
}
"""


def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(URL)

        for _ in range(2):
            # Wait for additional videos to load completely
            page.wait_for_page_ready_state()
            # Scroll down the page to trigger loading of more videos
            page.keyboard.press("End")

        # Use query_data() method to fetch video lists data from the page
        response = page.query_data(QUERY)

        # Print the details of the first video
        print(response["videos"][0])


if __name__ == "__main__":
    main()

'''


+ EXAMPLE OF COLLECTING PRICING DATA FROM AN E-COMMERCE WEBSITE

'''

"""This is an example of how to collect pricing data from e-commerce website using AgentQL."""

import asyncio

import agentql
from agentql.ext.playwright.async_api import Page
from playwright.async_api import async_playwright

# URL of the e-commerce website
# You can replace it with any other e-commerce website but the queries should be updated accordingly
URL = "https://www.bestbuy.com"


async def _do_extract_pricing_data(page: Page) -> list:
    """Extract pricing data from the current page.

    Args:
        page (Page): The Playwright page object to interact with the browser.

    Returns:
        list: The pricing data extracted from the page.
    """
    # The query of the data to be extracted
    query = """
    {
        products[] {
            name
            model
            sku
            price(integer)
        }
    }"""
    pricing_data = await page.query_data(query)

    return pricing_data.get("products", [])


async def _search_product(
    page: Page,
    product: str,
    min_price: int,
    max_price: int,
) -> bool:
    """Search for a product with a price range.

    Args:
        page (Page): The Playwright page object to interact with the browser.
        product (str): The product name to search for.
        min_price (int): The minimum price of the product.
        max_price (int): The maximum price of the product.

    Returns:
        bool: True if the search is successful, False otherwise.
    """

    # Search for a product
    search_input = await page.get_by_prompt("the search input field")
    if not search_input:
        print("Search input field not found.")
        return False
    await search_input.type(product, delay=200)
    await search_input.press("Enter")

    # Define price range
    min_price_input = await page.get_by_prompt("the min price input field")
    if not min_price_input:
        print("Min price input field not found.")
        return False
    await min_price_input.fill(str(min_price))

    max_price_input = await page.get_by_prompt("the max price input field")
    if not max_price_input:
        print("Max price input field not found.")
        return False
    await max_price_input.fill(str(max_price))
    await max_price_input.press("Enter")
    return True


async def _go_to_the_next_page(page: Page) -> bool:
    """Navigate to the next page of the search results.

    Args:
        page (Page): The Playwright page object to interact with the browser.

    Returns:
        bool: True if the next page is navigated successfully, False if no more next page.
    """
    # Find the next page button using smart locator
    next_page_query = """
    {
        pagination {
            prev_page_url
            next_page_url
        }
    }"""
    print("Navigating to the next page...")
    pagination = await page.query_data(next_page_query)
    next_page_url = pagination.get("pagination", {}).get("next_page_url")
    if not next_page_url:
        return False
    try:
        if not next_page_url.startswith("http"):
            next_page_url = URL + next_page_url  # Make it a full URL
        await page.goto(next_page_url)
        return True
    except Exception:
        pass

    return False


async def extract_pricing_data(
    page: Page,
    product: str,
    min_price: int,
    max_price: int,
    max_pages: int = 3,
) -> list:
    """Extract pricing data for a product within a price range."""
    # Search for the product with the specified price range
    print(f"Searching for product: {product} with price range: ${min_price} - ${max_price}")
    if await _search_product(page, product, min_price, max_price) is False:
        print("Failed to search for the product.")
        return []

    current_page = 1
    pricing_data = []
    while current_page <= max_pages:
        # Extract pricing data from the current page
        print(f"Extracting pricing data on page {current_page}...")
        pricing_data_on_page = await _do_extract_pricing_data(page)
        print(f"{len(pricing_data_on_page)} products found")

        pricing_data.extend(pricing_data_on_page)

        # Navigate to the next page
        if not await _go_to_the_next_page(page):
            print("No more next page.")
            break

        current_page += 1

    return pricing_data


async def main():
    """Main function."""
    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False
    ) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = await agentql.wrap_async(browser.new_page())
        await page.goto(URL)  # open the target URL

        pricing_data = await extract_pricing_data(
            page,
            product="gpu",
            min_price=500,
            max_price=800,
        )

        print(pricing_data)


if __name__ == "__main__":
    asyncio.run(main())

'''


+ EXAMPLE OF PAGINATING THROUGH A WEBSITE

'''

import json
import logging

from playwright.sync_api import sync_playwright

import agentql

# import paginate tool from agentql tools
from agentql.tools.sync_api import paginate

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://news.ycombinator.com/")

        # define the query to extract post titles
        QUERY = """
        {
            posts[] {
                title
            }
        }
        """
        # collect all data over the next 3 pages with the query defined above
        paginated_data = paginate(page, QUERY, 3)

        # save the aggregateddata to a json file
        with open("./hackernews_paginated_data.json", "w") as f:
            json.dump(paginated_data, f, indent=4)
        log.debug("Paginated data has been saved to hackernews_paginated_data.json")



'''


+ EXAMPLE OF COMPARING PRODUCT PRICES ACROSS WEBSITES
'''
"""This example demonstrates how to compare product prices across websites with query_data() method."""

import agentql
from playwright.sync_api import sync_playwright

# Set the URL to the desired website
BESTBUY_URL = "https://www.bestbuy.com/site/nintendo-switch-oled-model-w-joy-con-white/6470923.p?skuId=6470923"
TARGET_URL = "https://www.target.com/p/nintendo-switch-oled-model-with-white-joy-con/-/A-83887639#lnk=sametab"
NINTENDO_URL = "https://www.nintendo.com/us/store/products/nintendo-switch-oled-model-white-set/"

# Define the queries to get the product price
PRODUCT_INFO_QUERY = """
{
    nintendo_switch_price(integer)
}
"""


def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(BESTBUY_URL)

        # Use query_data() method to fetch the price from the BestBuy page
        response = page.query_data(PRODUCT_INFO_QUERY)

        print("Price at BestBuy: ", response["nintendo_switch_price"])

        page.goto(NINTENDO_URL)

        # Use query_data() method to fetch the price from the Nintendo page
        response = page.query_data(PRODUCT_INFO_QUERY)

        print("Price at Nintendo: ", response["nintendo_switch_price"])

        page.goto(TARGET_URL)

        # Use query_data() method to fetch the price from the Target page
        response = page.query_data(PRODUCT_INFO_QUERY)

        print("Price at Target: ", response["nintendo_switch_price"])


if __name__ == "__main__":
    main()


'''


+ EXAMPLE OF LOGGING INTO A WEBSITE

'''

"""This example demonstrates how to login into websites by retrieving and interacting with web elements in AgentQL."""

import agentql
from playwright.sync_api import sync_playwright

# Set the URL to the desired website
URL = "https://practicetestautomation.com/practice-test-login/"

LOGIN_QUERY = """
{
    username_field
    password_field
    submit_btn
}
"""


def main():
    with sync_playwright() as p, p.chromium.launch(headless=False) as browser:

        page = agentql.wrap(browser.new_page())  # Wrapped to access AgentQL's query API

        # Navigate to the URL
        page.goto(URL)

        # Get the username and password fields
        response = page.query_elements(LOGIN_QUERY)

        # Fill the username and password fields
        response.username_field.fill("student")
        response.password_field.fill("Password123")

        # Click the submit button
        response.submit_btn.click()

        # Used only for demo purposes. It allows you to see the effect of the script.
        page.wait_for_timeout(10000)


if __name__ == "__main__":
    main()


'''


+ EXAMPLE OF RANDOM MOUSE MOVEMENT

'''

import random
import time

from playwright.sync_api import ElementHandle, Page, sync_playwright

import agentql


def random_mouse_movement(page: Page):
    for _ in range(10):
        page.mouse.move(random.randint(0, 1000), random.randint(0, 1000))
        time.sleep(random.uniform(0.1, 0.5))


def random_click(page: Page, element: ElementHandle):
    box = element.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)


def random_scroll(page: Page):
    page.mouse.wheel(0, 1000)
    time.sleep(random.uniform(0.1, 0.5))


with sync_playwright() as playwright:
    # Launch browser with proxy settings
    browser = playwright.chromium.launch(headless=False)

    # Wrap browser with AgentQL
    page = agentql.wrap(browser.new_page())
    page.goto("https://duckduckgo.com/")

    # Type "AgentQL" into the search box keystroke by keystroke
    page.get_by_prompt("the search bar").press_sequentially("AgentQL")

    # Click the search button in a random manner
    random_click(page, page.get_by_prompt("the search button"))

    for _ in range(5):
        random_mouse_movement(page)
        random_scroll(page)


'''