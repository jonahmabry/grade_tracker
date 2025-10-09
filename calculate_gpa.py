def grade_to_gpa(grade):
    """Turning the course grade into a gpa"""
    if grade >= 93: return 4.0   # A
    elif grade >= 90: return 3.7 # A-
    elif grade >= 87: return 3.3 # B+
    elif grade >= 83: return 3.0 # B
    elif grade >= 80: return 2.7 # B-
    elif grade >= 77: return 2.3 # C+
    elif grade >= 73: return 2.0 # C
    elif grade >= 70: return 1.7 # C-
    elif grade >= 67: return 1.3 # D+
    elif grade >= 63: return 1.0 # D
    elif grade >= 60: return 0.7 # D-
    else: return 0.0             # F

CREDIT_HOURS = {
    "BUSI-1010": 1,
    "ENGR-1110": 2,
    "COMP-1210": 3,
    "ENGL-1120": 3,
    "BUAL-2600": 3,
    "BUSI-1040": 3,
    "CTCT-3250": 3,
    "ECON-2020": 3,
    "MUSI-2747": 3,
    "MATH-1620": 4,
    "PHYS-1600": 4,
}

def calculate_gpa(current_grades):
    """Assigning classes with credit hours and calculating the total gpa"""
    total_points, total_hours = 0, 0
    for course, current_grade in current_grades.items():
        hours = CREDIT_HOURS.get(course, 0)
        total_hours += hours
        total_points += hours * grade_to_gpa(current_grade)
    return total_points / total_hours if total_hours else 0