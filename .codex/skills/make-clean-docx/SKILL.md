---
name: make-clean-docx
description: Create a clean DOCX from a revision markup DOCX without modifying the markup file. Use when Codex needs to copy {Rev}/revision/{article_id}.rev.markup.docx to {Rev}/revision/{article_id}.rev.clean.docx and accept tracked changes only in the clean copy while preserving the hard rule that markup DOCX files are never changed.
---

# Make Clean DOCX

## Overview

Generate `{Rev}/revision/{article_id}.rev.clean.docx` from `{Rev}/revision/{article_id}.rev.markup.docx`. The markup document is read-only and must remain untouched.

## Inputs

- Workspace root: default to `Rev` unless the user specifies another root such as `Rev1`.
- Article ID: identify from `{Rev}/origin/{article_id}.docx` or from exactly one matching markup file if needed.
- Source markup DOCX: `{Rev}/revision/{article_id}.rev.markup.docx`.

If article ID or markup source is ambiguous, ask the user in Chinese before acting.

## Output

```text
{Rev}/revision/{article_id}.rev.clean.docx
```

## Hard Boundaries

- Never modify, overwrite, move, rename, delete, or accept changes in `{Rev}/revision/{article_id}.rev.markup.docx`.
- Work only on a copied clean output file.
- If accepting revisions cannot be performed safely on the copy, stop and report the blocker.
- Do not use the clean output as evidence that markup was changed; explicitly verify the source markup file remains present and untouched.

## Procedure

1. Locate the markup DOCX.
2. Record basic source metadata before work, such as path, size, and modified time when available.
3. Copy markup DOCX to the clean output path.
4. Accept all tracked revisions in the clean output only.
5. Preserve comments only if the accepted-clean workflow naturally preserves them; report whether comments were preserved or removed if known.
6. Verify source metadata did not change.

## Tool Preference

Use available local tooling in this order:

1. Microsoft Word automation only if available and approved for GUI/automation use.
2. LibreOffice or another office converter if it can accept tracked changes in the copy reliably.
3. A dedicated DOCX/OOXML script only if it is known to accept tracked revisions correctly for this document type.

Do not claim tracked changes were accepted unless the tool actually performed that operation. A simple file copy is not a clean document.

## Verification

After generation, verify:

1. Clean DOCX exists at `{Rev}/revision/{article_id}.rev.clean.docx`.
2. Markup DOCX still exists at its original path.
3. Markup DOCX size and modified time are unchanged when this metadata is available.
4. The method used to accept revisions is reported.
5. If visual or tracked-change verification is unavailable, say so explicitly.

## User Report

Respond in Chinese with:

- source markup DOCX
- output clean DOCX
- tool/method used
- verification that markup was untouched
- any limitations or blocker
