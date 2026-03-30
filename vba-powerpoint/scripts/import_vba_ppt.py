"""
import_vba_ppt.py — Import VBA modules from .bas / .cls files into a PowerPoint .pptm / .potm file.

Usage:
    python import_vba_ppt.py <path_to_pptm> <input_dir>

⚠️  A timestamped backup of the .pptm is created automatically before any write.
    Import overwrites existing module code and cannot be undone without the backup.

Requirements:
    pip install pywin32
    PowerPoint must be installed.
    "Trust access to the VBA project object model" must be enabled in PowerPoint Trust Center.
"""

import sys
import os
import shutil
from datetime import datetime
import win32com.client

IMPORTABLE_EXTENSIONS = {".bas", ".cls"}

CLASS_HEADER_PREFIXES = ("VERSION 1.0 CLASS", "Attribute VB_")


def create_backup(pptm_path: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(pptm_path)
    backup_path = f"{base}_BACKUP_{ts}{ext}"
    shutil.copy2(pptm_path, backup_path)
    print(f"  Backup created: {backup_path}")
    return backup_path


def strip_cls_header(code: str) -> str:
    lines = code.splitlines(keepends=True)
    return "".join(
        line for line in lines
        if not any(line.startswith(p) for p in CLASS_HEADER_PREFIXES)
    )


def import_vba(pptm_path: str, input_dir: str) -> None:
    pptm_path = os.path.abspath(pptm_path)
    input_dir = os.path.abspath(input_dir)

    if not os.path.exists(pptm_path):
        print(f"ERROR: File not found: {pptm_path}", file=sys.stderr)
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

    print(f"Importing VBA into: {pptm_path}")
    print(f"Source directory:   {input_dir}")
    print(f"Modules to import:  {len(bas_files)}\n")

    create_backup(pptm_path)
    print()

    # PowerPoint COM requires Visible = True to avoid hangs during automation.
    # Unlike Word/Access (which work headless), PowerPoint may briefly show a window.
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = True
    pres = None

    try:
        pres = ppt.Presentations.Open(pptm_path, WithWindow=False)
        vbp = pres.VBProject
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
                    code = strip_cls_header(raw_code) if ext == ".cls" else raw_code
                    cm = comp.CodeModule
                    if cm.CountOfLines > 0:
                        cm.DeleteLines(1, cm.CountOfLines)
                    cm.AddFromString(code)
                else:
                    comp = vbp.VBComponents.Add(1)  # vbext_ct_StdModule
                    comp.Name = module_name
                    comp.CodeModule.AddFromString(raw_code)

                print(f"  Imported: {filename}")
                imported += 1

            except Exception as e:
                print(f"  ERROR importing {filename}: {e}")
                errors += 1

        pres.Save()
        pres.Save()
        print(f"\nDone. {imported} modules imported, {errors} errors.")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if pres is not None:
            pres.Close()
        ppt.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python import_vba_ppt.py <path_to_pptm> <input_dir>")
        sys.exit(1)
    import_vba(sys.argv[1], sys.argv[2])
