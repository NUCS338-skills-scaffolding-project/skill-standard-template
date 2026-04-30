---
skill_id: "example-code"
name: "Example: Length Validator"
skill_type: "code"
tags: ["example", "validation"]
course_types: ["cs"]
learning_goal_tags: ["specify-io"]
trigger_signals: ["input-bounds-needed"]
chip_icon: "📏"
python_entry: "logic.py"
version: "0.1.0"
---

# Example: Length Validator

> ⓘ This is the **example/template code-skill** that ships with the template repo.
> Replace it with your own skill once you've used it as a reference.
> See `Team-Guide.md` for the full schema and conventions.
>
> Note that this is a **code skill**, so it ships a `logic.py` that exposes
> `run(input) -> dict`. Code skills must include a `logic.py`. See
> `skills/example-skill/` for the instructional pattern (no `logic.py`).

## Description

Validates that a string input falls within a configurable length range. A simple stand-in to demonstrate the code-skill folder structure and the `run(input)` contract.

## When to Trigger

- A skill needs to enforce input length bounds before further processing
- A submission requires a min/max character check

## Inputs

A dict with keys:
- `text` (str): the input to validate
- `min_len` (int, optional, default 1): minimum allowed length
- `max_len` (int, optional, default 10000): maximum allowed length

## Outputs

A dict with keys:
- `ok` (bool): whether the input passed
- `reason` (str | None): a short failure reason if `ok` is `False`, otherwise `None`

## Usage

```python
from logic import run

result = run({"text": "hello", "min_len": 1, "max_len": 100})
# result == {"ok": True, "reason": None}

result = run({"text": "", "min_len": 1})
# result == {"ok": False, "reason": "below min_len (1)"}
```

## Notes

Pure function. No side effects. Safe to call repeatedly with the same input.
