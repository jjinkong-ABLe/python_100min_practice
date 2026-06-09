def count_vowels(text):
    vowels = "aeiou"
    count = 0

    for char in text.lower():
        if char in vowels:
            count += 1

    return count


def summarize_scores(scores):
    total = sum(scores)
    average = total / len(scores)
    highest = max(scores)
    lowest = min(scores)
    return total, average, highest, lowest


print("=== Mini Project 1: Vowel Counter ===")
sentence = "Python practice makes code easier"
print(sentence)
print(f"Vowels: {count_vowels(sentence)}")

print("\n=== Mini Project 2: Score Summary ===")
scores = [88, 92, 76, 95, 84]
total, average, highest, lowest = summarize_scores(scores)
print(f"Scores: {scores}")
print(f"Total: {total}")
print(f"Average: {average:.1f}")
print(f"Highest: {highest}")
print(f"Lowest: {lowest}")
