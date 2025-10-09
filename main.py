import datetime
import json

import requests
import os
from dotenv import load_dotenv
import pytz
from calculate_gpa import calculate_gpa

load_dotenv()


# --- CONFIG ---
API_TOKEN = os.environ.get("CANVAS_TOKEN")
BASE_URL = "https://auburn.instructure.com/api/v1"
ICLOUD_PATH = os.path.expanduser("/Users/jonahmabry/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/grades.txt")
PREVIOUS_GRADES = "previous_grades.json"
TERM_ID = 4407 # Fall 2025
USER_ID = "4205893"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# --- FORMAT DATES LIKE 9/7 - 9/13 ---
today_date = datetime.datetime.now(pytz.timezone("America/Chicago"))
start_of_week = today_date - datetime.timedelta(days=today_date.weekday() + 1) # Sunday
end_of_week = start_of_week + datetime.timedelta(days=6) # Saturday

week_range = f"{start_of_week.strftime('%-m/%-d')} - {end_of_week.strftime('%-m/%-d')}"
print(f"Jonah's Grades {week_range}\n{'=' * 25}")


# --- GET ACTIVE COURSES ---
courses = requests.get(f"{BASE_URL}/courses", headers=headers).json()
filtered_courses = [course for course in courses if course["enrollment_term_id"] == TERM_ID]


# --- FETCH GRADES FROM CANVAS AND SAVE THEM TO current_grades ---
current_grades = {}
for course in filtered_courses:
    enrollment_data = requests.get(f"{BASE_URL}/courses/{course["id"]}/enrollments", headers=headers, params={"user_id": USER_ID}).json()

    short_name = course["name"][:-16] # Removing the end of the course name (ex: from "MATH-1620-R10 (Fall 2025)" to "MATH-1620")
    current_grades[short_name] = enrollment_data[0]['grades']['current_score']


# --- SET old_grades WITH PREVIOUS_GRADES
if os.path.exists(PREVIOUS_GRADES):
    with open(PREVIOUS_GRADES, "r") as f:
        old_grades = json.load(f)
else:
    old_grades = {}


def find_diff(diff):
    """Returns the difference from the previous grade or gpa"""
    if abs(diff) > 0:
        sign = "+" if diff > 0 else ""
        return f" ({sign}{diff:.2f})"
    return ""


def update_grades(old_grades, current_grades):
    """Returns formatted output string with current grades and differences from previous grades."""
    output = ""
    for course, current_grade in current_grades.items():
        old = old_grades[course] if old_grades else 0

        grade_msg = f"{course}: {current_grade}"
        grade_diff = current_grade - old

        output += f"{grade_msg}{find_diff(grade_diff)}\n"
    print(output)
    return output + "\n"


def update_gpa(old_grades, current_grades):
    """Returns formatted output string with current GPA and differences from previous GPA."""
    old_gpa = calculate_gpa(old_grades) if old_grades else 0
    current_gpa = calculate_gpa(current_grades)

    gpa_msg = f"GPA: {current_gpa:.2f}"
    gpa_diff = current_gpa - old_gpa

    print(f"{gpa_msg}{find_diff(gpa_diff)}")
    return f"{gpa_msg}{find_diff(gpa_diff)}"


# --- WRITE GRADES TO ICLOUD_PATH ---
with open(ICLOUD_PATH, "w") as f:
    f.write(f"Jonah's Grades {week_range}\n{'=' * 25}\n")
    f.write(update_grades(old_grades, current_grades))
    f.write(update_gpa(old_grades, current_grades))


# --- SET PREVIOUS_GRADES WITH current_grades ---
with open(PREVIOUS_GRADES, "w") as f:
    json.dump(current_grades, f, indent=4)


print(f"Saved {len(current_grades)} grades to {ICLOUD_PATH[ICLOUD_PATH.rfind('/') + 1:]}")