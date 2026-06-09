print("=== For Loop ===")

for number in range(1, 6):
    print(number)

print("\n=== Enumerate ===")

tasks = ["review notes", "write code", "run program"]

for index, task in enumerate(tasks, start=1):
    print(f"{index}. {task}")

print("\n=== While Loop ===")

countdown = 3

while countdown > 0:
    print(countdown)
    countdown -= 1

print("Start!")

print("\n=== Break and Continue ===")

for number in range(1, 10):
    if number == 3:
        continue
    if number == 7:
        break
    print(number)
