# LLM artwork notes parser

A small Python project that turns messy notes from artwork files (quantity and scale
written in many different ways) into clean JSON using an LLM API.

Example:

    "3 pcs - scala 1/20"  ->  {"quantity": 3, "scale": "1:20", "needs_review": false}

## How it works

- `parser.py` sends one note to the Claude API and asks for a fixed JSON format.
- The output is validated in code (integer quantity, scale like `1:50`, boolean flag).
  Anything invalid or doubtful becomes `needs_review: true` instead of being trusted.
- `run_tests.py` runs `cases.json` (20 invented notes with expected answers) and prints
  accuracy per field and every failure.

## Run it

    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=your_key_here   # Windows PowerShell: $env:ANTHROPIC_API_KEY="your_key_here"
    python run_tests.py

Try a single note: `python parser.py "Qty 4x, scale 1:50"`

## Results

TODO: Not evaluated yet. This is a first version that has not been run against the full test set.

## Limits

TODO: Early starter project. The test notes are invented, not real customer data, and the prompt has not been tuned.
