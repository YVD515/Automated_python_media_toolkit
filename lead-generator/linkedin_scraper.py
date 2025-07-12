# sources/linkedin_scraper.py

from models.lead import Lead
from serpapi import GoogleSearch
import re

def get_leads_from_linkedin(keyword, location, api_key, max_results=50):
    leads = []
    results_per_page = 10

    for start in range(0, max_results, results_per_page):
        query = f"site:linkedin.com/in {keyword} {location}"
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": results_per_page,
            "start": start
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for result in results.get("organic_results", []):
            link = result.get("link", "")
            title_text = result.get("title", "")
            snippet = result.get("snippet", "")

            name = title_text.split(" - ")[0].strip()

            # --- Enrich title and company from snippet ---
            title, company = "", ""
            match = re.search(r"(.+?) at (.+?)(\||$)", snippet)
            if match:
                title = match.group(1).strip()
                company = match.group(2).strip()

            # --- Email enrichment placeholder ---
            email = ""  # Placeholder for future integration

            leads.append(Lead(
                name=name,
                title=title,
                company=company,
                location=location,
                profile_url=link,
                email=email
            ))

        if len(results.get("organic_results", [])) < results_per_page:
            break

    return leads[:max_results]
