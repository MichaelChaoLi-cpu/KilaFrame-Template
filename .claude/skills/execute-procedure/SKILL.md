---
name: execute-procedure
description: Drive the manuscript revision workflow from {Rev}/docs/procedure.md. Use when the agent needs to inspect revision progress, identify the current procedure step, route human-only work, execute or dispatch machine-owned work through skills such as convert-origin-docx, build-revision-plan, make-clean-docx, convert-response-docx, and build-response-draft, append {Rev}/docs/procedure-execution.log, choose the next unfinished revision-plan item, or draft response text while preserving the rule that markup docx files are never modified and response-draft.md is only written with explicit per-request human authorization.
---

# Execute Procedure

## Overview

Use this skill as the workflow controller for a revision workspace. Read `{Rev}/docs/procedure.md`, inspect current files, decide the next step, append a log entry, then either dispatch a machine-owned task or tell the human exactly what to do.

This skill is a controller. Keep conversion, revision-plan construction, response formatting, and response-draft generation in dedicated skills when available.

## Inputs

- Workspace root: default to `Rev` unless the user explicitly specifies another name such as `Rev1`.
- Article ID: identify from `{Rev}/origin/{article_id}.docx` when needed.
- Procedure: `{Rev}/docs/procedure.md`.
- Execution log: `{Rev}/docs/procedure-execution.log`.

If `{Rev}` or `{article_id}` is ambiguous, ask the user in Chinese before editing files.

## Hard Boundaries

- Treat `{Rev}/docs/procedure.md` as the source of truth. If it is missing, tell the user to run `build-procedure`.
- Never create, edit, rename, overwrite, accept changes in, move, or delete any file matching `*markup.docx`, `*.rev.markup.docx`, or a user-described markup Word file.
- Never perform manuscript text replacement inside markup Word documents. Draft exact replacement text and instructions for the human; the human applies changes in the markup document.
- Human-only steps must stay human-only. Log the status and tell the user what to do; do not simulate completion.
- Respect explicit "只提意见", "不要动", "不要动手改 md", or similar instructions over any automation path.
- Do not use memory as evidence for current files. Inspect the current repo files.

## Response Draft Write Boundary

Default behavior:

- Draft per-comment response text in the chat for the human to copy.
- Do not write per-comment response text directly into `{Rev}/revision/response-draft.md`.

Writing is allowed only when:

- The human explicitly authorizes writing to `{Rev}/revision/response-draft.md` in the current request.
- The authorization is per request; do not reuse old authorization.

Even with authorization, preserve reviewer comment text exactly and report the changed section.

## Dispatch Skills

Use or invoke these skills when the corresponding task is next:

- `convert-origin-docx`: convert `{Rev}/origin/{article_id}.docx` to `{Rev}/origin/origin.md` and `{Rev}/origin/originsrc/`.
- `build-revision-plan`: create or update `{Rev}/docs/revisionplan.md`, assign execution order, preserve human notes/status, and choose the next unfinished item.
- `make-clean-docx`: copy `{Rev}/revision/{article_id}.rev.markup.docx` to `{Rev}/revision/{article_id}.rev.clean.docx` and accept revisions only in the clean copy; never modify markup.
- `convert-response-docx`: convert `{Rev}/revision/response-draft.md` to `{Rev}/revision/response-draft.docx` using the skill's personal document formatting rules.
- `build-response-draft`: create the initial response draft or generate response text from `{Rev}/docs/structuredcomments.md`, `{Rev}/origin/editormessage.md`, and response template rules.

If a needed dispatch skill is not available, do the safest fallback only if it is simple and unambiguous. Otherwise, log a blocker and tell the user which skill is missing.

## Standard Run

1. Determine `{Rev}`.
2. Read `{Rev}/docs/procedure.md`.
3. Inspect relevant current files:
   - `{Rev}/origin/`
   - `{Rev}/revision/`
   - `{Rev}/docs/`
   - repo files outside `{Rev}/` only when needed for a comment-specific modification plan
