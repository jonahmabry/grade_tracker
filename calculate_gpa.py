# Turning the course grade into a gpa
def grade_to_gpa(grade):
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

def calculate_gpa(grades_list):
    total_points = 0
    total_hours = 0

    for course in grades_list:
        # Assigning classes with credit hours and adding up total hours
        match course:
            case "ENGR-1110":
                grades_list[course]['credit_hours'] = 2
                total_hours += 2
            case "COMP-1210" | "ENGL-1120":
                grades_list[course]['credit_hours'] = 3
                total_hours += 3
            case "MATH-1620" | "PHYS-1600":
                grades_list[course]['credit_hours'] = 4
                total_hours += 4
            case _:
                grades_list[course]['credit_hours'] = 0

        # Turning the class grade into a gpa and then calculating the total gpa
        class_gpa = grade_to_gpa(grades_list[course]['grade'])
        total_points += grades_list[course]['credit_hours'] * class_gpa

    gpa = total_points / total_hours
    print(f"GPA: {gpa}")

    return gpa