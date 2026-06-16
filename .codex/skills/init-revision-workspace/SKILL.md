---
name: init-revision-workspace
description: Initialize a manuscript revision workspace in a target research repo. Use when Codex needs to create the default Rev/ workspace or a user-named revision workspace such as Rev1/, create origin/, revision/, and docs/, create empty origin/rawcomments.md and origin/editormessage.md input files, and update the target repo .gitignore so injected .codex/skills/, .claude/skills/, and revision artifacts stay untracked except {Rev}/revision/response-draft.md.
---

# Init Revision Workspace

## Overview

Initialize the revision workspace described in `idea/overall.md`. Create the directory skeleton, two empty human-input Markdown files, and `.gitignore` rules; do not populate manuscript, procedure, log, response, or Word files.

## Inputs

- Workspace root name: default to `Rev` when the user does not specify a name.
- User may specify another root name, such as `Rev1`.
- Treat the selected root as `{Rev}` in this skill.

If the user asks for a location outside the current repo or gives multiple possible names, ask for clarification in Chinese before editing files.

## Preconditions

1. Confirm the current working directory is the target research repo root or identify the target repo root from the user's request.
2. Confirm there is no existing file at `{Rev}`. If `{Rev}` exists as a file, stop and ask the user how to proceed.
3. If `{Rev}` exists as a directory, do not delete or overwrite it. Add only missing required subdirectories and update `.gitignore`.
4. Do not run `git clone`; skill installation or update is handled by README commands outside this skill.

## Create Directories

Create this structure:

```text
{Rev}/
  origin/
    rawcomments.md
    editormessage.md
  revision/
  docs/
```

Rules:

- Do not create placeholder files such as `.gitkeep`.
- Create `{Rev}/origin/rawcomments.md` and `{Rev}/origin/editormessage.md` as empty files when missing.
- If either file already exists, do not write to it or overwrite it. Remind the human to inspect the existing file before continuing.
- Do not create `procedure.md`, `revisionplan.md`, `procedure-execution.log`, `response-draft.md`, `response-draft.docx`, `clean.docx`, `markup.docx`, or any manuscript content.
- Do not create optional `etc/` unless the user explicitly asks for it.

Directory meanings:

- `{Rev}/origin/`: human-provided inputs such as `{article_id}.docx`, raw reviewer comments, editor message, generated `origin.md`, and generated `originsrc/`.
- `{Rev}/revision/`: revision outputs and working files, including `markup.docx`, clean docx, `response-draft.md`, and `response-draft.docx`.
- `{Rev}/docs/`: agent-managed procedure, revision plan, logs, checks, and process records.

## Update `.gitignore`

Create `.gitignore` if it does not exist. Preserve all existing rules.

Add or update a single managed block:

```gitignore
# BEGIN manuscript revision workspace
.codex/skills/
.claude/skills/
{Rev}/*
!{Rev}/revision/
{Rev}/revision/*
!{Rev}/revision/response-draft.md
# END manuscript revision workspace
```

Replace `{Rev}` with the actual workspace root, for example:

```gitignore
# BEGIN manuscript revision workspace
.codex/skills/
.claude/skills/
Rev/*
!Rev/revision/
Rev/revision/*
!Rev/revision/response-draft.md
# END manuscript revision workspace
```

Rules:

- If the managed block already exists, update it in place instead of appending a duplicate block.
- If related rules exist outside the managed block, do not delete them. Report possible overlap to the user.
- The intended git behavior is: injected skills are ignored; all revision workspace contents are ignored except `{Rev}/revision/response-draft.md`.

## Verification

After editing, verify:

1. `{Rev}/origin/`, `{Rev}/revision/`, and `{Rev}/docs/` exist and are directories.
2. `{Rev}/origin/rawcomments.md` and `{Rev}/origin/editormessage.md` exist as files.
3. `.gitignore` contains exactly one managed block.
4. The managed block contains the selected `{Rev}` name.
5. No files were created inside `{Rev}/` except the two empty origin Markdown files.
6. Any pre-existing `rawcomments.md` or `editormessage.md` was left unchanged and reported to the human.

If a verification check fails, fix it if safe; otherwise report the blocker and stop.

## User Report

Respond in Chinese with:

- selected workspace root
- directories created or already present
- whether `rawcomments.md` and `editormessage.md` were newly created or already existed, with a reminder to inspect existing files
- whether `.gitignore` was created, appended, or updated
- the rule that only `{Rev}/revision/response-draft.md` is intentionally open to git
- any overlap or blocker found
