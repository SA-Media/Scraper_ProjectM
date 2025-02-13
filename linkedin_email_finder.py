import os
import asyncio
from datetime import datetime
import psycopg2
from playwright.async_api import async_playwright
from agentql import AgentQL  # AgentQL SDK for querying and data extraction
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL configuration from environment variables
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")

def get_db_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DATABASE,
    )

def init_db():
    """Initialize the database and create required tables if they don't exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Create companies table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        );
    """)
    # Create employees table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            name VARCHAR(255),
            position VARCHAR(255),
            email VARCHAR(255),
            linkedin_profile_url TEXT,
            scraped_at TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

async def login_linkedin(page):
    """Logs into LinkedIn using credentials from environment variables."""
    await page.goto("https://www.linkedin.com/login")
    await page.fill("input#username", LINKEDIN_EMAIL)
    await page.fill("input#password", LINKEDIN_PASSWORD)
    await page.click("button[type='submit']")
    await page.wait_for_load_state("networkidle")
    # Note: Additional steps may be needed for handling CAPTCHAs or 2FA.

async def scrape_employee_profile(page, profile_url):
    """
    Navigates to an employee's LinkedIn profile and extracts data using AgentQL.
    The extraction query is defined to return the name, current position, and email.
    """
    await page.goto(profile_url)
    await page.wait_for_load_state("networkidle")
    employee_query = {
        "name": "Extract the employee's full name from the profile header.",
        "position": "Extract the current job title from the profile (e.g., from the headline or experience).",
        "email": "Extract the email address from the contact information section, if available.",
    }
    data = await AgentQL.query(page, employee_query, api_key=AGENTQL_API_KEY)
    return data

async def scrape_company_employees(page, company):
    """
    Iterates through the given list of employee profile URLs for a company.
    Returns a list of employee data dictionaries.
    """
    results = []
    for profile_url in company["profile_urls"]:
        try:
            print(f"Scraping employee profile: {profile_url}")
            employee_data = await scrape_employee_profile(page, profile_url)
            employee_data["linkedin_profile_url"] = profile_url
            results.append(employee_data)
        except Exception as e:
            print(f"Error scraping profile {profile_url}: {e}")
    return results

def save_company_and_employees(conn, company_name, employees):
    """Saves the company (if not already saved) and its employee data to the database."""
    cur = conn.cursor()
    # Insert the company. If it already exists, update (or do nothing) and retrieve the id.
    cur.execute("""
        INSERT INTO companies (name)
        VALUES (%s)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id;
    """, (company_name,))
    result = cur.fetchone()
    if result is None:
        # In case nothing was returned, select the id manually.
        cur.execute("SELECT id FROM companies WHERE name = %s;", (company_name,))
        company_id = cur.fetchone()[0]
    else:
        company_id = result[0]
    
    for emp in employees:
        cur.execute("""
            INSERT INTO employees (company_id, name, position, email, linkedin_profile_url, scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            company_id,
            emp.get("name"),
            emp.get("position"),
            emp.get("email"),
            emp.get("linkedin_profile_url"),
            datetime.now()
        ))
    conn.commit()
    cur.close()

async def main():
    # Initialize database tables
    init_db()
    # Open a persistent DB connection for saving data
    conn = get_db_connection()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Change to headless=True for production
        context = await browser.new_context()
        page = await context.new_page()

        print("Logging into LinkedIn...")
        await login_linkedin(page)

        # Define a sample list of companies.
        # Each company must include a name and a list of employee LinkedIn profile URLs.
        companies = [
            {
                "name": "Acme Inc",
                "profile_urls": [
                    "https://www.linkedin.com/in/sample-employee1/",
                    "https://www.linkedin.com/in/sample-employee2/"
                ]
            },
            {
                "name": "Globex Corporation",
                "profile_urls": [
                    "https://www.linkedin.com/in/sample-employee3/"
                ]
            },
            # Add more companies and their employee profile URLs as needed.
        ]

        for company in companies:
            print(f"\nProcessing company: {company['name']}")
            employees = await scrape_company_employees(page, company)
            if employees:
                print(f"Saving {len(employees)} employee(s) for {company['name']} to the database.")
                save_company_and_employees(conn, company["name"], employees)
            else:
                print(f"No employee data scraped for {company['name']}.")

        conn.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 