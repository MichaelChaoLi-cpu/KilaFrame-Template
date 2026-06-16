---
name: build-revision-plan
description: Build or update the manuscript revision plan at {Rev}/docs/revisionplan.md. Use when Codex needs to turn structured reviewer comments into an ordered action plan, assign priorities and human/agent responsibilities, choose the next unfinished comment, or update plan status after human confirmation while preserving the rule that markup docx files are never modified.
---

# Build Revision Plan

## Overview

Create or update `{Rev}/docs/revisionplan.md` from structured reviewer comments and current project context. This skill owns the revision plan artifact; `execute-procedure` should dispatch to this skill instead of building the plan directly.

The plan is an agent draft and maintenance document. Human review and final strategy confirmation remain required for research decisions.

## Inputs

- Workspace root: default to `Rev` unless the user specifies another root such as `Rev1`.
- Structured comments: `{Rev}/docs/structuredcomments.md`.
- Editor message: `{Rev}/origin/editormessage.md`.
- Converted manuscript, when available: `{Rev}/origin/origin.md`.
- Existing plan, when updating: `{Rev}/docs/revisionplan.md`.
- Optional repo context outside `{Rev}/`: code, data, scripts, outputs, figures, supplements, or other materials needed to judge feasibility.

If `{Rev}` is ambiguous, ask the user in Chinese before editing files.

## Hard Boundaries

- Never create, edit, rename, overwrite, accept changes in, move, or delete any markup DOCX.
- Do not perform manuscript text replacement.
- Do not mark a comment complete unless the human has confirmed the manuscript change and response are acceptable.
- Do not invent reviewer comments or rewrite reviewer text.
- Do not use memory as evidence for current files; inspect live files.

## When Creating A New Plan

Before writing `{Rev}/docs/revisionplan.md`:

1. Read `{Rev}/docs/structuredcomments.md`.
2. Read `{Rev}/origin/editormessage.md` if it exists.
3. Read `{Rev}/origin/origin.md` if it exists and is useful for section mapping.
4. Inspect repo files outside `{Rev}/` only when needed to evaluate whether a comment requires code, data, analysis, figures, or supplements.
5. Preserve all comment identifiers from `structuredcomments.md`.

If `revisionplan.md` already exists, do not overwrite it unless the user explicitly asks to regenerate it. Prefer an update that preserves existing status and human notes.

## Plan Format

Use a Markdown table unless the procedure asks for another format.

Required columns:

- reviewer id
- comment id
- 修改序号
- 问题简述
- 风险等级
- 影响的章节
- 修改计划
- 负责人
- 依赖
- 是否搞定

Allowed status values for `是否搞定`:

- `pending`
- `in_progress`
- `human_edit_required`
- `response_draft_required`
- `human_review_required`
- `done`
- `blocked`

Use `负责人` values such as `human`, `agent`, or `human+agent`.

## Sorting Rules

Assign `修改序号` by practical execution order:

1. Independent comments before coupled comments.
2. Text-only/local comments before comments requiring new analysis or computation.
3. Local section edits before global restructuring.
4. High-risk or decision-changing comments should be visible early, but not marked executable until the human confirms strategy.
5. Overall comments usually go last because detailed edits make the overall response easier to finalize.

When procedure-specific sorting rules exist in `{Rev}/docs/procedure.md`, follow them.

## Updating An Existing Plan

Use this skill to:

- add missing comments after `structuredcomments.md` changes
- preserve existing human notes and statuses
- update `是否搞定` after human confirmation
- set `blocked` with a concrete blocker
- choose the next unfinished item by `修改序号`
- revise priority/order when dependencies change

Do not silently discard rows. If a row appears obsolete, report it and ask before deleting.

## Verification

After creating or updating the plan:

1. Confirm every structured comment appears in the plan.
2. Confirm no extra reviewer comment is invented.
3. Confirm required columns are present.
4. Confirm existing `done` statuses and human notes were preserved unless explicitly changed.
5. Report whether any comments require human strategy confirmation.

## User Report

Respond in Chinese with:

- whether the plan was created, updated, regenerated, or only inspected
- file path of the plan
- count of planned comments
- any blockers or comments needing human strategy confirmation
- next recommended action
