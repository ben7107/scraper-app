 import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import openpyxl
import os
import datetime

EXCEL_FILE = "mailing_list.xlsx"
LOG_FILE = "scraper.log"

def scrape_action(url, username, password):
    try:
        # Fetch page
        response = requests.get(url, auth=(username, password))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Demo extraction (replace with real selectors)
        name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"
        email = soup.find("a", href=lambda x: x and "mailto:" in x)
        email = email.get_text(strip=True) if email else "N/A"
        phone = soup.find("span", class_="phone")
        phone = phone.get_text(strip=True) if phone else "N/A"
        address = soup.find("div", class_="address")
        address = address.get_text(strip=True) if address else "N/A"

        record = [name, email, phone, address, url]

        # Excel handling
        if not os.path.exists(EXCEL_FILE):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Name", "Email", "Phone", "Address", "Source URL"])
            wb.save(EXCEL_FILE)

        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active

        # Deduplication by email
        emails = [row[1].value for row in ws.iter_rows(min_row=2)]
        if email not in emails:
            ws.append(record)
            wb.save(EXCEL_FILE)
            added = True
        else:
            added = False

        # Logging
        with open(LOG_FILE, "a") as log:
            log.write(f"{datetime.datetime.now()} | URL: {url} | Added: {added} | Email: {email}\n")

        messagebox.showinfo("ScraperApp", f"Scraping complete.\nRecord {'added' if added else 'skipped'}.")

    except Exception as e:
        messagebox.showerror("ScraperApp", f"Error: {str(e)}")

def main():
    root = tk.Tk()
    root.title("ScraperApp")
    root.geometry("400x300")

    tk.Label(root, text="Target URL").pack(pady=5)
    url_entry = tk.Entry(root, width=40)
    url_entry.pack(pady=5)

    tk.Label(root, text="Username").pack(pady=5)
    user_entry = tk.Entry(root, width=40)
    user_entry.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=5)
    pass_entry = tk.Entry(root, width=40, show="*")
    pass_entry.pack(pady=5)

    def run_scrape():
        scrape_action(url_entry.get(), user_entry.get(), pass_entry.get())

    tk.Button(root, text="Start Scraping", command=run_scrape).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
