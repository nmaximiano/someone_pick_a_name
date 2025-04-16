import schedule
import time
import subprocess

def run_scraper():
    subprocess.run(["python3", "/Users/jadencampbell/someone_pick_a_name/sms/scrape_menu.py"])

# Run every day at 6:00 AM
schedule.every().day.at("06:00").do(run_scraper)

while True:
    schedule.run_pending()
    time.sleep(60)
