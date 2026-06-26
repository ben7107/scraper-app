import tkinter as tk
from tkinter import messagebox

def scrape_action():
    messagebox.showinfo("ScraperApp", "Scraping started... (demo)")

def main():
    root = tk.Tk()
    root.title("ScraperApp")
    root.geometry("300x200")

    label = tk.Label(root, text="Welcome to ScraperApp!", font=("Arial", 12))
    label.pack(pady=20)

    button = tk.Button(root, text="Start Scraping", command=scrape_action)
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
