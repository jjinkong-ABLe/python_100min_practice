message = "Python makes practice fun"

print("=== Indexing and Slicing ===")
print(message[0])
print(message[-1])
print(message[0:6])
print(message[7:])

print("\n=== String Methods ===")
print(message.lower())
print(message.upper())
print(message.replace("fun", "useful"))
print(message.count("a"))
print(message.startswith("Python"))

name = "Jin"
score = 92

print("\n=== Formatting ===")
print("Student: {}, Score: {}".format(name, score))
print(f"Student: {name}, Score: {score}")
