name = "Jin"
birth_year = "2005"
favorite_subjects = ["Python", "biology", "data analysis"]

current_year = 2026
age = current_year - int(birth_year)

print("=== Profile ===")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Subjects: {', '.join(favorite_subjects)}")

print("\n=== Quick Checks ===")
print(f"Is adult? {age >= 20}")
print(f"Likes Python? {'Python' in favorite_subjects}")
print(f"Next year age: {age + 1}")
