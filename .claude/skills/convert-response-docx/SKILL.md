---
name: convert-response-docx
description: Convert a response-to-reviewers Markdown draft into a styled DOCX using the user's personal response formatting rules. Use when Codex needs to convert {Rev}/revision/response-draft.md to {Rev}/revision/response-draft.docx, preserve reviewer/comment text, apply the bundled response DOCX format law, and avoid modifying any markup DOCX files.
---

# Convert Response DOCX

## Overview

Convert `{Rev}/revision/response-draft.md` into `{Rev}/revision/response-draft.docx` using the personal response document style captured in `references/response-docx-format.md` and the bundled default template `assets/response-template.docx`.

## Required Reference

Read `references/response-docx-format.md` before converting.

## Inputs

- Workspace root: default to `Rev` unless the user specifies another root such as `Rev1`.
- Source Markdown: `{Rev}/revision/response-draft.md`.
- Formatting template DOCX: default to `assets/response-template.docx`; use a user-provided approved response DOCX template only when the user explicitly provides one.

If both the bundled template and user-provided template are missing, ask the user for the approved template path before generating final DOCX.

## Output

```text
{Rev}/revision/response-draft.docx
```

## Rules

- Do not modify `{Rev}/revision/response-draft.md` during conversion.
- Do not modify any markup DOCX.
- Preserve reviewer comments, editor comments, response text, article quotations, and line/page placeholders.
- Use `scripts/md_to_response_docx.py` when a template DOCX is available.
- If no template DOCX is available, do not invent final formatting. Report that conversion is blocked pending template.

## Conversion Command

When template is available:

```bash
python3 <skill-dir>/scripts/md_to_response_docx.py \
  {Rev}/revision/response-draft.md \
  <skill-dir>/assets/response-template.docx \
  {Rev}/revision/response-draft.docx
```

## Verification

After conversion, verify:

1. Output DOCX exists.
2. Output DOCX is a valid ZIP package.
3. `word/document.xml` parses as valid XML.
4. `word/styles.xml`, `word/numbering.xml`, and `word/settings.xml` exist.
5. Major headings map to expected DOCX styles according to `references/response-docx-format.md`.
6. If LibreOffice or another renderer is available, render and visually inspect. If not available, report structure-only validation.

## User Report

Respond in Chinese with:

- source Markdown
- output DOCX
- template used
- validation performed
- whether visual QA was performed
- any blocker or limitation
