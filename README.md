# KilaFrame Template

Primary language: English. Chinese companion: [README.zh-CN.md](README.zh-CN.md).

Version: `v0.0.0`

KilaFrame Template is a Codex skill bundle for manuscript revision workflows. It is designed to be copied into a separate research repository, where Codex can initialize a revision workspace, build a procedure file, execute the procedure, keep logs, and dispatch document-conversion subskills.

This repository is not meant to hold a specific manuscript. It holds reusable workflow skills.

## Core Rules

- The target research repository owns the manuscript files and revision outputs.
- The default revision workspace is `Rev/`, but the user may choose another name such as `Rev1/`.
- Codex may read `markup.docx`, but must never edit, overwrite, move, delete, or accept revisions in the markup file.
- Text replacement in the manuscript body must be performed by a human in Word.
- Codex may generate a clean DOCX from the markup DOCX, but only as a separate clean output file.
- Per-comment response text is output for the human to copy by default. Codex may write it into `{Rev}/revision/response-draft.md` only when the human explicitly authorizes that write in the current request.
- `{Rev}/origin/rawcomments.md` and `{Rev}/origin/editormessage.md` are created only when missing. Existing files must not be overwritten.

## Skills

This bundle contains seven skills:

| Skill | Role |
| --- | --- |
| `init-revision-workspace` | Create `{Rev}/origin/`, `{Rev}/revision/`, `{Rev}/docs/`, create empty human-input files only when missing, and update `.gitignore`. |
| `build-procedure` | Generate `{Rev}/docs/procedure.md` from a fixed template with small project-specific edits. |
| `execute-procedure` | Read the procedure, check current state, log progress, run machine steps, or prompt the human for the next human step. |
| `convert-origin-docx` | Convert `{Rev}/origin/{article_id}.docx` into `{Rev}/origin/origin.md` and `{Rev}/origin/originsrc/`. |
| `make-clean-docx` | Copy `{Rev}/revision/{article_id}.rev.markup.docx` to `{Rev}/revision/{article_id}.rev.clean.docx` and accept revisions only in the clean copy. |
| `convert-response-docx` | Convert `{Rev}/revision/response-draft.md` to `{Rev}/revision/response-draft.docx` using the bundled response DOCX style. |
| `build-response-draft` | Build the initial response draft or per-comment response text from structured comments, editor messages, and the bundled response template. |

## Install Skills Into a Research Repo

Do not clone this repository inside the target research repo. Use a temporary sparse checkout, then copy only `.codex/skills/`.

```bash
git clone --filter=blob:none --sparse https://github.com/<owner>/<repo>.git /tmp/kilaframe-template
cd /tmp/kilaframe-template
git sparse-checkout set .codex/skills

mkdir -p /path/to/research-repo/.codex
cp -R .codex/skills /path/to/research-repo/.codex/
```

Replace `https://github.com/<owner>/<repo>.git` with the GitHub URL of this template repository, and replace `/path/to/research-repo` with the target research repository.

`curl -O` is not the recommended default because GitHub does not expose a whole directory as a single raw file. It is suitable for one file, not for reliably installing this skill directory.

## Target Workspace Layout

After initialization, the target research repo uses this structure. `{Rev}` is the chosen revision workspace name.

```text
{Rev}/
  origin/
    {article_id}.docx
    rawcomments.md
    editormessage.md
    origin.md
    originsrc/
  revision/
    {article_id}.rev.markup.docx
    {article_id}.rev.clean.docx
    response-draft.md
    response-draft.docx
  docs/
    procedure.md
    structuredcomments.md
    revisionplan.md
    procedure-execution.log
```

`{article_id}` is identified from `{Rev}/origin/{article_id}.docx`.

The `origin/` directory is the input area, `revision/` is the output and revision area, and `docs/` is the procedure, plan, and log area.

## Recommended `.gitignore`

`init-revision-workspace` is responsible for updating `.gitignore` in the target research repo. For the default `Rev/` workspace, the intended rules are:

```gitignore
.codex/skills/

Rev/*
!Rev/revision/
Rev/revision/*
!Rev/revision/response-draft.md
```

If the workspace is named `Rev1/`, replace `Rev/` with `Rev1/`.

## Typical Workflow

1. Copy the skills into the target research repo.
2. Ask Codex to run `$init-revision-workspace`. Use `Rev/` by default, or specify another workspace name.
3. Human places `{article_id}.docx`, `rawcomments.md`, and `editormessage.md` in `{Rev}/origin/`.
4. Ask Codex to run `$build-procedure` to create `{Rev}/docs/procedure.md`.
5. Ask Codex to run `$execute-procedure`.
6. Codex checks the current state, writes `{Rev}/docs/procedure-execution.log`, and either runs the next machine step or prompts the human.
7. Human performs manuscript body edits in the markup DOCX.
8. Codex may generate clean DOCX, draft response text, update plans, and convert the response draft to DOCX according to the procedure.

## Development Notes

The design source is [idea/overall.md](idea/overall.md).

The bundled response DOCX template has been sanitized and is stored at `.codex/skills/convert-response-docx/assets/response-template.docx`.
