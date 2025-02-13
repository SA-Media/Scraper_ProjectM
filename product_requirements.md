# Product Requirements Document (PRD)

## App Overview
**Name:** LinkedIn Email Finder  
**Description:**  
A tool designed to take a list of companies and automatically locate employee LinkedIn profiles, extracting key data—name, position, and email—from their contact sections. This data is then stored in a PostgreSQL database for further use.

## Target Audience
- **Primary Users:** Blog owners looking to build or expand their outreach and networking by gathering verified contact information.
- **User Goals:**  
  - Efficiently gather employee contact details.
  - Use the data for targeted outreach, networking, or content collaboration.
- **Pain Points:**  
  - Manual collection of data is time-consuming.
  - Difficulty in verifying accurate contact information.

## Key Features
1. **Input Mechanism:**  
   - Accept a list of companies as input.
2. **Automated Data Extraction:**  
   - Scrape LinkedIn for employee profiles.
   - Extract name, position, and email directly from profile contact sections.
3. **Data Storage:**  
   - Save the extracted data into a PostgreSQL database.
4. **Future Enhancements:**  
   - Add options to filter by industry or specific email criteria.

## Success Metrics
- **Accuracy:** High percentage of valid and verified emails extracted.
- **Efficiency:** Time taken to process and store data.
- **Scalability:** Ability to handle an increasing list of companies and profiles without significant performance degradation.

## Assumptions & Risks
- **Assumptions:**  
  - Users have a list of companies to feed into the system.
  - LinkedIn profiles are accessible after login.
- **Risks:**  
  - Potential violation of LinkedIn’s terms of service.
  - Handling CAPTCHAs or anti-bot measures during scraping.



