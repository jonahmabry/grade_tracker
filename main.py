import datetime
import requests
import os
from dotenv import load_dotenv
import pytz

load_dotenv()


# --- CONFIG ---
API_TOKEN = os.environ.get("CANVAS_TOKEN")
BASE_URL = "https://auburn.instructure.com/api/v1"
DAYS_AHEAD = 7
LOCAL_TZ = pytz.timezone("America/Chicago")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

today_date = datetime.datetime.now(LOCAL_TZ)
start_of_week = today_date - datetime.timedelta(days=today_date.weekday() + 1) # Sunday
end_of_week = start_of_week + datetime.timedelta(days=6) # Saturday

# Format dates like 9/7 - 9/13
week_range = f"{start_of_week.strftime('%-m/%-d')} - {end_of_week.strftime('%-m/%-d')}"
print(f"Jonah's Grades {week_range}\n{'=' * 25}")


# --- GETTING ACTIVE COURSES ---
courses = requests.get(f"{BASE_URL}/courses", headers=headers).json()
filtered_courses = [course for course in courses if course["enrollment_term_id"] == 4407] # 4407 is the id for Fall 2025


# --- FETCHING GRADES AND SAVING THEM TO "grades.txt" IN ICLOUD DRIVE/SHORTCUTS ---
grades_list = []
for course in filtered_courses:
    enrollment_data = requests.get(f"{BASE_URL}/courses/{course["id"]}/enrollments", headers=headers, params={"user_id": "4205893"}).json()
    short_name = course["name"][:-16] # Removing the end of the course name (ex: from "MATH-1620-R10 (Fall 2025)" to "MATH-1620")
    print(f"{short_name}: {enrollment_data[0]["grades"]["current_score"]}")
    grades_list.append(f"{short_name}: {enrollment_data[0]['grades']['current_score']}")


# --- SAVING GRADES TO "grades.txt" IN ICLOUD DRIVE/SHORTCUTS ---
# --- SO THAT I CAN RUN A SHORTCUT THAT TEXTS ME MY GRADES EACH WEEK ---
icloud_path = os.path.expanduser(
    "/Users/jonahmabry/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/grades.txt"
)

with open(icloud_path, "w") as f:
    f.write(f"Jonah's Grades {week_range}\n{'=' * 25}\n")
    for line in grades_list:
        f.write(line + "\n")


print(f"Saved {len(grades_list)} grades to {icloud_path}")