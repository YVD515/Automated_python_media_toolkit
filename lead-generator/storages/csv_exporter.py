# storage/csv_exporter.py

import pandas as pd
from models.lead import Lead

def export_leads_to_csv(leads: list[Lead], filename="leads.csv"):
    data = [lead.__dict__ for lead in leads]
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[✔] Exported {len(leads)} leads to {filename}")
