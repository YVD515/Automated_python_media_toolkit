import tkinter as tk
from tkinter import messagebox
from sources.linkedin_scraper import get_leads_from_linkedin
from storage.csv_exporter import export_leads_to_csv

def search_leads():
    keyword = entry_keyword.get().strip()
    location = entry_location.get().strip()
    api_key = entry_api_key.get().strip()
    max_results = entry_max_results.get().strip()

    if not keyword or not location or not api_key:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    if not max_results.isdigit():
        max_results_val = 30
    else:
        max_results_val = int(max_results)

    try:
        leads = get_leads_from_linkedin(keyword, location, api_key, max_results=max_results_val)
    except Exception as e:
        messagebox.showerror("API Error", f"Failed to fetch leads:\n{e}")
        return

    if not leads:
        messagebox.showinfo("Result", "No leads found!")
        return

    export_leads_to_csv(leads)
    messagebox.showinfo("Success", f"{len(leads)} leads saved to leads.csv!")

# --- Tkinter UI setup ---
app = tk.Tk()
app.title("Lead Generator")

tk.Label(app, text="Job Title or Keyword:").grid(row=0, column=0, sticky="e")
entry_keyword = tk.Entry(app, width=40)
entry_keyword.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="Location:").grid(row=1, column=0, sticky="e")
entry_location = tk.Entry(app, width=40)
entry_location.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="SerpAPI Key:").grid(row=2, column=0, sticky="e")
entry_api_key = tk.Entry(app, width=40, show="*")
entry_api_key.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Max Results:").grid(row=3, column=0, sticky="e")
entry_max_results = tk.Entry(app, width=40)
entry_max_results.insert(0, "30")
entry_max_results.grid(row=3, column=1, padx=10, pady=5)

btn_search = tk.Button(app, text="Generate Leads", command=search_leads)
btn_search.grid(row=4, column=0, columnspan=2, pady=15)

app.mainloop()
