# sources/linkedin_scraper.py

from models.lead import Lead
from serpapi import GoogleSearch       # ✅ CORRECT


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
            title = result.get("title", "")
            snippet = result.get("snippet", "")

            # Basic name/title parsing (improve later if needed)
            name = title.split(" - ")[0].strip()
            leads.append(Lead(
                name=name,
                title="",
                company="",
                location=location,
                profile_url=link,
                email=""
            ))

        if len(results.get("organic_results", [])) < results_per_page:
            break  # no more pages

    return leads[:max_results]
