student_name = "Jin"
grade = 2
height_cm = 164.5
is_enrolled = True

birth_year_text = "2005"
current_year = 2026
age = current_year - int(birth_year_text)

print("=== Variables and Types ===")
print(f"Name: {student_name}")
print(f"Grade: {grade}")
print(f"Height: {height_cm} cm")
print(f"Enrolled: {is_enrolled}")
print(f"Age: {age}")

print("\n=== Type Checks ===")
print(type(student_name))
print(type(grade))
print(type(height_cm))
print(type(is_enrolled))
