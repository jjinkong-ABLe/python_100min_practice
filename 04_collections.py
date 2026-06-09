fruits = ["apple", "banana", "cherry"]
fruits.append("grape")
fruits[1] = "blueberry"

print("=== List ===")
print(fruits)
print(fruits[0])
print(fruits[1:3])

coordinates = (37.56, 126.97)

print("\n=== Tuple ===")
print(coordinates)
print(f"Latitude: {coordinates[0]}")

unique_numbers = {1, 2, 2, 3, 3, 3}

print("\n=== Set ===")
print(unique_numbers)
print(2 in unique_numbers)

student = {
    "name": "Jin",
    "major": "biology",
    "level": "beginner",
}

print("\n=== Dictionary ===")
print(student["name"])
student["language"] = "Python"
print(student)
