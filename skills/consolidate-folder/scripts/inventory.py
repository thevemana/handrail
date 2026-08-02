#!/usr/bin/env python3
"""Pre-flight inventory for consolidate-folder. Stdlib only.

Usage: python inventory.py <folder> [--all]

Prints a manifest (one row per file) plus a SCOPE verdict. The manifest is the
contract: every PROCESS row must appear in the final document's Source Index,
and every SKIP/FAIL row must appear in Gaps or Conflicts.
"""
import sys, os, hashlib

TEXTY = {".md", ".markdown", ".txt", ".rst", ".org", ".csv", ".tsv", ".json",
         ".yaml", ".yml", ".html", ".htm", ".rtf", ".log", ".tex"}
EXTRACT = {".docx", ".pptx", ".xlsx", ".pdf"}
# Legacy binary Office formats (.doc/.ppt/.xls) are NOT here: they are not zips
# and cannot be read without a converter. They stay note-only on purpose.
NOTE_ONLY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".heic", ".bmp",
             ".tif", ".tiff", ".mp4", ".mov", ".mp3", ".wav", ".zip", ".exe",
             ".dll", ".xls", ".ppt", ".doc", ".key", ".numbers",
             ".pages", ".sqlite", ".db", ".bin", ".ico", ".woff", ".woff2"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".obsidian",
             ".idea", ".vscode", "dist", "build", ".next", "target", ".cache",
             ".DS_Store", "site-packages", ".terraform"}

MAX_FILES = 40
MAX_TOTAL_BYTES = 2_000_000       # ~500k tokens of text, well past comfort
MAX_SINGLE_BYTES = 400_000


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: inventory.py <folder> [--all]\n")
        sys.exit(2)
    root = os.path.abspath(os.path.expanduser(sys.argv[1]))
    if not os.path.isdir(root):
        sys.stderr.write("ERROR: not a folder: %s\n" % root)
        sys.exit(2)
    show_all = "--all" in sys.argv

    rows, skipped_dirs = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        pruned = [d for d in dirnames if d in SKIP_DIRS or d.startswith(".")]
        for d in pruned:
            skipped_dirs.append(os.path.relpath(os.path.join(dirpath, d), root))
        if not show_all:
            dirnames[:] = [d for d in dirnames if d not in pruned]
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            ext = os.path.splitext(fn)[1].lower()
            try:
                size = os.path.getsize(full)
                with open(full, "rb") as fh:
                    digest = hashlib.sha256(fh.read()).hexdigest()[:12]
            except OSError as e:
                rows.append((rel, 0, "", "FAIL", "unreadable: %s" % e.strerror))
                continue
            if ext in NOTE_ONLY:
                action, why = "NOTE-ONLY", "non-text asset: reference, do not merge"
            elif ext in EXTRACT:
                action, why = "EXTRACT", "needs extraction before reading"
            elif ext in TEXTY or ext == "":
                action, why = "PROCESS", ""
            else:
                action, why = "REVIEW", "unrecognised extension: confirm before reading"
            if size == 0:
                action, why = "FAIL", "empty file (0 bytes)"
            elif size > MAX_SINGLE_BYTES and action == "PROCESS":
                action, why = "REVIEW", "large file (%.0f KB): read in parts" % (size / 1024)
            rows.append((rel, size, digest, action, why))

    dupes = {}
    for rel, size, digest, action, why in rows:
        if digest:
            dupes.setdefault(digest, []).append(rel)

    print("PATH\tBYTES\tSHA256-12\tACTION\tNOTE")
    for rel, size, digest, action, why in rows:
        print("%s\t%d\t%s\t%s\t%s" % (rel, size, digest or "-", action, why))

    readable = [r for r in rows if r[3] in ("PROCESS", "EXTRACT")]
    total = sum(r[1] for r in readable)
    print("\n--- SUMMARY ---")
    print("files found:        %d" % len(rows))
    print("to read:            %d  (%.0f KB)" % (len(readable), total / 1024))
    print("note-only assets:   %d" % sum(1 for r in rows if r[3] == "NOTE-ONLY"))
    print("needs review:       %d" % sum(1 for r in rows if r[3] == "REVIEW"))
    print("failed/empty:       %d" % sum(1 for r in rows if r[3] == "FAIL"))
    for digest, paths in dupes.items():
        if len(paths) > 1:
            print("identical content:  %s" % " == ".join(paths))
    if skipped_dirs:
        print("pruned dirs:        %s" % ", ".join(sorted(set(skipped_dirs))[:10]))

    over = []
    if len(readable) > MAX_FILES:
        over.append("%d files exceeds the %d-file single-pass limit" % (len(readable), MAX_FILES))
    if total > MAX_TOTAL_BYTES:
        over.append("%.0f KB exceeds the %.0f KB single-pass limit" % (total / 1024, MAX_TOTAL_BYTES / 1024))
    if over:
        print("\nSCOPE: STOP - " + "; ".join(over))
        print("Do not start reading. Report this to the user and agree a narrower")
        print("scope or a batched plan with a per-batch partial document first.")
        sys.exit(3)
    print("\nSCOPE: OK - safe to read in one pass.")


if __name__ == "__main__":
    main()
