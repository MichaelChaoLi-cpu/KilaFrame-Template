---
name: convert-origin-docx
description: Convert the original manuscript DOCX in a revision workspace to readable Markdown. Use when Codex needs to convert {Rev}/origin/{article_id}.docx into {Rev}/origin/origin.md and extract images/assets into {Rev}/origin/originsrc/ without modifying the source DOCX or any markup DOCX files.
---

# Convert Origin DOCX

## Overview

Convert `{Rev}/origin/{article_id}.docx` into `{Rev}/origin/origin.md` and extract related image assets into `{Rev}/origin/originsrc/`. This skill creates a readable source manuscript for analysis and revision planning.

## Inputs

- Workspace root: default to `Rev` unless the user specifies another root such as `Rev1`.
- Article ID: identify from exactly one file matching `{Rev}/origin/*.docx`.
- Source DOCX: `{Rev}/origin/{article_id}.docx`.

Ignore temporary Word files such as names beginning with `~$`. If no source DOCX or multiple candidate DOCX files exist, ask the user in Chinese before converting.

## Outputs

```text
{Rev}/origin/origin.md
{Rev}/origin/originsrc/
```

## Rules

- Do not modify `{Rev}/origin/{article_id}.docx`.
- Do not read, modify, copy, or generate any markup docx for this task.
- Do not overwrite `{Rev}/origin/origin.md` or `{Rev}/origin/originsrc/` unless the user explicitly requests regeneration.
- Prefer a converter that preserves headings, paragraphs, tables as readable Markdown, references, figure captions, and image links.
- If image extraction is supported, write assets under `{Rev}/origin/originsrc/` and make `origin.md` references point there.
- If conversion tooling is unavailable, report the missing tool and stop instead of inventing manuscript content.

## Tool Preference

Use available local tooling in this order:

1. `pandoc` with media extraction when available.
2. Existing repo conversion scripts if the target repo provides them.
3. Python DOCX extraction libraries if already installed in the active environment.
4. A structure-only fallback only when the user accepts reduced fidelity.

Do not install dependencies unless the user asks or the current task clearly requires it and approval is obtained.

## Verification

After conversion, verify:

1. `{Rev}/origin/origin.md` exists and is non-empty.
2. The source DOCX remains unchanged.
3. If images were extracted, `{Rev}/origin/originsrc/` exists and contains the referenced assets.
4. Report the converter used and any fidelity limitations.

## User Report

Respond in Chinese with:

- source DOCX
- output Markdown
- asset directory
- converter used
- verification result
- any limitations or blocker
