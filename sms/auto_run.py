import schedule
import time
import subprocess

def run_scraper():
    subprocess.run(["python3", "./sms/scrape_menu.py"])

# Run every day at 6:00 AM
schedule.every().day.at("06:00").do(run_scraper)
run_scraper()

while True:
    schedule.run_pending()
    time.sleep(60)
