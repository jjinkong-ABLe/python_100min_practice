def minutes_to_hours(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return hours, remaining_minutes


def get_focus_message(minutes):
    if minutes < 25:
        return "Short session: warm up and pick one tiny goal."
    if minutes < 60:
        return "Good session: focus on one practice problem."
    return "Deep session: remember to take a break after each hour."


study_minutes = int(input("How many minutes will you study today? "))
hours, minutes = minutes_to_hours(study_minutes)

print("\n=== Study Plan ===")
print(f"Total: {hours} hour(s) {minutes} minute(s)")
print(get_focus_message(study_minutes))

print("\nChecklist")
tasks = ["Open notes", "Write code", "Run and fix errors"]

for index, task in enumerate(tasks, start=1):
    print(f"{index}. {task}")
