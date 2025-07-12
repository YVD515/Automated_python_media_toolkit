import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, ttk as tkttk
import json, os, webbrowser, datetime
from fpdf import FPDF

from sources.linkedin_scraper import get_leads_from_linkedin
from storage.csv_exporter import export_leads_to_csv
from models.lead import Lead

CONFIG_FILE = "config.json"
SESSION_FILE = "last_session.json"
leads_buffer = []


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def deduplicate_leads(leads):
    seen = set()
    unique = []
    for lead in leads:
        if lead.profile_url not in seen:
            seen.add(lead.profile_url)
            unique.append(lead)
    return unique


def save_session(leads):
    with open(SESSION_FILE, "w") as f:
        json.dump([lead.__dict__ for lead in leads], f)


def load_last_session():
    if not os.path.exists(SESSION_FILE):
        return []
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return [Lead(**d) for d in data]

import os
import urllib.request

def ensure_noto_font(font_dir="fonts", font_name="NotoSans-Regular.ttf"):
    os.makedirs(font_dir, exist_ok=True)
    font_path = os.path.join(font_dir, font_name)
    if not os.path.isfile(font_path):
        print("Downloading NotoSans-Regular.ttf font...")
        url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"
        try:
            urllib.request.urlretrieve(url, font_path)
            print(f"Font downloaded and saved to {font_path}")
        except Exception as e:
            print(f"Failed to download font: {e}")
            raise
    return font_path


def export_to_pdf(leads, filename="leads.pdf"):
    font_path = ensure_noto_font()  # Download font if missing
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('NotoSans', '', font_path, uni=True)
    pdf.set_font('NotoSans', '', 12)

    pdf.cell(200, 10, txt="Lead Export", ln=True, align='C')

    for lead in leads:
        text = f"{lead.name} | {lead.title} | {lead.company} | {lead.location}\n{lead.profile_url}\n"
        pdf.multi_cell(0, 10, text)

    pdf.output(filename)
    print(f"[✔] Exported {len(leads)} leads to {filename}")


def export_from_table():
    if not leads_buffer:
        messagebox.showwarning("Nothing to export", "No leads loaded yet.")
        return

    filename = entry_filename.get().strip() or "leads.csv"
    chosen_format = export_format_var.get()

    # Fix filename extension if needed
    if chosen_format == "csv" and not filename.lower().endswith(".csv"):
        filename += ".csv"
    elif chosen_format == "pdf" and not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    if chosen_format == "csv":
        export_leads_to_csv(leads_buffer, filename=filename)
        messagebox.showinfo("Exported", f"{len(leads_buffer)} leads exported to {filename}")
    else:
        try:
            export_to_pdf(leads_buffer, filename=filename)
            messagebox.showinfo("Exported", f"{len(leads_buffer)} leads exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export to PDF:\n{e}")


def populate_leads_table(leads):
    for row in tree.get_children():
        tree.delete(row)
    for lead in leads:
        tree.insert("", "end", values=(lead.name, lead.title, lead.company, lead.location, lead.profile_url))


def filter_table(event=None):
    query = entry_filter.get().strip().lower()
    tree.delete(*tree.get_children())
    for lead in leads_buffer:
        if query in lead.location.lower():
            tree.insert("", "end", values=(lead.name, lead.title, lead.company, lead.location, lead.profile_url))


def on_double_click(event):
    selected = tree.selection()
    if selected:
        url = tree.item(selected[0])["values"][-1]
        webbrowser.open_new_tab(url)


def search_leads():
    keywords = [k.strip() for k in entry_keyword.get().split(",") if k.strip()]
    locations = [l.strip() for l in entry_location.get().split(",") if l.strip()]
    api_key = entry_api_key.get().strip()
    max_results = entry_max_results.get().strip()
    filename = entry_filename.get().strip()

    if not keywords or not locations or not api_key:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    max_results_val = int(max_results) if max_results.isdigit() else 30
    label_status.config(text="🔍 Searching...", foreground="blue")
    progress.start()
    app.update_idletasks()

    all_leads = []
    try:
        for job in keywords:
            for loc in locations:
                label_status.config(text=f"Searching: {job} in {loc}...", foreground="blue")
                app.update_idletasks()
                leads = get_leads_from_linkedin(job, loc, api_key, max_results=max_results_val)
                all_leads.extend(leads)
    except Exception as e:
        progress.stop()
        messagebox.showerror("API Error", f"Failed to fetch leads:\n{str(e)}")
        label_status.config(text="Search failed ❌", foreground="red")
        return

    progress.stop()

    if not all_leads:
        label_status.config(text="No leads found", foreground="orange")
        messagebox.showinfo("Result", "No leads found!")
        return

    unique_leads = deduplicate_leads(all_leads)
    leads_buffer.clear()
    leads_buffer.extend(unique_leads)
    populate_leads_table(leads_buffer)
    save_session(leads_buffer)
    label_status.config(text=f"✅ {len(unique_leads)} leads ready to export", foreground="green")
    messagebox.showinfo("Success", f"{len(unique_leads)} leads found and deduplicated.")

    config_data = {
        "keyword": entry_keyword.get(),
        "location": entry_location.get(),
        "api_key": api_key,
        "max_results": max_results,
        "filename": filename
    }
    save_config(config_data)


