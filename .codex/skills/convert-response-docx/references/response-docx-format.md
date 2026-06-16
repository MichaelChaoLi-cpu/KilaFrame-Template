# Response DOCX Format

This reference records the user's personal response-to-reviewers DOCX style.

## Core Method

Use the bundled approved response DOCX as a package template unless the user explicitly provides another approved template. Copy the template DOCX package and replace only `word/document.xml`. This preserves styles, numbering definitions, page setup, margins, footer, settings, theme, and other Word package metadata.

Use `scripts/md_to_response_docx.py` for conversion when an approved template DOCX is available.

Default approved template:

```text
assets/response-template.docx
```

This bundled DOCX is an anonymized formatting template.

## Expected Paths

Default source:

```text
{Rev}/revision/response-draft.md
```

Default output:

```text
{Rev}/revision/response-draft.docx
```

If the user explicitly provides a newer approved response DOCX, use that template instead for the current conversion. Do not invent a final DOCX without an approved template.

## Page Setup

Preserve page setup from the template package. The established style uses:

- US Letter page size.
- 1 inch top and bottom margins.
- wider left and right margins.
- inherited footer and document settings.
- Times New Roman 12 pt body text through the template Normal style.
- spacious paragraph line spacing.

Do not rebuild these settings manually if the template is available.

## Style Mapping

Map Markdown to DOCX styles as follows:

| Markdown element | DOCX style / formatting |
| --- | --- |
| First `#` title | `Title` |
| `# Revision Summary` | `Heading1` |
| `# Editor` | page break before heading, then `Heading1` |
| `# Reviewer N` | page break before heading, then `Heading1` |
| `## Overall Comment` | `Heading2` |
| `## Comment N` | `Heading2` |
| Normal paragraphs | template Normal style |
| `**Response:**` | bold + italic `Response:` paragraph |
| `(Lines XX-XX; Pages XX)` paragraphs | bold + italic paragraph |
| Revision-summary bullet lines | template bullet/numbering style |
| Other bullet lines | template bullet/numbering style |

Major sections should begin on new pages. Insert a page break before `Editor` and before each `Reviewer` section.

## Content Rules

The Markdown file is the source of truth for content.

Preserve:

- Reviewer and editor comment text.
- Response text.
- Quoted article text.
- Reference entries.
- Line/page placeholders such as `(Lines XX-XX; Pages XX)`.

Do not rewrite reviewer comments during conversion.

The converter supports:

- `#` and `##` headings.
- Paragraphs.
- `- ` bullet lines.
- Inline `**bold**` text.
- A standalone `**Response:**` marker.
- Line/page citation paragraphs in the form `(Lines ...; Pages ...)`.

Do not build Word tables from Markdown tables for response files unless the user explicitly asks.

## Quality Checks

After conversion, verify at minimum:

1. The DOCX exists.
2. The DOCX ZIP package contains:
   - `[Content_Types].xml`
   - `word/document.xml`
   - `word/styles.xml`
   - `word/numbering.xml`
   - `word/settings.xml`
3. `word/document.xml` parses as valid XML.
4. The first paragraph uses `Title`.
5. `Revision Summary`, `Editor`, and each `Reviewer` heading use `Heading1`.
6. Overall and numbered comments use `Heading2`.
7. There is a page break before `Editor` and before each `Reviewer`.

If LibreOffice is available, render the DOCX to page images and visually inspect the output. If LibreOffice is not available, report structure-only validation.
