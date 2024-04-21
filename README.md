# Product Scraper for DentalStall Shop

## Introduction
This script is designed to scrape product data from `https://dentalstall.com/shop/`. It navigates through multiple pages of product listings, extracting details such as product title, price, and image URL.

## Features
- Handles pagination by embedding page numbers directly into the URL path.
- Efficiently fetches products across multiple pages as specified by the user.
- Implements a rate-limiting feature to respect the website's request handling policies.
- Provides an API endpoint for initiating scraping processes and fetching results.

## Requirements
- Python 3.x
- Libraries: `requests`, `bs4` (BeautifulSoup)

## API Endpoint Details
- **Endpoint:** `/scrape/dentelstall/`
- **Method:** POST
- **Description:** Initiates the scraping process and returns the scraped data.
- **Parameters:** 
  - `page_limit` (optional): Specifies the number of pages to scrape. Default is 5.
- **Example Request:**
  ```bash
  curl -X POST 'http://localhost:8000/scrape/dentelstall?page_limit=5'
## Screenshots
- **API Response**
<img width="1083" alt="Screenshot 2024-04-22 at 1 18 17 AM" src="https://github.com/exthazor/atlys_scrapper/assets/25245510/363e95b9-72bc-4168-b2ac-f1ed4b69ac60"> <br/>
- **API Response if incorrect token**
<img width="787" alt="Screenshot 2024-04-22 at 1 27 57 AM" src="https://github.com/exthazor/atlys_scrapper/assets/25245510/1db6cf51-faa3-4193-a50f-377ee8269e49"> <br/>
- **Database**
<img width="1035" alt="Screenshot 2024-04-22 at 1 19 53 AM" src="https://github.com/exthazor/atlys_scrapper/assets/25245510/7d085d17-f545-47d4-b18e-772fa2ab8f46"> <br/>
- **Cache (Redis)**
<img width="1208" alt="Screenshot 2024-04-22 at 1 20 24 AM" src="https://github.com/exthazor/atlys_scrapper/assets/25245510/ef649aae-7539-4952-a07f-62468d17541e"> <br/>


