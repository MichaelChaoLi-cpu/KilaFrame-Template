---
name: build-response-draft
description: Build response-to-reviewers Markdown drafts and per-comment response text from structured reviewer comments. Use when the agent needs to create the initial {Rev}/revision/response-draft.md from {Rev}/docs/structuredcomments.md and {Rev}/origin/editormessage.md, or draft response text for a specific comment while preserving reviewer wording and only writing to response-draft.md with explicit per-request human authorization.
---

# Build Response Draft

## Overview

Create the initial response draft or draft per-comment response text using the bundled response template. This skill preserves reviewer/editor wording and respects the write boundary for `{Rev}/revision/response-draft.md`.

## Required Reference

Read `references/response-template.md` before creating an initial draft or response text.

## Inputs

- Workspace root: default to `Rev` unless the user specifies another root such as `Rev1`.
- Structured comments: `{Rev}/docs/structuredcomments.md`.
- Editor message: `{Rev}/origin/editormessage.md`.
- Response draft: `{Rev}/revision/response-draft.md`.
- Optional current comment context from `{Rev}/docs/revisionplan.md`.

## Write Boundary

Initial draft:

- This skill may create `{Rev}/revision/response-draft.md` when the user asks for initial draft generation and the file does not exist.
- If the file exists, do not overwrite it unless the user explicitly requests regeneration or update.

Per-comment response:

- Default: output response text in chat for the human to copy into `{Rev}/revision/response-draft.md`.
- Do not write per-comment response text directly to `{Rev}/revision/response-draft.md` unless the human explicitly authorizes writing in the current request.
- Authorization is per request and cannot be reused.

## Initial Draft Rules

When creating the initial draft:

1. Start from `references/response-template.md`.
2. Copy editor message content from `{Rev}/origin/editormessage.md` when present.
3. Copy reviewer comment content from `{Rev}/docs/structuredcomments.md` exactly.
4. Preserve reviewer and comment headings.
5. Add response placeholders after each comment.
6. Leave line/page placeholders for human completion.
7. Verify comment count and copied comment text against structured comments.

## Per-Comment Response Rules

When drafting a response after human manuscript edits:

- Thank the reviewer.
- Identify the changed section.
- Summarize the change in one sentence.
- Leave a clear placeholder for human to paste article quotation, page number, and line number.
- Do not claim changes that are not supported by current files.
- If current files do not support the response, explain the issue instead of drafting a false response.

## Forbidden Actions

- Do not modify any `.docx`.
- Do not modify markup DOCX.
- Do not rewrite reviewer or editor comments.
- Do not fabricate line/page numbers.
- Do not mark revision plan items complete; `execute-procedure` owns that after human confirmation.

## Verification

After creating or updating an initial draft, verify:

1. `{Rev}/revision/response-draft.md` exists.
2. Reviewer comment count matches `{Rev}/docs/structuredcomments.md`.
3. Reviewer comment text is copied exactly.
4. Editor message handling is reported.

For per-comment response text, verify that the response is grounded in current files or clearly label it as a draft pending human confirmation.

## User Report

Respond in Chinese with:

- whether an initial draft was created, updated, left unchanged, or only response text was drafted in chat
- whether `response-draft.md` was written with current-request authorization
- comment count/text verification result when applicable
- any missing input or blocker
