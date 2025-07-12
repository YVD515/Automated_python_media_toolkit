# sources/linkedin_scraper.py

from models.lead import Lead
from serpapi import GoogleSearch
import re

def get_leads_from_linkedin(keyword, location, api_key, max_results=50, industry_filters=None, seniority_filters=None):
    leads = []
    results_per_page = 10

    # Handle optional filters
    industry_filters = industry_filters or []
    seniority_filters = seniority_filters or []

    # Combine additional filters into query
    industry_query = " ".join(industry_filters)
    seniority_query = " ".join(seniority_filters)

    for start in range(0, max_results, results_per_page):
        query = f"site:linkedin.com/in {keyword} {location} {industry_query} {seniority_query}"
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

            leads.append(Lead(
                name=name,
                title=title,
                company=company,
                location=location,
                profile_url=link,
                email=""  # No email integration
            ))

        if len(results.get("organic_results", [])) < results_per_page:
            break

    return leads[:max_results]