# ---- UI ----
config = load_config()
app = ttk.Window(title="Lead Generator", themename="cosmo", size=(780, 700), resizable=(False, True))

main_frame = ttk.Frame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = ttk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

ttk.Label(scrollable_frame, text="🔎 LinkedIn Lead Generator", font=("Segoe UI", 16, "bold")).pack(pady=10)

input_frame = ttk.Labelframe(scrollable_frame, text="Lead Search Parameters", padding=20)
input_frame.pack(fill="x", pady=10)

ttk.Label(input_frame, text="Job Titles (comma-separated):").grid(row=0, column=0, sticky="e", pady=5)
entry_keyword = ttk.Entry(input_frame, width=50)
entry_keyword.insert(0, config.get("keyword", ""))
entry_keyword.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Locations (comma-separated):").grid(row=1, column=0, sticky="e", pady=5)
entry_location = ttk.Entry(input_frame, width=50)
entry_location.insert(0, config.get("location", ""))
entry_location.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="SerpAPI Key:").grid(row=2, column=0, sticky="e", pady=5)
entry_api_key = ttk.Entry(input_frame, width=50, show="*")
entry_api_key.insert(0, config.get("api_key", ""))
entry_api_key.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Max Results per Combo:").grid(row=3, column=0, sticky="e", pady=5)
entry_max_results = ttk.Entry(input_frame, width=50)
entry_max_results.insert(0, config.get("max_results", "30"))
entry_max_results.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Output File Name:").grid(row=4, column=0, sticky="e", pady=5)
entry_filename = ttk.Entry(input_frame, width=50)
entry_filename.insert(0, config.get("filename", "leads.csv"))
entry_filename.grid(row=4, column=1, padx=10, pady=5)

ttk.Button(scrollable_frame, text="🎯 Generate Leads", bootstyle=SUCCESS, command=search_leads).pack(pady=10)
label_status = ttk.Label(scrollable_frame, text="", font=("Segoe UI", 10))
label_status.pack(pady=(0, 10))

progress = ttk.Progressbar(scrollable_frame, mode="indeterminate", length=300)
progress.pack(pady=(0, 5))

entry_filter = ttk.Entry(scrollable_frame, width=40)
entry_filter.insert(0, "Type location to filter...")
entry_filter.bind("<KeyRelease>", filter_table)
entry_filter.pack(pady=(5, 5))

columns = ("Name", "Title", "Company", "Location", "Profile URL")
tree = tkttk.Treeview(scrollable_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=130 if col != "Profile URL" else 200)
tree.pack(padx=15, pady=(5, 0), fill="both", expand=True)
tree.bind("<Double-1>", on_double_click)

ttk.Label(input_frame, text="Export Format:").grid(row=5, column=0, sticky="e", pady=5)
export_format_var = tk.StringVar()
export_format_combo = tkttk.Combobox(input_frame, textvariable=export_format_var, state="readonly", width=47)
export_format_combo['values'] = ("csv", "pdf")
export_format_combo.current(0)  # default to CSV
export_format_combo.grid(row=5, column=1, padx=10, pady=5)

ttk.Button(scrollable_frame, text="📥 Export Displayed Leads", bootstyle=PRIMARY, command=export_from_table).pack(pady=20)

prev_session = load_last_session()
if prev_session:
    leads_buffer.extend(prev_session)
    populate_leads_table(leads_buffer)
    label_status.config(text=f"Loaded {len(leads_buffer)} leads from previous session.", foreground="green")

app.mainloop()
