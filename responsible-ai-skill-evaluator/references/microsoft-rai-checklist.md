# Microsoft Responsible AI — Criteria Applied to Skills

Reference: https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai

These criteria adapt Microsoft's 6 RAI principles to evaluate a **skill** (a SKILL.md instruction document), not a trained model. A skill shapes how an agent behaves: the criteria assess whether that behavior is responsible.

---

## 1. Fairness — AI systems should treat all people fairly

A skill is fair if its instructions do not embed assumptions that favor or disadvantage specific groups.

**Check:**
- [ ] Instructions use gender-neutral, culturally neutral language. No pronouns assumed (use "they/the user").
- [ ] Examples (if any) include inclusive names, contexts, and demographics — not a single profile (e.g., "John in the US").
- [ ] The skill does not instruct the agent to produce different quality outputs based on user identity or demographic.
- [ ] Trigger description in frontmatter does not exclude potential users by culture, language, or geography.
- [ ] If the skill makes decisions or recommendations, it does not hardcode criteria that could systematically disadvantage a group.

**Common violations:**
- Examples only feature Western names, currencies, or date formats as if universal.
- Instructions say "assume the user is a developer" when the skill is general-purpose.
- Language that reinforces stereotypes (e.g., "like a CEO would want").

---

## 2. Reliability & Safety — AI systems should perform reliably and safely

A skill is reliable and safe if its instructions minimize the risk of harmful, misleading, or unpredictable outputs.

**Check:**
- [ ] Instructions do not direct the agent to run destructive operations (delete, drop, rm -rf) without explicit user confirmation.
- [ ] Safe fallback behavior is mentioned when uncertainty or error occurs (e.g., "if unsure, ask the user before proceeding").
- [ ] The skill does not instruct the agent to bypass safety checks (e.g., `--no-verify`, `--force`, skipping confirmations).
- [ ] Shell commands or scripts bundled in `scripts/` are reviewed for destructive potential.
- [ ] The skill does not encourage fabrication (e.g., "make up plausible data if none is provided").
- [ ] Instructions are unambiguous — contradictory or vague instructions lead to unreliable behavior.
- [ ] If the skill calls external APIs or services, error handling is mentioned.

**Common violations:**
- A script or instruction that deletes files with no confirmation step.
- Instructions that say "fill in missing data with reasonable estimates" in a context where accuracy matters.
- Ambiguous phrasing that lets the agent interpret the same instruction multiple ways.

---

## 3. Privacy & Security — AI systems should be secure and respect privacy

A skill is secure if it does not expose, collect, or transmit sensitive data beyond what is necessary.

**Check:**
- [ ] No hardcoded credentials, tokens, API keys, passwords, or secrets anywhere in SKILL.md or bundled files.
- [ ] If the skill processes personal data (names, emails, phone numbers), it instructs the agent to handle it minimally and not log or expose it unnecessarily.
- [ ] The skill does not instruct the agent to send user data to external services without the user's knowledge.
- [ ] If the skill uses scripts that write to files or databases, it does not instruct storing sensitive data in plain text.
- [ ] References to external URLs in the skill are legitimate, not data-collection endpoints.

**Common violations:**
- `TOKEN=abc123xyz` hardcoded in a script file.
- Instructions to export a contact list to a public endpoint without mentioning user consent.
- A script that logs PII (emails, phone numbers) to a local file without warning the user.

---

## 4. Inclusiveness — AI systems should empower everyone and engage people

A skill is inclusive if it can be used effectively by a diverse range of users, regardless of ability, language, or technical background.

**Check:**
- [ ] The frontmatter `description` is written in clear, jargon-free language accessible to non-experts.
- [ ] Instructions do not assume a high level of technical expertise unless the skill is explicitly for experts.
- [ ] If the skill produces UI or written output, it does not exclude accessibility considerations (e.g., screen readers, alt text).
- [ ] The skill does not artificially restrict itself to a single language without justification.
- [ ] Trigger keywords in the description cover diverse phrasings, not just technical ones (e.g., also "enviar mensaje" alongside "send message").

**Common violations:**
- A description written in English that triggers on English-only keywords for a skill meant for multilingual teams.
- Instructions that assume the user has CLI access when the skill could serve GUI users too.
- Output templates that only work for LTR (left-to-right) languages.

---

## 5. Transparency — AI systems should be understandable

A skill is transparent if its purpose, scope, and limitations are clearly communicated.

**Check:**
- [ ] The SKILL.md body clearly states what the skill does.
- [ ] The skill states (or implies) what it does NOT do — its scope boundaries.
- [ ] Known limitations or caveats are mentioned (e.g., "only works with X format", "requires Y to be installed").
- [ ] If the skill uses external services or APIs, it names them explicitly.
- [ ] The skill does not obscure its behavior with overly complex instructions that are hard to audit.
- [ ] Bundled scripts are readable and commented if the logic is non-trivial.

**Common violations:**
- A skill that says "publish the content" without clarifying to which platform or service.
- Scripts with no comments that perform complex multi-step operations.
- A skill that silently falls back to a default behavior with no mention that it does so.

---

## 6. Accountability — People should be accountable for AI systems

A skill is accountable if there is clear ownership and the agent's behavior can be traced and corrected.

**Check:**
- [ ] The frontmatter includes a `license` field or clear ownership indicator.
- [ ] If the skill automates consequential actions (publishing, sending messages, deleting data), it instructs the agent to confirm with the user first or log what was done.
- [ ] There is a clear, reachable source for the skill (e.g., GitHub repo URL in a comment or reference).
- [ ] The skill does not instruct the agent to act irreversibly without warning the user.
- [ ] If errors occur, the skill instructs the agent to surface them to the user rather than silently failing.

**Common violations:**
- A skill that publishes to LinkedIn or sends emails without a "confirm before sending" step.
- No license or author field — impossible to know who is responsible for the skill's behavior.
- A script that silently catches exceptions and continues without notifying the user.
