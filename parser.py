"""Turn messy artwork notes into clean structured data using an LLM."""
import json
import re

from anthropic import Anthropic

MODEL = "claude-sonnet-5-5"

SYSTEM = """You extract data from messy notes written on signage artwork files.
Return ONLY a JSON object with exactly these keys:
- "quantity": integer, or null if missing or unclear
- "scale": string in the form "1:50", or null if missing or unclear
- "needs_review": true if quantity or scale is missing, ambiguous or
  contradictory, otherwise false
Notes can be in English, Danish, Italian or mixed. Write scales as
"1:N" even if the note says "1/20" or "1 to 20". Do not guess.
No other text, no explanations, no code fences."""

SCALE_PATTERN = re.compile(r"^\d+:\d+$")  #regex to match scales format like "1:50"
FALLBACK = {"quantity": None, "scale": None, "needs_review": True}


def validate(data):
    """Check the model output. Anything doubtful is marked for human review."""
    if not isinstance(data, dict):
        return dict(FALLBACK)
    quantity = data.get("quantity")
    scale = data.get("scale")
    review = data.get("needs_review")
    if quantity is not None and (isinstance(quantity, bool) or not isinstance(quantity, int)):
        return dict(FALLBACK)
    if scale is not None and not (isinstance(scale, str) and SCALE_PATTERN.match(scale)):
        return dict(FALLBACK)
    if not isinstance(review, bool):
        return dict(FALLBACK)
    return {"quantity": quantity, "scale": scale, "needs_review": review}


def parse_note(text, client=None):
    client = client or Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,  # the model may think first, and thinking counts against this limit
        system=SYSTEM,
        messages=[{"role": "user", "content": text}],
    )
    # The reply can start with a thinking block, so pick the text block explicitly.
    raw = next((b.text for b in response.content if b.type == "text"), "").strip()
    try:
        return validate(json.loads(raw))
    except json.JSONDecodeError:
        return dict(FALLBACK)


if __name__ == "__main__":
    import sys

    print(json.dumps(parse_note(" ".join(sys.argv[1:])), indent=2))
