#!/usr/bin/env python3
"""Extract readable text from .docx, .pptx and .xlsx into Markdown.

Stdlib only, no pip installs. Cross-platform.

Usage: python extract-office-text.py <file> [--include-chrome]

  --include-chrome   also extract Word headers/footers and PowerPoint speaker notes

Exits 0 on success, 2 on a handled failure (message on stderr, machine-readable
prefix ERROR: so the caller logs it as "not processed" rather than skipping it).

Design note: tracked-change deletions and the "original" half of a move revision
are skipped deliberately. A regex-based extractor unwraps them into live text,
which resurrects deleted content and fabricates conflicts between documents that
do not actually disagree. That is worse than failing.
"""
import sys, os, re, zipfile, xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# Subtrees whose text must NOT appear in output: tracked deletions and the
# "original" half of a format/move revision.
SKIP = {W + "del", W + "moveFrom"}


def fail(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(2)


def note(msg):
    sys.stderr.write("NOTE: " + msg + "\n")


def natural_key(name):
    """Sort slide2.xml before slide10.xml."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


# --------------------------------------------------------------------------- #
# Word
# --------------------------------------------------------------------------- #

def run_text(el, rels, footnote_marks):
    """Text of an element in document order, honouring tabs, breaks, deletions."""
    out = []
    for child in el:
        tag = child.tag
        if tag in SKIP:
            continue
        if tag == W + "t":
            out.append(child.text or "")
        elif tag in (W + "tab",):
            out.append("\t")
        elif tag in (W + "br", W + "cr"):
            out.append("\n")
        elif tag == W + "noBreakHyphen":
            out.append("-")
        elif tag == W + "footnoteReference" or tag == W + "endnoteReference":
            fid = child.get(W + "id")
            if fid:
                footnote_marks.append(fid)
                out.append("[^%s]" % fid)
        elif tag == W + "hyperlink":
            inner = run_text(child, rels, footnote_marks)
            target = rels.get(child.get(R + "id"))
            out.append("[%s](%s)" % (inner, target) if target else inner)
        elif tag == W + "pPr":
            continue
        else:
            out.append(run_text(child, rels, footnote_marks))
    return "".join(out)


def para_md(p, rels, footnote_marks):
    text = run_text(p, rels, footnote_marks).strip()
    if not text:
        return ""
    ppr = p.find(W + "pPr")
    if ppr is not None:
        style = ppr.find(W + "pStyle")
        val = style.get(W + "val") if style is not None else ""
        if val:
            low = val.lower()
            if low.startswith("heading"):
                digits = "".join(c for c in low if c.isdigit())
                level = min(int(digits), 6) if digits else 1
                return "#" * level + " " + text
            if low in ("title",):
                return "# " + text
        if ppr.find(W + "numPr") is not None:
            return "- " + text
    return text


def rows_to_md(rows):
    """Shared by Word tables and PowerPoint tables."""
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    md = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    for r in rows[1:]:
        md.append("| " + " | ".join(r) + " |")
    return "\n".join(md)


def table_md(tbl, rels, footnote_marks):
    rows = []
    for tr in tbl.findall(W + "tr"):
        cells = []
        for tc in tr.findall(W + "tc"):
            parts = [run_text(p, rels, footnote_marks).strip()
                     for p in tc.iter(W + "p")]
            cells.append(" ".join(x for x in parts if x).replace("|", "\\|"))
        if cells:
            rows.append(cells)
    return rows_to_md(rows)


def block_md(parent, rels, footnote_marks):
    out = []
    for el in parent:
        if el.tag == W + "p":
            md = para_md(el, rels, footnote_marks)
            if md:
                out.append(md)
        elif el.tag == W + "tbl":
            md = table_md(el, rels, footnote_marks)
            if md:
                out.append(md)
        elif el.tag == W + "sdt":
            content = el.find(W + "sdtContent")
            if content is not None:
                out.extend(block_md(content, rels, footnote_marks))
    return out


def load_rels(z, part="word/_rels/document.xml.rels"):
    rels = {}
    try:
        root = ET.fromstring(z.read(part))
    except (KeyError, ET.ParseError):
        return rels
    for rel in root:
        if rel.get("TargetMode") == "External":
            rels[rel.get("Id")] = rel.get("Target")
    return rels


def load_notes(z, name, tag):
    notes = {}
    try:
        root = ET.fromstring(z.read(name))
    except (KeyError, ET.ParseError):
        return notes
    for n in root.findall(W + tag):
        nid = n.get(W + "id")
        text = " ".join(x for x in
                        (run_text(p, {}, []).strip() for p in n.iter(W + "p")) if x)
        if text:
            notes[nid] = text
    return notes


def extract_docx(z, names, path, include_chrome):
    try:
        root = ET.fromstring(z.read("word/document.xml"))
    except ET.ParseError as e:
        fail("document.xml is malformed (%s): %s" % (e, path))

    rels = load_rels(z)
    marks = []
    body = root.find(W + "body")
    blocks = block_md(body if body is not None else root, rels, marks)

    if marks:
        fn = load_notes(z, "word/footnotes.xml", "footnote")
        fn.update(load_notes(z, "word/endnotes.xml", "endnote"))
        defs = ["[^%s]: %s" % (m, fn[m]) for m in dict.fromkeys(marks) if m in fn]
        if defs:
            blocks.append("\n".join(defs))

    chrome = sorted(n for n in names
                    if n.startswith("word/header") or n.startswith("word/footer"))
    if chrome:
        if include_chrome:
            for n in chrome:
                try:
                    croot = ET.fromstring(z.read(n))
                except ET.ParseError:
                    continue
                text = block_md(croot, rels, [])
                if text:
                    blocks.append("<!-- %s -->\n%s" % (n, "\n\n".join(text)))
        else:
            note("%d header/footer part(s) not extracted; re-run with "
                 "--include-chrome if they carry content." % len(chrome))
    if "word/comments.xml" in names and not include_chrome:
        note("this file contains comments; they were not extracted.")
    return blocks


# --------------------------------------------------------------------------- #
# PowerPoint
# --------------------------------------------------------------------------- #

def shape_text(el):
    """Concatenate a:t runs within one a:p, honouring line breaks."""
    out = []
    for child in el:
        if child.tag == A + "t":
            out.append(child.text or "")
        elif child.tag == A + "br":
            out.append("\n")
        else:
            out.append(shape_text(child))
    return "".join(out)


def pptx_table_md(tbl):
    rows = []
    for tr in tbl.findall(A + "tr"):
        cells = []
        for tc in tr.findall(A + "tc"):
            parts = [shape_text(p).strip() for p in tc.iter(A + "p")]
            cells.append(" ".join(x for x in parts if x).replace("|", "\\|"))
        if cells:
            rows.append(cells)
    return rows_to_md(rows)


def extract_slide(z, name):
    """Return the markdown blocks for one slide, in document order."""
    try:
        root = ET.fromstring(z.read(name))
    except (KeyError, ET.ParseError):
        return []
    blocks, seen_tables = [], set()
    for tbl in root.iter(A + "tbl"):
        seen_tables.update(id(p) for p in tbl.iter(A + "p"))
    for el in root.iter():
        if el.tag == A + "tbl":
            md = pptx_table_md(el)
            if md:
                blocks.append(md)
        elif el.tag == A + "p" and id(el) not in seen_tables:
            text = shape_text(el).strip()
            if text:
                blocks.append(text)
    return blocks


def extract_pptx(z, names, path, include_chrome):
    slides = sorted((n for n in names
                     if n.startswith("ppt/slides/slide") and n.endswith(".xml")),
                    key=natural_key)
    if not slides:
        fail("no slides found in this .pptx: %s" % path)

    blocks = []
    for position, name in enumerate(slides, start=1):
        body = extract_slide(z, name)
        if not body:
            continue
        blocks.append("## Slide %d" % position)
        blocks.extend(body)
        if include_chrome:
            # The notes part is keyed to the slide's own file number, which is not
            # the same as its position once slides have been deleted or reordered.
            digits = "".join(c for c in os.path.basename(name) if c.isdigit())
            notes_name = "ppt/notesSlides/notesSlide%s.xml" % digits
            if digits and notes_name in names:
                # Drop the slide-number placeholder shape PowerPoint puts in notes.
                ntext = [b for b in extract_slide(z, notes_name)
                         if b.strip() not in (digits, str(position))]
                if ntext:
                    blocks.append("> Speaker notes: " + " ".join(ntext))

    have_notes = any(n.startswith("ppt/notesSlides/") for n in names)
    if have_notes and not include_chrome:
        note("this deck has speaker notes; they were not extracted. "
             "Re-run with --include-chrome to include them.")
    return blocks


# --------------------------------------------------------------------------- #
# Excel
# --------------------------------------------------------------------------- #

def col_index(ref):
    """'AB12' -> 27 (zero-based column). Returns None if unparseable."""
    letters = "".join(c for c in ref if c.isalpha()).upper()
    if not letters:
        return None
    n = 0
    for c in letters:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def load_shared_strings(z):
    strings = []
    try:
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    except (KeyError, ET.ParseError):
        return strings
    for si in root.findall(S + "si"):
        strings.append("".join(t.text or "" for t in si.iter(S + "t")))
    return strings


def sheet_names(z):
    """Map worksheet part name -> visible sheet name, in workbook order."""
    order = []
    try:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
    except (KeyError, ET.ParseError):
        return order
    rels = {}
    try:
        rroot = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        for rel in rroot:
            target = rel.get("Target", "")
            target = target[3:] if target.startswith("../") else target
            rels[rel.get("Id")] = target if target.startswith("xl/") else "xl/" + target
    except (KeyError, ET.ParseError):
        pass
    sheets = wb.find(S + "sheets")
    for sh in (sheets if sheets is not None else []):
        part = rels.get(sh.get(R + "id"))
        if part:
            order.append((part, sh.get("name") or part))
    return order


def extract_sheet(z, part, strings):
    try:
        root = ET.fromstring(z.read(part))
    except (KeyError, ET.ParseError):
        return []
    rows = []
    data = root.find(S + "sheetData")
    for row in (data if data is not None else []):
        cells = {}
        for c in row.findall(S + "c"):
            ctype = c.get("t")
            if ctype == "inlineStr":
                is_el = c.find(S + "is")
                val = "".join(t.text or "" for t in is_el.iter(S + "t")) if is_el is not None else ""
            else:
                v = c.find(S + "v")
                raw = v.text if v is not None and v.text is not None else ""
                if ctype == "s":
                    try:
                        val = strings[int(raw)]
                    except (ValueError, IndexError):
                        val = ""
                elif ctype == "b":
                    val = "TRUE" if raw == "1" else "FALSE"
                else:
                    val = raw
            idx = col_index(c.get("r") or "")
            if idx is None:
                idx = len(cells)
            if val != "":
                cells[idx] = val.replace("|", "\\|").replace("\n", " ")
        if cells:
            width = max(cells) + 1
            rows.append([cells.get(i, "") for i in range(width)])
    return rows


def extract_xlsx(z, names, path, include_chrome):
    strings = load_shared_strings(z)
    sheets = sheet_names(z)
    if not sheets:
        sheets = [(n, n.rsplit("/", 1)[-1])
                  for n in sorted((x for x in names
                                   if x.startswith("xl/worksheets/sheet")
                                   and x.endswith(".xml")), key=natural_key)]
    if not sheets:
        fail("no worksheets found in this .xlsx: %s" % path)

    blocks, empty = [], 0
    for part, name in sheets:
        rows = extract_sheet(z, part, strings)
        if not rows:
            empty += 1
            continue
        blocks.append("## Sheet: %s" % name)
        blocks.append(rows_to_md(rows))
    if empty:
        note("%d empty sheet(s) skipped." % empty)
    if not blocks:
        note("no cell values found; the workbook may hold only charts or pivot caches.")
    return blocks


# --------------------------------------------------------------------------- #

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    include_chrome = "--include-chrome" in sys.argv
    if len(args) != 1:
        fail("usage: extract-office-text.py <file.docx|.pptx|.xlsx> [--include-chrome]")
    path = os.path.abspath(os.path.expanduser(args[0]))
    if not os.path.isfile(path):
        fail("file not found: %s" % path)
    if os.path.getsize(path) == 0:
        fail("file is empty (0 bytes): %s" % path)
    if not zipfile.is_zipfile(path):
        fail("not a valid Office file (not a zip archive) - if this is a legacy "
             ".doc/.ppt/.xls, convert it to the modern format first: %s" % path)

    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        if "word/document.xml" in names:
            blocks = extract_docx(z, names, path, include_chrome)
        elif any(n.startswith("ppt/slides/") for n in names):
            blocks = extract_pptx(z, names, path, include_chrome)
        elif any(n.startswith("xl/") for n in names):
            blocks = extract_xlsx(z, names, path, include_chrome)
        else:
            fail("not a recognised Office format (no word/, ppt/ or xl/ parts): %s" % path)

    out = "\n\n".join(b for b in blocks if b)
    sys.stdout.buffer.write(out.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
