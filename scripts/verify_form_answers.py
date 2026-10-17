import re
from pathlib import Path

files_to_check = [
    Path("submission/final_form_answers.md"),
    Path("submission/form_answers.md"),
    Path("submission/release/form_answers.md")
]

for file_path in files_to_check:
    if not file_path.exists():
        continue
    print(f"\nChecking field lengths for: {file_path}")
    content = file_path.read_text(encoding="utf-8")
    sections = re.findall(r"### (Field \d+:[^\n]+)\r?\n```(?:text)?\r?\n([\s\S]*?)\r?\n```", content)
    for title, text in sections:
        char_len = len(text.strip())
        status = "PASS" if char_len <= 1024 else "FAIL (EXCEEDED 1024 LIMIT!)"
        print(f"  {title:45}: {char_len:4} chars [{status}]")
