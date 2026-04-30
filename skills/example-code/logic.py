"""
Example code-skill logic. Replace with your real skill.

This is the executable half of the `example-code` skill. It exposes a single
`run(input)` function that validates a string against optional length bounds.
The shape (`run` taking a dict, returning a dict) is the contract every code
skill must follow — see Team-Guide.md §4c.
"""

DEFAULT_MIN = 1
DEFAULT_MAX = 10000


def run(input):
    """
    Validate that input["text"] falls within length bounds.

    :param input: dict with keys "text" (str), "min_len" (int, optional),
                  "max_len" (int, optional)
    :return: dict {"ok": bool, "reason": str | None}
    """
    text = input.get("text", "")
    min_len = input.get("min_len", DEFAULT_MIN)
    max_len = input.get("max_len", DEFAULT_MAX)

    if not isinstance(text, str):
        return {"ok": False, "reason": "text is not a string"}
    if len(text) < min_len:
        return {"ok": False, "reason": f"below min_len ({min_len})"}
    if len(text) > max_len:
        return {"ok": False, "reason": f"above max_len ({max_len})"}
    return {"ok": True, "reason": None}
