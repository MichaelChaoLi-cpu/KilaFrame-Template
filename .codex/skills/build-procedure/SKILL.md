---
name: build-procedure
description: Generate a manuscript revision procedure from the fixed template. Use when Codex needs to create or update {Rev}/docs/procedure.md for a revision workspace initialized by init-revision-workspace, identify article_id from {Rev}/origin/{article_id}.docx, apply only user-specified project adjustments, and preserve the rules that markup docx files are never modified and response-template rules are supplied by a separate skill.
---

# Build Procedure

## Overview

Create `{Rev}/docs/procedure.md` from `references/procedure-template.md`. This skill does not execute the revision workflow, generate comments, build response drafts, convert Word files, or edit markup documents.

## Required Reference

Read `references/procedure-template.md` before generating or updating a procedure.

## Inputs

- Workspace root: default to `Rev` unless the user explicitly specifies another name such as `Rev1`.
- Article ID: identify from exactly one file matching `{Rev}/origin/*.docx`.
- Project adjustments: apply only changes explicitly provided by the user.

If any input is ambiguous, ask the user in Chinese before editing files.

## Preconditions

1. Confirm `{Rev}/` exists and is a directory.
2. Confirm `{Rev}/origin/`, `{Rev}/revision/`, and `{Rev}/docs/` exist.
3. Identify `{article_id}` from `{Rev}/origin/{article_id}.docx`.
4. If no candidate origin docx exists, stop and ask the user to place `{Rev}/origin/{article_id}.docx`.
5. If multiple candidate origin docx files exist, stop and ask the user which one defines `{article_id}`.
6. Ignore temporary Word files such as names beginning with `~$` when identifying article ID.

Do not infer `{article_id}` from markup, clean, response, log, or memory.

## Output Rules

Output path:

```text
{Rev}/docs/procedure.md
```

Generation rules:

1. Copy the fixed template.
2. Replace `{Rev}` with the selected workspace root.
3. Replace `{article_id}` with the identified article ID.
4. Apply only user-specified project adjustments.
5. Preserve the hard boundary that agent must not modify, overwrite, move, delete, or accept changes in markup docx files.
6. Preserve the rule that `response-template` is not owned by `build-procedure`; it is provided by another skill called by `execute-procedure`.
7. Preserve the rule that agent may inspect repo code/data/scripts/results outside `{Rev}/` to construct revision plans, without assuming fixed directory names.

## Existing Procedure

If `{Rev}/docs/procedure.md` already exists:

- If the user explicitly asked to overwrite, rebuild, or update it, update the file.
- Otherwise, do not overwrite it. Report that it already exists and ask whether to update, replace, or leave it unchanged.

When updating an existing procedure, keep user edits unless the user explicitly requests regeneration from the fixed template.

## Forbidden Actions

- Do not create or edit `response-draft.md`.
- Do not create or edit `revisionplan.md`.
- Do not create or edit `structuredcomments.md`.
- Do not create or edit `procedure-execution.log`.
- Do not create, edit, move, delete, or rewrite any `.docx`.
- Do not modify markup docx files under any circumstance.
- Do not invent project-specific procedure steps without user instruction.

## Verification

After writing `{Rev}/docs/procedure.md`, verify:

1. The file exists.
2. The selected workspace root appears in the procedure.
3. The identified article ID appears in the procedure.
4. No `{Rev}` or `{article_id}` placeholders remain unless the user explicitly requested placeholders.
5. The procedure contains the markup docx no-write rule.
6. The procedure keeps `response-template` outside `build-procedure`.

If verification fails, fix the procedure if the fix is mechanical and unambiguous; otherwise stop and ask the user.

## User Report

Respond in Chinese with:

- selected workspace root
- identified article ID
- whether `{Rev}/docs/procedure.md` was created, updated, or left unchanged
- any project adjustments applied
- verification result
- any question that blocked generation