4. Determine the current step:
   - missing human input
   - next AI-owned task
   - dispatch-skill task
   - validation task
   - response drafting task
   - review or human-only task
   - blocked by missing files or ambiguity
5. Append exactly one log entry to `{Rev}/docs/procedure-execution.log`.
6. If the next step is human-only, tell the human the concrete next action and stop.
7. If the next step is machine-owned and the user asked to execute or continue, perform or dispatch it, verify output, and report the next step.
8. If the next step is machine-owned but the user only asked to inspect, log and report the proposed action without changing source artifacts.

## Log Format

Create `{Rev}/docs/` if it already should exist but is missing only when this is clearly safe; otherwise tell the user to run `init-revision-workspace`.

Append to `{Rev}/docs/procedure-execution.log`; do not overwrite previous entries.

Use this format:

```markdown
## YYYY-MM-DD HH:MM TZ - <short action>

- Request: <what the user asked>
- Files checked: <paths actually inspected>
- Current step: <procedure step name>
- Status: <done | next-human | next-ai | dispatched | blocked | needs-review>
- Actions taken: <concrete changes, dispatches, or "none">
- Verification: <checks actually performed>
- Next: <one concrete next action for human or agent>
- Boundaries: markup docx untouched; response-draft.md write <not requested | authorized this request | not touched>
```

Be precise about verification. If you did not open, parse, render, or inspect a file, say so.

## Step Routing

Human-only:

- place or save original manuscript, reviewer comments, editor message, or markup docx
- inspect existing `rawcomments.md` or `editormessage.md`
- confirm comment count and splitting quality
- apply manuscript text edits in markup Word documents
- paste final quotations, page numbers, and line numbers
- final review of response docx and revision files

Machine-owned directly in this controller:

- check file presence and workflow status
- structure raw comments into `{Rev}/docs/structuredcomments.md`
- validate structured comments against raw comments
- identify the next unfinished comment using `build-revision-plan` rules and `{Rev}/docs/revisionplan.md`
- inspect repo code, data, scripts, or results outside `{Rev}/` for modification planning
- draft manuscript change suggestions for the human
- draft response text for the human to copy
- request or dispatch revision-plan status updates only after human confirms the response/modification is acceptable

Dispatch to other skills:

- origin docx conversion -> `convert-origin-docx`
- revision plan creation, priority ordering, and status maintenance -> `build-revision-plan`
- clean docx generation -> `make-clean-docx`
- response draft initial build or response template use -> `build-response-draft`
- response docx conversion and formatting -> `convert-response-docx`

Shared/review:

- If the user asks whether a response or modification is acceptable, inspect current files and explain issues.
- If acceptable and the user asked to update plan/log, dispatch revision-plan status maintenance to `build-revision-plan` and log.
- If unacceptable, explain the issue and do not edit Markdown unless the user explicitly asks for edits.

## Artifact Rules

- Preserve reviewer comment text verbatim. Structure, numbering, and headings may be added, but comment content must remain copied rather than rewritten.
- For `{Rev}/docs/structuredcomments.md`, ensure all raw comment content is represented and no new comment content is invented.
- For `{Rev}/docs/revisionplan.md`, rely on `build-revision-plan` for required columns, sorting, status preservation, and coverage checks.
- Sort revision plan by the dependency/locality/risk rules in `{Rev}/docs/procedure.md`.
- When choosing the next comment, follow `build-revision-plan` rules: read `{Rev}/docs/revisionplan.md`, sort by 修改序号, and pick the first item not marked complete.
- For response text after a human manuscript edit, use the pattern: thank the reviewer, identify the changed section, summarize the change in one sentence, leave room for the human to paste quotations/page/line numbers.

## Reporting To The User

Respond in Chinese with:

- current step
- what was logged
- what was changed or dispatched, if anything
- whether `response-draft.md` was untouched or written with current-request authorization
- the next human action or next available machine action

Keep the answer short unless a blocker requires detail.
