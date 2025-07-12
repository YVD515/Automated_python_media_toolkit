# main.py

from storage.csv_exporter import export_leads_to_csv
from sources.linkedin_scraper import get_leads_from_linkedin

def main():
    print("=== Lead Generator ===")
    keyword = input("Enter job title or keyword (e.g., Marketing Manager): ").strip()
    location = input("Enter location (e.g., New York, USA): ").strip()
    api_key = input("Enter your SerpAPI key: ").strip()
    max_results = input("How many leads do you want? (e.g., 30): ").strip()

    if not max_results.isdigit():
        print("Invalid number. Defaulting to 30 leads.")
        max_results = 30
    else:
        max_results = int(max_results)

    print(f"[👀] Searching LinkedIn profiles for '{keyword}' in '{location}' ...")

    leads = get_leads_from_linkedin(keyword, location, api_key, max_results=max_results)

    if leads:
        print(f"[💾] Exporting {len(leads)} leads to CSV...")
        export_leads_to_csv(leads)
    else:
        print("[⚠️] No leads found!")

    print("[✅] Done! Check leads.csv")

if __name__ == "__main__":
    main()
