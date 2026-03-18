# MCP Technical Quality Checklist

These criteria evaluate the technical design, reliability, and completeness of an MCP server implementation.

---

## 1. Tool Design

Good MCP tools are narrow, well-described, and strongly typed. The agent (Claude) uses the tool description to decide when and how to call a tool — a bad description causes misuse.

**Check:**
- [ ] Every tool has a clear, action-oriented `description` that explains: what it does, when to use it, and what it returns.
- [ ] Tool names are in `snake_case` and unambiguous (e.g., `send_whatsapp_message`, not `send` or `doAction`).
- [ ] Every parameter has a `description` that explains its purpose, format, and valid values.
- [ ] Parameters use appropriate types: `string`, `number`, `boolean`, `array`, `object` — not everything is a `string`.
- [ ] Required vs optional parameters are explicitly marked (`required: [...]` in JSON Schema, or equivalent).
- [ ] Tools do one thing — no "god tools" that combine multiple unrelated operations in one call.
- [ ] Return values are structured (JSON object) with documented fields, not raw strings or opaque blobs.

**Common violations:**
- Tool description: `"Sends the message"` — no mention of which service, what inputs, what it returns.
- A `run_command` tool that accepts any shell string — too broad, dangerous.
- All parameters typed as `string` even when a boolean or number would be more appropriate and safer.

---

## 2. Error Handling

An MCP that crashes on bad input or swallows errors silently is unreliable and hard for the agent to recover from.

**Check:**
- [ ] All tool handlers have a top-level try/catch (or equivalent).
- [ ] Errors are returned as structured MCP error responses, not thrown unhandled (which crashes the server).
- [ ] Error messages are informative: they describe what went wrong and, where possible, how to fix it.
  - Good: `"Contact not found: no contact matching 'John Doe'. Try with last name first."`
  - Bad: `"Error"`, `"undefined"`, `"null"`
- [ ] HTTP errors from upstream APIs are caught and translated to meaningful messages (e.g., 401 → "Token expired, please refresh your LinkedIn token").
- [ ] Timeouts are handled — no tool can hang indefinitely waiting for an external service.
- [ ] The server startup fails fast and with a clear message if required environment variables are missing.

**Common violations:**
- `async handler(args) { return await api.send(args) }` — no error handling; a network error crashes the MCP.
- Catching errors but returning `{ success: true }` regardless.
- Missing env var causes a cryptic `TypeError: Cannot read properties of undefined` at runtime instead of `"Missing LINKEDIN_TOKEN environment variable"`.

---

## 3. Companion Skill

A companion SKILL.md transforms a raw MCP into a safe, guided tool for the agent. Without it, the agent uses tools with no guardrails.

**Check:**
- [ ] A companion SKILL.md exists in `~/.copilot/skills/<mcp-name>/SKILL.md`.
- [ ] The skill includes a health/availability check step before attempting operations.
- [ ] The skill mandates confirmation (dryRun or equivalent) before irreversible operations.
- [ ] The skill documents the MCP's known limitations (e.g., "does not support group messages > 1000 members").
- [ ] The skill has a clear installation/troubleshooting path for when the MCP is unavailable.
- [ ] The skill frontmatter `description` includes trigger keywords for the MCP's main use cases.

**Scoring guide:**
- No companion skill + MCP has only read-only tools → PARTIAL
- No companion skill + MCP has write/delete/publish tools → FAIL
- Companion skill exists but has no dryRun/confirmation step → PARTIAL
- Companion skill exists with full safety workflow → PASS

---

## 4. Dependencies & Supply Chain

Outdated or malicious dependencies are a common attack vector.

**Check:**
- [ ] `package.json` / `requirements.txt` pins specific versions (not `"*"` or `"latest"`).
- [ ] No known vulnerable packages in direct dependencies (run `npm audit` or `pip audit` if possible).
- [ ] The MCP does not depend on packages with very low download counts or unknown maintainers for critical operations.
- [ ] `node_modules/` or virtualenv is in `.gitignore` and not committed.
- [ ] Lock file (`package-lock.json`, `yarn.lock`, `poetry.lock`) is committed to ensure reproducible installs.

**Approach for evaluation:**
```bash
# For TypeScript/Node MCPs
cd <mcp-dir> && npm audit --audit-level=high

# For Python MCPs
pip install pip-audit && pip-audit
```

**Common violations:**
- `"sdk": "*"` in package.json — any version, including future breaking or compromised ones.
- No lock file committed — installs may differ across machines.
- `node_modules/` committed to the repo (bloat + security risk).

---

## 5. Logging & Observability

An observable MCP is easier to debug, audit, and trust.

**Check:**
- [ ] The MCP logs startup information (server name, version, which tools are registered).
- [ ] Errors are logged with enough context to diagnose (tool name, input shape, error message).
- [ ] Logs do NOT contain PII or secrets (see mcp-rai-checklist.md §2 and §1).
- [ ] There is a way to know the MCP is running and healthy (e.g., a `healthcheck` tool or startup log message).
- [ ] Log verbosity is controllable — verbose/debug mode is not on by default in production.

**Acceptable logging pattern:**
```typescript
// Good: logs operation type and result shape, not content
console.error(`[send_message] Error sending to chatId=${chatId.slice(-6)}: ${err.message}`)

// Bad: logs full PII
console.log(`Sending "${messageText}" to ${phoneNumber} (${contactName})`)
```

**Common violations:**
- No logging at all — impossible to diagnose failures.
- `console.log(JSON.stringify(args))` in every handler — logs all inputs including message content and contact data.
- No healthcheck mechanism — agent cannot verify the MCP is alive before attempting operations.

---

## Quick Reference: Scoring Summary

| Section | PASS | PARTIAL | FAIL |
|---------|------|---------|------|
| Tool Design | All tools well-described, typed, single-purpose | Minor gaps in descriptions or types | God tools, no descriptions, dangerous open parameters |
| Error Handling | try/catch everywhere, informative errors | Some handlers unprotected | Unhandled crashes, silent swallowing |
| Companion Skill | Exists with dryRun + health check | Exists but missing safety steps | Absent + MCP has destructive tools |
| Dependencies | Pinned versions, audit clean, lock file | Minor audit warnings, or missing lock | Critical vulnerabilities, `*` versions |
| Logging | Startup info, error context, no PII | Some PII leakage or no healthcheck | No logging or full PII in logs |
