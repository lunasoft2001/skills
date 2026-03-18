# AgentSkills.io — Format & Quality Criteria for Skills

Reference: https://agentskills.io/skill-creation/evaluating-skills

These criteria assess whether a skill follows the AgentSkills.io open standard for format, efficiency, and eval quality.

---

## 1. Structure & Format

A skill must follow the canonical directory structure.

**Check:**
- [ ] The skill directory contains a `SKILL.md` file at the root.
- [ ] The only allowed subdirectories are `scripts/`, `references/`, `assets/`, and `evals/`.
- [ ] No extraneous files exist: no `README.md`, `INSTALLATION_GUIDE.md`, `CHANGELOG.md`, `QUICK_REFERENCE.md`.
- [ ] Bundled scripts are in `scripts/`, reference docs in `references/`, templates/assets in `assets/`.
- [ ] If evals exist, they are in `evals/evals.json` following the required schema.

**Canonical structure:**
```
skill-name/
├── SKILL.md
├── scripts/          (optional)
├── references/       (optional)
├── assets/           (optional)
└── evals/
    └── evals.json    (optional but recommended)
```

**Common violations:**
- README.md included alongside SKILL.md.
- Scripts placed at the root instead of `scripts/`.
- Random documentation files that are not reference material.

---

## 2. Frontmatter Quality

The frontmatter (`name` + `description`) is the most critical part of the skill. It determines when and whether the skill triggers.

**Check:**
- [ ] `name` field is present, lowercase, hyphen-separated, and matches the directory name.
- [ ] `description` field is present and comprehensive — it should cover:
  - What the skill does
  - When to use it (use cases, scenarios)
  - Explicit trigger keywords and phrases (including language variants if applicable)
- [ ] The description is specific enough to trigger in the right context but not so narrow it misses valid requests.
- [ ] The description does NOT repeat information obvious from the name alone.
- [ ] Optional `license` field is present for public skills.
- [ ] No unknown or extra frontmatter fields that agents won't recognize.

**Good description pattern:**
> "[One sentence what it does]. Use when [scenarios]. Triggers on: [keyword list including language variants]."

**Common violations:**
- Description is one generic sentence like "Helps with X tasks."
- No trigger keywords — the agent has to guess when to use it.
- `name` field doesn't match the actual directory name.

---

## 3. Body Conciseness (Context Efficiency)

The body is only loaded when the skill triggers — but it still consumes context window tokens. Every instruction must justify its token cost.

**Check:**
- [ ] The body does NOT explain concepts Claude already knows (e.g., "JSON is a data format used for...").
- [ ] Instructions are action-oriented, not explanatory prose.
- [ ] No redundant instructions — the same guidance is not repeated in multiple places.
- [ ] Large reference material (schemas, API docs, detailed policies) is in `references/` files, not embedded in the body.
- [ ] Examples are concise and illustrative — not exhaustive multi-paragraph walkthroughs.
- [ ] The body is under ~5,000 words. If longer, split into references.
- [ ] The skill uses appropriate degrees of freedom:
  - High freedom (text) for tasks where multiple approaches are valid.
  - Low freedom (specific scripts or step sequences) only when operations are fragile or must be exact.

**Common violations:**
- Body contains a full API documentation copy that belongs in `references/api_docs.md`.
- Verbose explanations like "This step is important because..." for self-evident actions.
- Scripts embedded inline in the body instead of in `scripts/` files.

---

## 4. Bundled Resources Appropriateness

Bundled resources should add value without bloating the skill.

**Check:**
- [ ] `scripts/` only contains code that is reused across multiple runs or is too fragile to regenerate reliably.
- [ ] Scripts are executable, correct, and tested — a broken script is worse than no script.
- [ ] `references/` files contain documentation Claude needs to consult (not copy into outputs).
- [ ] `assets/` files are used in outputs — not just stored for information.
- [ ] No binary files in `references/` or `scripts/`. Only text-based files belong there.
- [ ] File sizes are reasonable — a `references/` file over 50KB should be split or summarized.

**Common violations:**
- A one-off script included in `scripts/` that is only used once and is simple enough for Claude to write on the fly.
- Reference files that duplicate what's already in SKILL.md.
- Large binary assets in `references/` instead of `assets/`.

---

## 5. Eval Coverage

Evals provide evidence that the skill works and improves on the baseline. Recommended for skills submitted for public publishing.

**Check (if `evals/evals.json` exists):**
- [ ] Each eval has: `id`, `prompt`, `expected_output`.
- [ ] Prompts are realistic user messages — varied phrasing, not template-like.
- [ ] At least 2-3 test cases covering different scenarios.
- [ ] At least one edge case (malformed input, unusual request, boundary condition).
- [ ] Each eval includes `assertions` — specific, verifiable statements about the output.
- [ ] Assertions are concrete: "Output file is valid JSON", "Report includes at least 3 recommendations" — not vague like "Output is good".

**Check (if `evals/evals.json` does NOT exist):**
- [ ] For simple single-purpose skills, absence of evals is acceptable (PARTIAL, not FAIL).
- [ ] For complex multi-step skills or public submission candidates, evals are required.

**eval schema reference:**
```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user message here",
      "expected_output": "Description of what success looks like",
      "files": ["evals/files/sample.csv"],
      "assertions": [
        "The output includes X",
        "The output does not contain Y",
        "The result file is valid JSON"
      ]
    }
  ]
}
```

**Common violations:**
- Prompts like "use the skill" — too vague to test anything.
- Assertions like "The output is correct" — unverifiable.
- Only happy-path test cases, no edge cases.
- Evals that test what Claude can do without the skill — not evidence of the skill's value.

---

## Eval Maturity Levels

Use this scale when scoring eval coverage:

| Level | Description |
|-------|-------------|
| **None** | No evals directory — PARTIAL for simple skills, FAIL for complex/public skills |
| **Basic** | 1-2 test cases, no assertions — PARTIAL |
| **Standard** | 2-3 test cases with assertions covering main scenarios — PASS |
| **Advanced** | 3+ test cases including edge cases, assertions, baseline comparison data — PASS+ |
