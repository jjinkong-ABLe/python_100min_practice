temperature = 28
is_raining = False

print("=== Weather Check ===")

if temperature >= 30:
    print("It is hot.")
elif temperature >= 20:
    print("It is warm.")
else:
    print("It is cool.")

if is_raining:
    print("Take an umbrella.")
else:
    print("No umbrella needed.")

score = 86

print("\n=== Grade Check ===")

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "Keep practicing"

print(f"Score: {score}, Grade: {grade}")
