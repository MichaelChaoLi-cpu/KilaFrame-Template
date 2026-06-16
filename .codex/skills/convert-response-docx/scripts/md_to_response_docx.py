#!/usr/bin/env python3
"""Convert a response-to-reviewers Markdown file to DOCX using a template DOCX.

The script avoids third-party packages. It copies the template DOCX package and
replaces only word/document.xml, preserving styles, numbering, settings, theme,
footer, margins, and other package-level formatting.
"""

from __future__ import annotations

import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XMLNS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("w", W)


def wtag(name: str) -> str:
    return f"{{{W}}}{name}"


def attrs(**kwargs: str) -> dict[str, str]:
    return {wtag(k): v for k, v in kwargs.items()}


def el(name: str, *children: ET.Element, **kwargs: str) -> ET.Element:
    node = ET.Element(wtag(name), attrs(**kwargs))
    node.extend(children)
    return node


def text_run(text: str, *, bold: bool = False, italic: bool = False) -> ET.Element:
    run = ET.Element(wtag("r"))
    if bold or italic:
        rpr = ET.SubElement(run, wtag("rPr"))
        if bold:
            ET.SubElement(rpr, wtag("b"))
            ET.SubElement(rpr, wtag("bCs"))
        if italic:
            ET.SubElement(rpr, wtag("i"))
            ET.SubElement(rpr, wtag("iCs"))
    t = ET.SubElement(run, wtag("t"))
    if text.startswith(" ") or text.endswith(" ") or "  " in text:
        t.set(f"{{{XMLNS}}}space", "preserve")
    t.text = text
    return run


def add_runs_for_inline_markup(p: ET.Element, text: str) -> None:
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            p.append(text_run(part[2:-2], bold=True))
        else:
            p.append(text_run(part))


def paragraph(
    text: str = "",
    style: str | None = None,
    *,
    page_break: bool = False,
    summary_bullet: bool = False,
    bold: bool = False,
    italic: bool = False,
) -> ET.Element:
    p = ET.Element(wtag("p"))
    ppr = ET.SubElement(p, wtag("pPr"))
    if style:
        ppr.append(el("pStyle", val=style))
    if summary_bullet:
        numpr = ET.SubElement(ppr, wtag("numPr"))
        numpr.append(el("ilvl", val="0"))
        numpr.append(el("numId", val="2"))
        ppr.append(el("jc", val="both"))
    if page_break:
        r = ET.SubElement(p, wtag("r"))
        r.append(el("br", type="page"))
        return p
    if text:
        if bold or italic:
            p.append(text_run(text, bold=bold, italic=italic))
        else:
            add_runs_for_inline_markup(p, text)
    return p


def get_template_sectpr(template_docx: Path) -> ET.Element:
    with ZipFile(template_docx) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    sect = root.find(f".//{wtag('sectPr')}")
    if sect is None:
        raise RuntimeError("Template DOCX does not contain sectPr")
    return sect


def normalize_heading(text: str) -> str:
    return text.strip().lstrip("#").strip()


def build_body(markdown: str, sectpr: ET.Element) -> ET.Element:
    body = ET.Element(wtag("body"))
    lines = markdown.splitlines()
    in_revision_summary = False
    after_summary = False
    previous_blank = False
    first_paragraph = True

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            if not previous_blank:
                body.append(paragraph(""))
            previous_blank = True
            continue
        previous_blank = False

        if stripped.startswith("# "):
            title = normalize_heading(stripped)
            if first_paragraph:
                body.append(paragraph(title, "Title"))
            else:
                if title == "Editor" or title.startswith("Reviewer "):
                    body.append(paragraph(page_break=True))
                    after_summary = True
                body.append(paragraph(title, "Heading1"))
            in_revision_summary = title == "Revision Summary"
            first_paragraph = False
            continue

        if stripped.startswith("## "):
            body.append(paragraph(normalize_heading(stripped), "Heading2"))
            continue

        if stripped.startswith("- "):
            text = stripped[2:].strip()
            body.append(paragraph(text, "p1", summary_bullet=True))
            continue

        if stripped == "**Response:**":
            body.append(paragraph("Response:", bold=True, italic=True))
            continue

        if re.fullmatch(r"\(Lines .+; Pages? .+\)", stripped):
            body.append(paragraph(stripped, bold=True, italic=True))
            continue

        body.append(paragraph(html.unescape(stripped)))

    body.append(sectpr)
    return body


def make_document_xml(body: ET.Element) -> bytes:
    document = ET.Element(wtag("document"))
    document.append(body)
    return ET.tostring(document, encoding="utf-8", xml_declaration=True)


def write_docx(template_docx: Path, output_docx: Path, document_xml: bytes) -> None:
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(template_docx, "r") as zin, ZipFile(output_docx, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = document_xml
            zout.writestr(item, data)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("Usage: md_to_response_docx.py INPUT.md TEMPLATE.docx OUTPUT.docx", file=sys.stderr)
        return 2
    source_md = Path(argv[1])
    template_docx = Path(argv[2])
    output_docx = Path(argv[3])
    markdown = source_md.read_text(encoding="utf-8")
    sectpr = get_template_sectpr(template_docx)
    body = build_body(markdown, sectpr)
    document_xml = make_document_xml(body)
    write_docx(template_docx, output_docx, document_xml)
    print(output_docx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
