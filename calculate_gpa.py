def grade_to_gpa(grade):
    """Turning the course grade into a gpa"""
    if grade >= 90: return 4.0   # A
    elif grade >= 80: return 3.0 # B
    elif grade >= 70: return 2.0 # C
    elif grade >= 60: return 1.0 # D
    else: return 0.0             # F

CREDIT_HOURS = {
    "ENGR-1110": 2,
    "COMP-1210": 3,
    "ENGL-1120": 3,
    "MATH-1620": 4,
    "PHYS-1600": 4,
    "COMP-2240": 3,
    "COMP-2210": 4,
    "MATH-2660": 3,
    "PHYS-1610": 4,
    "ARTS-1610": 3,
}

def calculate_gpa(current_grades):
    """Assigning classes with credit hours and calculating the total gpa"""
    total_points, total_hours = 64, 16
    for course, current_grade in current_grades.items():
        hours = CREDIT_HOURS.get(course, 0)
        total_hours += hours
        total_points += hours * grade_to_gpa(current_grade)
    return total_points / total_hours if total_hours else 0