def to_number(text):
    try:
        number = int(text)
    except ValueError:
        return None
    else:
        return number
    finally:
        print(f"Checked value: {text}")


samples = ["10", "3", "python", "25"]

print("=== Exception Handling ===")

for sample in samples:
    result = to_number(sample)

    if result is None:
        print("Could not convert to number.")
    else:
        print(f"Converted number: {result}")
