import requests
from datetime import datetime

# Get today's date
today = datetime.now().strftime("%Y-%m-%d")

# API endpoint with dynamic date
API_URL = f"https://api-prd.sodexomyway.net/v0.2/data/menu/54043001/15462?date={today}"

# Headers copied from network inspector
HEADERS = {
    "accept": "*/*",
    "api-key": "68717828-b754-420d-9488-4c37cb7d7ef7",
    "authorization": "Bearer",
    "content-type": "application/json",
    "origin": "https://zagdining.sodexomyway.com",
    "referer": "https://zagdining.sodexomyway.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

MEAL_ORDER = ["BREAKFAST", "LUNCH", "AFTERNOON SNACK", "DINNER"]

def fetch_menu():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch API: {e}")
        return {}

    sorted_menu = {}

    for meal in data:
        meal_name = meal.get("name", "").strip().upper()
        if meal_name not in MEAL_ORDER:
            continue

        meal_title = meal_name.title()
        if meal_title not in sorted_menu:
            sorted_menu[meal_title] = {}

        for group in meal.get("groups", []):
            if not group:
                continue
            course_name = group.get("name", "Uncategorized") or "Uncategorized"
            course_title = course_name.title()
            if course_title not in sorted_menu[meal_title]:
                sorted_menu[meal_title][course_title] = []

            for item in group.get("items", []):
                formal_name = item.get("formalName", "").strip() or item.get("name", "").strip()
                if formal_name:
                    sorted_menu[meal_title][course_title].append(formal_name)


    return sorted_menu

def save_menu(menu):
    with open("menu.txt", "w") as f:
        for meal, courses in menu.items():
            f.write(f"{meal}:\n")
            for course, items in courses.items():
                f.write(f"  {course}:\n")
                for item in items:
                    f.write(f"    - {item}\n")
            f.write("\n")
    print("✅ Menu saved to menu.txt")

if __name__ == "__main__":
    menu = fetch_menu()
    save_menu(menu)
