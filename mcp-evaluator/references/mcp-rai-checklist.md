# MCP Security & Privacy Checklist (RAI-aligned)

These criteria apply Microsoft's Responsible AI principles and OWASP security guidelines to **MCP server source code and configuration**, not to a trained model.

---

## 1. Credential & Secret Handling

An MCP must never embed credentials in source code, config files committed to version control, or tool responses.

**Check:**
- [ ] No hardcoded tokens, API keys, passwords, or secrets in any `.ts`, `.py`, `.js`, or `.json` source file.
  - Search for: `token =`, `apiKey =`, `secret =`, `password =`, `Bearer `, `Authorization:` with literal values.
- [ ] Credentials are read exclusively from environment variables (`process.env.X`, `os.environ['X']`, `os.getenv('X')`).
- [ ] `.env` files (if any) are listed in `.gitignore` and not committed.
- [ ] `.env.example` or equivalent documents which env vars are required, with placeholder values only (e.g., `LINKEDIN_TOKEN=your_token_here`).
- [ ] Tool responses do not echo back secrets or tokens to the agent/user.

**Common violations:**
- `const TOKEN = "AQV..."` hardcoded in `src/services/linkedin.ts`.
- `mcp.json` containing `"env": {"TOKEN": "actual-token-value"}` committed to a public repo.
- A tool that returns the full Authorization header in its response for debugging.

---

## 2. PII and Data Privacy

MCPs that handle contacts, messages, emails, or phone numbers must minimize PII exposure.

**Check:**
- [ ] The MCP does not log PII (names, phone numbers, email addresses, message content) to stdout/stderr in production mode.
- [ ] PII returned by tools is scoped to what the caller requested — not entire address books or message histories unless explicitly asked.
- [ ] If the MCP caches or stores data locally, sensitive fields are not written in plain text to disk.
- [ ] Tool descriptions and parameter names do not mislead the agent into sending more PII than necessary.
- [ ] If processing EU/AT data (GDPR scope): the MCP does not transfer personal data to third-party endpoints beyond the intended service.

**Common violations:**
- `console.log('Sending to:', phoneNumber, message)` in production code.
- A tool that returns `getAllContacts()` when `findContact(name)` was called.
- Session auth files (e.g., `.wwebjs_auth/`) not excluded from logging or backup pipelines.

---

## 3. Destructive Operations Safety

Operations that cannot be undone — sending messages, publishing posts, deleting records — require explicit confirmation mechanisms.

**Check:**
- [ ] Tools that send/publish/delete accept a `dryRun: boolean` parameter (or equivalent) that previews the action without executing it.
- [ ] The companion SKILL.md (if present) mandates `dryRun: true` before any irreversible call.
- [ ] Tool descriptions explicitly warn when an operation is irreversible (e.g., `"Publishes a post to LinkedIn. This action cannot be undone."`).
- [ ] Delete/remove operations require the caller to pass an explicit identifier — no bulk-delete by pattern without confirmation.
- [ ] If no `dryRun` mechanism exists, the tool description instructs the agent to confirm with the user before calling.

**Common violations:**
- `sendMessage(chatId, text)` with no dryRun — one wrong call sends a real message.
- `createPost(content)` that publishes immediately with no preview step.
- Tool description saying "sends the message" without any warning about irreversibility.

---

## 4. Injection & SSRF Risks

MCPs that accept user-provided input and pass it to shell commands, URLs, or external services are at risk.

**Check:**
- [ ] No `exec()`, `shell=True`, `child_process.exec()`, or equivalent called with unsanitized user input.
  - Prefer `execFile()` or parameterized equivalents.
- [ ] URLs constructed from user input are validated against an allowlist before HTTP requests are made (SSRF prevention).
- [ ] File paths provided by the caller are validated — no path traversal (`../../../etc/passwd`).
- [ ] SQL or query strings are parameterized, not concatenated from user input.
- [ ] If the MCP downloads or processes files from user-provided URLs, mime-type and size are validated.

**Common violations:**
- `exec('curl ' + userProvidedUrl)` — classic command injection + SSRF.
- `fs.readFile(userPath)` without validating that `userPath` is within an allowed directory.
- Constructing API query as `?search=` + unsanitized user string (XSS/injection in third-party API).

---

## 5. Authentication & Token Security

MCPs that authenticate to external services must handle tokens securely throughout their lifecycle.

**Check:**
- [ ] Tokens are loaded at startup from environment, not re-read from disk on every request.
- [ ] Token expiry is handled: the MCP returns a clear error (not a silent failure or crash) when a token is expired.
- [ ] Refresh tokens (if applicable) are stored with the same care as access tokens — env vars or secure vault.
- [ ] The MCP does not expose its own authentication mechanism as a tool parameter (e.g., `createPost(content, token)` would expose the token in tool call logs).
- [ ] HTTPS is enforced for all outbound API calls — no `http://` endpoints for authenticated services.
- [ ] If using OAuth, the redirect flow is not implemented inside the MCP agent context (use a separate setup script).

**Common violations:**
- Token passed as a tool argument: `tool.call({ token: process.env.TOKEN, content })` — token appears in MCP call logs.
- Silent `catch` that swallows a 401 Unauthorized and returns success.
- Using `http://` instead of `https://` for the API base URL.
