"""Run parser.py against cases.json and report accuracy and failures."""
import json

from parser import parse_note

FIELDS = ["quantity", "scale", "needs_review"]


def main():
    with open("cases.json", encoding="utf-8") as f:
        cases = json.load(f)

    field_hits = {k: 0 for k in FIELDS}
    full_hits = 0
    failures = []

    for case in cases:
        result = parse_note(case["input"])
        expected = case["expected"]
        ok = True
        for k in FIELDS:
            if result[k] == expected[k]:
                field_hits[k] += 1
            else:
                ok = False
        if ok:
            full_hits += 1
        else:
            failures.append((case["input"], expected, result))

    total = len(cases)
    print(f"Fully correct: {full_hits}/{total} ({full_hits / total:.0%})")
    for k in FIELDS:
        print(f"  {k}: {field_hits[k]}/{total}")

    if failures:
        print("\nFailures:")
        for text, expected, result in failures:
            print(f"- {text!r}\n    expected {expected}\n    got      {result}")


if __name__ == "__main__":
    main()
