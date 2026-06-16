---
name: execute-procedure
description: Check and drive the manuscript revision procedure defined in etc/procedure.md. Use when the user asks Codex to inspect workflow progress, determine the next reviewer-response step, write or update procedure-execution.log, route human-only tasks, generate AI-owned workflow artifacts such as structured comments, revision plans, response drafts, or validations, or continue a manuscript revision process while preserving the rule that agents must never modify markup.docx files.
---

# Execute Procedure

## Overview

Use this skill as the controller for the revision workflow described in `etc/procedure.md`. Inspect the current repository state, append an execution log entry to `log/procedure-execution.log`, then either perform the next safe AI-owned action or tell the human exactly what to do next.

## Hard Boundaries

- Treat `etc/procedure.md` as the source of truth for the workflow. Read it before acting if the request depends on step order or file paths.
- Never create, edit, rename, overwrite, accept changes in, or otherwise mutate any file matching `*markup.docx`, `*.rev.markup.docx`, or a user-described markup Word file.
- Never perform manuscript text replacement inside markup Word documents. Draft exact replacement text and instructions for the human; the human applies changes in the markup document.
- Do not convert a markup document into a clean document by accepting tracked changes unless the user explicitly requests that action and the output path is a separate clean file. Even then, leave the markup file untouched.
- Human-only steps must stay human-only. For those steps, log the status and tell the user what to do; do not simulate completion.
- Respect explicit "只提意见", "不要动", "不要动手改 md", or similar instructions over any automation path.

## Standard Run

1. Read `etc/procedure.md`.
2. Inspect relevant files without using stale memory as evidence:
   - `manu/` or `rev1/manu/`
   - `comments/` or `rev1/comments/`
   - `laws/` or `rev1/laws/`
   - `response/` or `rev1/response/`
   - `log/procedure-execution.log`
3. Determine the current workflow step:
   - missing required human input
   - next AI-owned action available
   - validation needed
   - blocked by missing files or ambiguous paths
   - complete enough to move to the next comment
4. Append exactly one log entry for the run to `log/procedure-execution.log`.
5. If the next step is human-only, give a concise instruction to the human and stop.
6. If the next step is AI-owned and the user asked to execute or continue, perform the action, verify the output, append/update the log entry with the result if needed, and report the next step.
7. If the next step is AI-owned but the user only asked to inspect, log and report the proposed action without changing source artifacts.

## Log Format

Create `log/` if it does not exist. Append to `log/procedure-execution.log`; do not write procedure logs elsewhere and do not overwrite previous entries.

Use this compact format:

```markdown
## YYYY-MM-DD HH:MM TZ - <short action>

- Request: <what the user asked>
- Files checked: <paths actually inspected>
- Current step: <procedure step name>
- Status: <done | next-human | next-ai | blocked | needs-review>
- Actions taken: <concrete changes, or "none">
- Verification: <checks actually performed>
- Next: <one concrete next action for human or Codex>
- Boundaries: markup.docx untouched; text replacement remains human-applied
```

Be precise about verification. If you did not open or render a file, say so.

## Step Routing

Use the procedure's ownership labels:

- Human-only: moving/saving Word files, copying reviewer comments from email, checking comment counts and split quality, applying manuscript text edits in markup Word documents, pasting final quotations/page/line numbers.
- AI-owned: converting `origin.docx` to Markdown when requested and tools are available, structuring raw comments, validating structured comments against raw comments, building `revisionplan.md`, generating or updating `response-draft.md`, drafting suggested manuscript changes, drafting response text, inspecting clean/response/supplement files without modification.
- Shared/review: deciding whether a proposed response is acceptable. If unacceptable, explain the issue and do not edit Markdown unless the user explicitly asks for edits.

When choosing the next comment, read `comments/revisionplan.md` or `rev1/comments/revisionplan.md`, sort by "修改序号", and pick the first item not marked complete.

## Artifact Rules

- Preserve reviewer comment text verbatim. Structure, numbering, and headings may be added, but comment content must remain copy-pasted rather than rewritten.
- For `structuredcomments.md`, ensure all raw comment content is represented and no new comment content is invented.
- For `revisionplan.md`, include: reviewer id, comment id, 修改序号, 问题简述, 风险等级, 影响的章节, 修改计划, 是否搞定. Order by 修改序号 using the dependency/locality/risk rules in `etc/procedure.md`.
- For `response-draft.md`, copy comment content exactly, include editor message content when present, and verify comment count and content consistency.
- For response text after a human manuscript edit, use the pattern: thank the reviewer, identify the changed section, summarize the change in one sentence, leave room for the human to paste quotations/page/line numbers.

## Reporting To The User

After each run, answer with:

- current step
- what was logged
- what was changed, if anything
- the next human action or the next AI action available

Keep the answer short unless a blocker requires detail. Do not claim a file is correct unless you actually checked it in the current run.
