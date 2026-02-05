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
HISTORY_FILE = "grades_history.json"
TERM_ID = 3945 # Spring 2026
USER_ID = "4205893"

headers = {"Authorization": f"Bearer {API_TOKEN}"}


# --- WEEK RANGE ---
today_date = datetime.datetime.now(pytz.timezone("America/Chicago"))

# Compute start of week (Sunday)
weekday = today_date.weekday()  # Monday=0 ... Sunday=6
days_since_sunday = (weekday + 1) % 7
start_of_week = today_date - datetime.timedelta(days=days_since_sunday)
end_of_week = start_of_week + datetime.timedelta(days=6)

week_key = f"{start_of_week.strftime('%Y-%m-%d')}_to_{end_of_week.strftime('%Y-%m-%d')}"
week_range = f"{start_of_week.strftime('%-m/%-d')} - {end_of_week.strftime('%-m/%-d')}"

# Previous calendar week (for “Since Last Week”)
last_week_start = start_of_week - datetime.timedelta(days=7)
last_week_end = end_of_week - datetime.timedelta(days=7)
previous_week_key = f"{last_week_start.strftime('%Y-%m-%d')}_to_{last_week_end.strftime('%Y-%m-%d')}"


# --- GET ACTIVE COURSES ---
courses = requests.get(f"{BASE_URL}/courses?per_page=20", headers=headers).json()
filtered_courses = [course for course in courses if course.get("enrollment_term_id") == TERM_ID]


# --- FINDING CURRENT TERM ID ---
"""
for course in courses:
    print(course["name"], course["enrollment_term_id"])
"""


# --- FETCH GRADES FROM CANVAS ---
current_grades = {}
for course in filtered_courses:
    enrollment_data = requests.get(f"{BASE_URL}/courses/{course["id"]}/enrollments", headers=headers, params={"user_id": USER_ID}).json()

    short_name = course["name"][:9] # Only keeping the start of the course name (ex: from "MATH-2660-115 (Spring 2026)" to "MATH-1620")
    grade = enrollment_data[0]['grades']['current_score']
    current_grades[short_name] = grade if grade is not None else 0


# --- PRINT CURRENT CLASSES ---
"""
for course in filtered_courses:
    print(course["name"])
    assignments = requests.get(f"{BASE_URL}/courses/{course["id"]}/assignments", headers=headers, params={"user_id": USER_ID}).json()
    print(assignments[0]['name'])
"""


# --- LOAD HISTORY FILE ---
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = {}


# --- DETERMINE OLD DATA ---
def parse_week_key(key):
    start_str = key.split("_to_")[0]
    return datetime.datetime.strptime(start_str, "%Y-%m-%d")

all_weeks_sorted = sorted(history.keys(), key=parse_week_key)

previous_run_key = all_weeks_sorted[-1] if all_weeks_sorted else None
previous_run_grades = history.get(previous_run_key, {})
previous_week_grades = history.get(previous_week_key, {})

# --- HELPER FUNCTIONS ---
def find_diff(diff):
    """Returns the difference from the previous grade or gpa"""
    if abs(diff) > 0:
        sign = "+" if diff > 0 else ""
        return f" ({sign}{diff:.2f})"
    return ""

def update_grades(old, current):
    """Returns formatted output string with current grades and differences from previous grades."""
    output = ""
    for course, grade in current.items():
        prev_grade = old.get(course, 0)
        diff = grade - prev_grade if prev_grade != 0 else 0
        output += f"   {course}: {grade:.2f}{find_diff(diff)}\n"
    print(output, end='')
    return output

def update_gpa(old, current):
    """Returns formatted output string with current GPA and differences from previous GPA."""
    old_gpa = calculate_gpa(old) if old else 0
    new_gpa = calculate_gpa(current)
    diff = new_gpa - old_gpa if old_gpa != 0 else 0
    print(f"GPA: {new_gpa:.2f}{find_diff(diff)}\n")
    return f"GPA: {new_gpa:.2f}{find_diff(diff)}\n\n"


# --- WRITE GRADES TO ICLOUD_PATH ---
with open(ICLOUD_PATH, "w") as f:
    print(f"Jonah's Grades {week_range}\n{'=' * 28}")
    f.write(f"Jonah's Grades {week_range}\n{'=' * 23}\n")

    # Changes since last run
    print("Changes Since Last Run:")
    update_grades(previous_run_grades, current_grades)
    update_gpa(previous_run_grades, current_grades)

    # Changes since last week
    print("Changes Since Last Week:")
    f.write("Changes Since Last Week:\n")
    f.write(update_grades(previous_week_grades, current_grades))
    f.write(update_gpa(previous_week_grades, current_grades) + "\n\n")


# --- UPDATE HISTORY AND LAST RUN FILES---
history[week_key] = current_grades
with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=4)


print(f"Saved {len(current_grades)} grades for {week_range} to {os.path.basename(ICLOUD_PATH)}")
