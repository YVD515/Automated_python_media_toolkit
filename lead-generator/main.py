# main.py

from storage.csv_exporter import export_leads_to_csv
from sources.linkedin_scraper import get_leads_from_linkedin

def main():
    print("=== Lead Generator ===")
    keyword = input("Enter job title or keyword (e.g., Marketing Manager): ").strip()
    location = input("Enter location (e.g., New York, USA): ").strip()
    api_key = input("Enter your SerpAPI key: ").strip()
    max_results = input("How many leads do you want? (e.g., 30): ").strip()
    filename = input("Enter output filename (default: leads.csv): ").strip()

    if not max_results.isdigit():
        print("Invalid number. Defaulting to 30 leads.")
        max_results = 30
    else:
        max_results = int(max_results)

    if not filename:
        filename = "leads.csv"

    print(f"[👀] Searching LinkedIn profiles for '{keyword}' in '{location}' ...")

    try:
        leads = get_leads_from_linkedin(keyword, location, api_key, max_results=max_results)
    except Exception as e:
        print(f"[✖] Failed to fetch leads: {e}")
        return

    if leads:
        print(f"[💾] Exporting {len(leads)} leads to {filename}...")
        export_leads_to_csv(leads, filename=filename)
    else:
        print("[⚠️] No leads found!")

    print("[✅] Done!")

if __name__ == "__main__":
    main()
