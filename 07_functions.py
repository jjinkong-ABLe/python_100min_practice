def greet(name):
    return f"Hello, {name}!"


def calculate_total(price, quantity=1):
    return price * quantity


def introduce(name, language="Python", level="beginner"):
    article = "an" if level[0].lower() in "aeiou" else "a"
    print(f"{name} is learning {language} as {article} {level}.")


print("=== Functions ===")
print(greet("Jin"))
print(calculate_total(3000, 4))
print(calculate_total(1500))

introduce("Jin")
introduce(name="Min", level="intermediate", language="Python")
