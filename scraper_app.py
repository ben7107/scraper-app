import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests, re, csv, json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# --- AI Post-Processing (simple demo layer) ---
def validate_email(email):
    # Basic regex + obfuscation fix
    email = email.replace("[at]", "@").replace("(at)", "@")
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def enrich_contact(email):
    domain = email.split("@")[-1]
    company = domain.split(".")[0].capitalize()
    return company

# --- Scraping Engine ---
def scrape_site(url, username=None, password=None):
    try:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return [], f"Error: Site not reachable ({r.status_code})"
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        cleaned = []
        for e in emails:
            if validate_email(e):
                cleaned.append({
                    "Name": "",
                    "Email": e,
                    "Phone": "",
                    "Address": "",
                    "Company": enrich_contact(e),
                    "Source URL": url,
                    "Status": "Success"
                })
        if not cleaned:
            return [], "Warning: No emails detected"
        return cleaned, f"Scraped {len(cleaned)} emails"
    except Exception as ex:
        return [], f"Error: {str(ex)}"

# --- GUI ---
class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScraperApp Pro – Mailing List Scraper")
        self.entries = []

        self.table = ttk.Treeview(root, columns=("URL","Username","Password"), show="headings")
        for col in ("URL","Username","Password"):
            self.table.heading(col, text=col)
        self.table.pack(fill="both", expand=True)

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Add Row", command=self.add_row).pack(side="left")
        tk.Button(btn_frame, text="Remove Row", command=self.remove_row).pack(side="left")
        tk.Button(btn_frame, text="Run", command=self.run_scraper).pack(side="left")

        self.log = tk.Text(root, height=10)
        self.log.pack(fill="both", expand=True)

    def add_row(self):
        self.table.insert("", "end", values=("http://", "", ""))

    def remove_row(self):
        selected = self.table.selection()
        for s in selected:
            self.table.delete(s)

    def log_msg(self, msg):
        self.log.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")

    def run_scraper(self):
        rows = self.table.get_children()
        results = []
        for r in rows:
            url, user, pw = self.table.item(r)["values"]
            self.log_msg(f"Scraping {url}...")
            data, status = scrape_site(url, user, pw)
            results.extend(data)
            self.log_msg(status)

        if results:
            df = pd.DataFrame(results)
            df.drop_duplicates(subset=["Email"], inplace=True)
            df.to_excel("mailing_list.xlsx", index=False)
            self.log_msg("Exported mailing_list.xlsx")
        else:
            self.log_msg("No results to export.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
