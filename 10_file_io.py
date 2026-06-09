from pathlib import Path


output_path = Path(__file__).with_name("study_log.txt")
lines = [
    "Python practice log",
    "1. Variables",
    "2. Loops",
    "3. Functions",
]

output_path.write_text("\n".join(lines), encoding="utf-8")

print("=== File Write ===")
print(f"Wrote {output_path}")

print("\n=== File Read ===")
content = output_path.read_text(encoding="utf-8")
print(content)
