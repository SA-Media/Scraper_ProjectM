# Third-Party Libraries Documentation

This document outlines the third-party libraries used in the LinkedIn Email Finder project, including their purposes and integration details.

## Libraries & Tools

### 1. AgentQL
- **Purpose:**  
  - Enables natural-language based querying to extract UI elements and data from web pages.
- **Usage:**  
  - Extracts employee data (name, position, email) from LinkedIn profile pages.
- **Integration:**  
  - Integrated into the Python script to send queries after navigating to a profile.

### 2. Playwright
- **Purpose:**  
  - Provides browser automation to handle dynamic web pages and simulate human-like interactions.
- **Usage:**  
  - Automates the login process to LinkedIn and navigation to profile pages.
- **Integration:**  
  - Works asynchronously with Python’s `asyncio` to control browser sessions.

### 3. python-dotenv
- **Purpose:**  
  - Loads environment variables from a `.env` file, keeping sensitive credentials secure.
- **Usage:**  
  - Retrieves LinkedIn login credentials and the AgentQL API key.
- **Integration:**  
  - Used at the start of the script to configure the runtime environment.

### 4. PostgreSQL Driver (psycopg2 or SQLAlchemy)
- **Purpose:**  
  - Facilitates database connectivity and operations with PostgreSQL.
- **Usage:**  
  - Connects the backend script to the PostgreSQL database to store scraped data.
- **Integration:**  
  - Can be used directly (via `psycopg2`) or through an ORM layer like SQLAlchemy, depending on project requirements.

## Considerations
- **Versioning:**  
  - Ensure compatibility between the library versions and Python version in use.
- **Security & Compliance:**  
  - Always store API keys and credentials in secure, non-public locations (like a `.env` file).
- **Documentation:**  
  - Refer to each library's official documentation for detailed setup and advanced configurations.

