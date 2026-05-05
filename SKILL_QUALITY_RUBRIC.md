# Skill Quality Rubric

Self-check this list before pushing a skill to your team repo.
A skill that passes every item here will land as `status: ready` in the
registry on the next build — no back-and-forth with the Admin needed.

The catalog builder enforces the **Required** items automatically; a missing
required field sets your skill to `stub` or `broken`.
The **Recommended** and **Quality** items are not machine-checked, but they
determine whether the skill actually works well in real student sessions.

---

## Required fields (machine-enforced)

These must be present and non-empty in your `skills.md` frontmatter.
A missing required field → `status: stub`.

| Field | Notes |
|---|---|
| `skill_id` | Globally unique bare slug, e.g. `counter-example`. Matches your folder name. |
| `name` | Human-readable display name, title-cased. |
| `skill_type` | `instructional` or `code`. |
| `owner_team` | Your course/team identifier, e.g. `PHIL-270`. |
| `owner_contact` | Email or GitHub handle of the skill's maintainer. |
| `tags` | At least one tag. Used for skill search and selection. |
| `status` | Set to `ready` when the skill is complete. (`stub` is the default.) |
| `version` | Semver string, e.g. `0.1.0`. Bump on every meaningful change. |

For `instructional` skills, these body sections are also required:

| Section | Notes |
|---|---|
| `## Description` | One-paragraph summary of what the skill does. |
| `## When to Trigger` | Describes the student states or signals that activate this skill. |
| `## Flow` | Numbered steps. At least 2 steps. |
| `## Tutor Stance` | Bullet list of behavioural rules for the model. |

For `code` skills, `python_entry` must point to a file that exports `run(input: dict) -> dict`.

---

## Recommended fields (not machine-enforced, but strongly encouraged)

These significantly improve skill selection accuracy and quality.

| Field / Section | Why it matters |
|---|---|
| `stance` | `socratic`, `hint`, `reframe`, or `meta`. Tells the selector which *kind* of intervention to use. Without it, selection scoring ignores stance. |
| `trigger_signals` | List of 3–8 slug-style signals (e.g. `student-stuck`, `student-gold-plating`). These are the primary matching signals for the skill selector. |
| `learning_goal_tags` | Tags from `vocab/learning_goals.yaml`. Link the skill to learning outcomes. |
| `course_types` | `cs`, `humanities`, or both. Narrows selection to the right context. |
| `## Safe Output Types` | What the model is *allowed* to produce. Constrains hallucination. |
| `## Must Avoid` | Hard prohibitions (e.g. "Never give the answer directly"). Critical for instructional safety. |
| `## Example Exchange` | A short realistic dialogue. Used by the LLM as a tone reference. |

---

## Quality checks (human judgment)

Run through these before marking `status: ready`.

### Trigger signals
- [ ] Do the `trigger_signals` represent things a student would actually *say or do*, not abstract concepts?
- [ ] Are there at least 4 signals? Fewer than 4 reduces selector precision.
- [ ] Are the signals distinct from signals used by other skills on your team?

### Flow
- [ ] Does each flow step end with a clear action the *tutor* takes (not the student)?
- [ ] Does the flow have a natural beginning (surface the problem), middle (engage), and resolution (check for understanding)?
- [ ] Would a tutor following this flow never need to give away the answer?

### Tutor stance rules
- [ ] Are the rules written as explicit behavioural constraints, not vague intentions?
  - Good: "Never provide more than one hint per turn."
  - Weak: "Be helpful and supportive."
- [ ] Do the rules prevent the most common failure mode for this skill type?
  - Socratic: slipping into giving the answer.
  - Hint: giving too much too fast.
  - Reframe: dismissing the student's framing entirely.
  - Meta: moralising or lecturing instead of reflecting.

### Must Avoid
- [ ] Is there at least one must-avoid rule?
- [ ] Does it cover the most dangerous failure mode (usually: giving the answer)?

### Stance consistency
- [ ] Does the `stance` field match the actual behaviour described in the flow and stance rules?
- [ ] If `socratic`: every flow step should involve asking a question.
- [ ] If `hint`: the first step should surface *where* the student is stuck, not jump to the hint.
- [ ] If `reframe`: there should be a step that explicitly acknowledges the student's original frame before offering an alternative.
- [ ] If `meta`: the flow should address the student's *process* or *mindset*, not the content of their work.

### For code skills specifically
- [ ] Does `logic.py::run(input)` return a dict (not raise on valid inputs)?
- [ ] Are `inputs_schema` and `outputs_schema` present and accurate?
- [ ] Are there at least 2 fixture pairs in `fixtures/` covering a typical and an edge-case input?

---

## Quick validation command

Run this from the root of the skills-registry repo to check your skill before pushing:

```bash
python scripts/catalog_builder.py \
  --local /path/to/parent/dir \
  --strict \
  --report /tmp/build_report.md

# Then inspect your skill's entry:
grep -A 10 "your-skill-id" /tmp/build_report.md
```

A clean output shows `status: ready`. Any `stub` or `broken` entry will include the specific field or section that is missing.

---

## Coverage gaps to avoid

The registry tracks coverage across stances and course types. Before publishing,
check whether your skill fills a gap or duplicates existing coverage:

```bash
python scripts/catalog_builder.py --local /path/to/parent --output /tmp/catalog.json
python -c "
import json, collections
cat = json.load(open('/tmp/catalog.json'))
stances = collections.Counter(s.get('stance','none') for s in cat)
print('Stance coverage:', dict(stances))
"
```

The registry currently has no `reframe`-stance skills and no humanities-only skills.
If your course is non-CS, a reframe or meta skill for humanities contexts would
fill a real gap.

---

## Checklist summary (copy-paste version)

```
## Before pushing — skill quality checklist

Required fields
- [ ] skill_id (unique slug, matches folder name)
- [ ] name, skill_type, owner_team, owner_contact
- [ ] tags (≥1), status: ready, version (semver)
- [ ] For instructional: Description, When to Trigger, Flow (≥2 steps), Tutor Stance
- [ ] For code: python_entry, logic.py::run() returns dict

Recommended fields
- [ ] stance set (socratic / hint / reframe / meta)
- [ ] trigger_signals (≥4 slugs)
- [ ] learning_goal_tags from vocab/learning_goals.yaml
- [ ] course_types
- [ ] Safe Output Types and Must Avoid sections

Quality
- [ ] Trigger signals describe observable student behaviour
- [ ] Flow has beginning / middle / resolution
- [ ] Tutor stance rules are specific behavioural constraints
- [ ] Must Avoid covers the primary failure mode
- [ ] Stance field matches behaviour in flow + rules
- [ ] For code: fixture pairs cover typical + edge-case inputs

Validation
- [ ] catalog_builder.py --strict shows status: ready
- [ ] build_report.md shows no errors for this skill_id
```
