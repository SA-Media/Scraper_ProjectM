# Backend Documentation

## Overview
This backend service is a standalone Python script that automates the process of logging into LinkedIn, scraping employee data from company profiles, and storing the extracted data into a PostgreSQL database.

## Technology Stack
- **Language:** Python
- **Automation & Scraping:**  
  - **Playwright:** For browser automation and handling dynamic page content.
  - **AgentQL:** For natural-language based data extraction from UI elements.
- **Database:** PostgreSQL (for storing structured data).
- **Environment Management:** python-dotenv for loading credentials securely.

## Workflow
1. **Authentication:**  
   - The script logs into LinkedIn using credentials stored in a `.env` file.
2. **Data Scraping:**  
   - For each company in the provided list:
     - Locate employee LinkedIn profiles.
     - Navigate to each profile and extract:
       - **Name**
       - **Position**
       - **Email** (from the profile’s contact section)
3. **Data Storage:**  
   - Extracted data is stored in a PostgreSQL database with two main tables:
     - **Companies:** Stores company names.
     - **Employees:** Stores employee data along with a reference to the company.

## Database Schema

### Companies Table
| Field | Description |
| --- | --- |
| `id` | Primary key (auto-increment). |
| `name` | Company name. |

### Employees Table
| Field | Description |
| --- | --- |
| `id` | Primary key (auto-increment). |
| `company_id` | Foreign key linking to Companies table. |
| `name` | Employee's full name. |
| `position` | Employee's job title/position. |
| `email` | Employee's email address. |
| `linkedin_profile_url` | URL of the LinkedIn profile. |
| `scraped_at` | Timestamp when the data was scraped. |

## Key Considerations
- **Error Handling:**  
  - Implement error handling for CAPTCHAs, dynamic page elements, and login issues.
- **Environment Variables:**  
  - Use a `.env` file for sensitive information (LinkedIn credentials, AgentQL API key).
- **Scalability:**  
  - Designed as a standalone script to be integrated into a larger data pipeline later.

## Execution
- The script runs as a standalone process.
- No REST API or web server is provided; the data is directly fed into the database.
