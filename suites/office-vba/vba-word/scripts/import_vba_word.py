"""
import_vba_word.py — Import VBA modules from .bas / .cls files into a Word .docm / .dotm file.

Usage:
    python import_vba_word.py <path_to_docm> <input_dir>

⚠️  A timestamped backup of the .docm is created automatically before any write.
    Import overwrites existing module code and cannot be undone without the backup.

Requirements:
    pip install pywin32
    Word must be installed.
    "Trust access to the VBA project object model" must be enabled in Word Trust Center.
"""

import sys
import os
import shutil
from datetime import datetime
import win32com.client

IMPORTABLE_EXTENSIONS = {".bas", ".cls"}

# VBA class/document module headers that must not be duplicated when replacing code
CLASS_HEADER_PREFIXES = ("VERSION 1.0 CLASS", "Attribute VB_")


def create_backup(docm_path: str) -> str:
    """Create a timestamped backup of the .docm file before importing."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(docm_path)
    backup_path = f"{base}_BACKUP_{ts}{ext}"
    shutil.copy2(docm_path, backup_path)
    print(f"  Backup created: {backup_path}")
    return backup_path


def strip_cls_header(code: str) -> str:
    """Remove class module header lines (VERSION / Attribute) that Word manages internally."""
    lines = code.splitlines(keepends=True)
    body_lines = []
    for line in lines:
        if any(line.startswith(prefix) for prefix in CLASS_HEADER_PREFIXES):
            continue
        body_lines.append(line)
    return "".join(body_lines)


def import_vba(docm_path: str, input_dir: str) -> None:
    docm_path = os.path.abspath(docm_path)
    input_dir = os.path.abspath(input_dir)

    if not os.path.exists(docm_path):
        print(f"ERROR: File not found: {docm_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(input_dir):
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    bas_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f)[1].lower() in IMPORTABLE_EXTENSIONS
    ]
    if not bas_files:
        print("No .bas or .cls files found in the input directory. Nothing to import.")
        sys.exit(0)

    print(f"Importing VBA into: {docm_path}")
    print(f"Source directory:   {input_dir}")
    print(f"Modules to import:  {len(bas_files)}\n")

    # Backup before any write
    create_backup(docm_path)
    print()

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = None

    try:
        doc = word.Documents.Open(docm_path)
        vbp = doc.VBProject

        # Build a lookup of existing components by name
        existing = {c.Name: c for c in vbp.VBComponents}

        imported = 0
        errors = 0

        for filename in sorted(bas_files):
            module_name = os.path.splitext(filename)[0]
            ext = os.path.splitext(filename)[1].lower()
            filepath = os.path.join(input_dir, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                raw_code = f.read()

            try:
                if module_name in existing:
                    comp = existing[module_name]
                    # For class/document modules, strip the header before replacing
                    code = strip_cls_header(raw_code) if ext == ".cls" else raw_code
                    cm = comp.CodeModule
                    if cm.CountOfLines > 0:
                        cm.DeleteLines(1, cm.CountOfLines)
                    cm.AddFromString(code)
                else:
                    # Add a new standard module
                    comp = vbp.VBComponents.Add(1)  # vbext_ct_StdModule
                    comp.Name = module_name
                    comp.CodeModule.AddFromString(raw_code)

                print(f"  Imported: {filename}")
                imported += 1

            except Exception as e:
                print(f"  ERROR importing {filename}: {e}")
                errors += 1

        doc.Save()
        print(f"\nDone. {imported} modules imported, {errors} errors.")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if doc is not None:
            doc.Close(True)
        word.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python import_vba_word.py <path_to_docm> <input_dir>")
        sys.exit(1)
    import_vba(sys.argv[1], sys.argv[2])
