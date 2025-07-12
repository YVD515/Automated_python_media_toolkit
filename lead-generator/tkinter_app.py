# tkinter_app.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
from sources.linkedin_scraper import get_leads_from_linkedin
from storage.csv_exporter import export_leads_to_csv

CONFIG_FILE = "config.json"

# --- Config utilities ---
def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Warning: could not save config: {e}")

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# --- Lead search ---
def search_leads():
    keywords = [k.strip() for k in entry_keyword.get().split(",") if k.strip()]
    locations = [l.strip() for l in entry_location.get().split(",") if l.strip()]
    api_key = entry_api_key.get().strip()
    max_results = entry_max_results.get().strip()
    filename = entry_filename.get().strip()

    if not keywords or not locations or not api_key or not filename:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    if not max_results.isdigit():
        max_results_val = 30
    else:
        max_results_val = int(max_results)

    label_status.config(text="🔍 Searching...", foreground="blue")
    app.update_idletasks()

    all_leads = []
    total_combos = len(keywords) * len(locations)

    try:
        for job in keywords:
            for loc in locations:
                label_status.config(text=f"Searching: {job} in {loc}...", foreground="blue")
                app.update_idletasks()

                leads = get_leads_from_linkedin(job, loc, api_key, max_results=max_results_val)
                all_leads.extend(leads)

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to fetch leads:\n{e}")
        label_status.config(text="Search failed ❌", foreground="red")
        return

    if not all_leads:
        messagebox.showinfo("Result", "No leads found!")
        label_status.config(text="No leads found", foreground="orange")
        return

    export_leads_to_csv(all_leads, filename=filename)
    messagebox.showinfo("Success", f"{len(all_leads)} total leads saved to {filename}!")
    label_status.config(text=f"✅ {len(all_leads)} leads saved", foreground="green")

    # Save inputs to config
    config_data = {
        "keyword": entry_keyword.get(),
        "location": entry_location.get(),
        "api_key": api_key,
        "max_results": max_results,
        "filename": filename
    }
    save_config(config_data)


# --- App UI ---
config = load_config()
app = ttk.Window(title="Lead Generator", themename="superhero", size=(500, 420), resizable=(False, False))

ttk.Label(app, text="🔎 LinkedIn Lead Generator", font=("Segoe UI", 16, "bold")).pack(pady=10)

input_frame = ttk.Labelframe(app, text="Lead Search Parameters", padding=20)
input_frame.pack(fill="x", padx=20, pady=10)

# --- Keyword
ttk.Label(input_frame, text="Job Titles (comma-separated):").grid(row=0, column=0, sticky="e", pady=5)
entry_keyword = ttk.Entry(input_frame, width=40)
entry_keyword.insert(0, config.get("keyword", ""))
entry_keyword.grid(row=0, column=1, padx=10, pady=5)

# --- Location
ttk.Label(input_frame, text="Locations (comma-separated):").grid(row=1, column=0, sticky="e", pady=5)
entry_location = ttk.Entry(input_frame, width=40)
entry_location.insert(0, config.get("location", ""))
entry_location.grid(row=1, column=1, padx=10, pady=5)

# --- API Key
ttk.Label(input_frame, text="SerpAPI Key:").grid(row=2, column=0, sticky="e", pady=5)
entry_api_key = ttk.Entry(input_frame, width=40, show="*")
entry_api_key.insert(0, config.get("api_key", ""))
entry_api_key.grid(row=2, column=1, padx=10, pady=5)

# --- Max Results
ttk.Label(input_frame, text="Max Results per Combo:").grid(row=3, column=0, sticky="e", pady=5)
entry_max_results = ttk.Entry(input_frame, width=40)
entry_max_results.insert(0, config.get("max_results", "30"))
entry_max_results.grid(row=3, column=1, padx=10, pady=5)

# --- Output Filename
ttk.Label(input_frame, text="Output File Name:").grid(row=4, column=0, sticky="e", pady=5)
entry_filename = ttk.Entry(input_frame, width=40)
entry_filename.insert(0, config.get("filename", "leads.csv"))
entry_filename.grid(row=4, column=1, padx=10, pady=5)

# --- Search Button
ttk.Button(app, text="🎯 Generate Leads", bootstyle=SUCCESS, command=search_leads).pack(pady=10)

# --- Status Label
label_status = ttk.Label(app, text="", font=("Segoe UI", 10))
label_status.pack(pady=5)

app.mainloop()
