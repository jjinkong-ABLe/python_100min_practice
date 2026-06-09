a = 17
b = 5

print("=== Arithmetic ===")
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")
print(f"{a} // {b} = {a // b}")
print(f"{a} % {b} = {a % b}")
print(f"{a} ** 2 = {a ** 2}")

print("\n=== Comparison and Logic ===")
print(a > b)
print(a == b)
print(a > 10 and b < 10)
print(a < 10 or b < 10)
print(not a == b)

subjects = ["python", "biology", "statistics"]

print("\n=== Membership ===")
print("python" in subjects)
print("history" not in subjects)
