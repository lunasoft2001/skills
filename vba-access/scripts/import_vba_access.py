"""
import_vba_access.py — Import standard and class VBA modules from .bas / .cls files into an Access .accdb / .mdb file.

Usage:
    python import_vba_access.py <path_to_accdb> <input_dir>

⚠️  A timestamped backup of the .accdb is created automatically before any write.
    Import overwrites existing module code and cannot be undone without the backup.

Scope:
    Imports only standard modules (.bas) and class modules (.cls).
    Form and report code modules are NOT imported — use the access-analyzer skill for those.

Requirements:
    pip install pywin32
    Access must be installed.
    "Trust access to the VBA project object model" must be enabled in Access Trust Center.
"""

import sys
import os
import shutil
from datetime import datetime
import win32com.client

IMPORTABLE_EXTENSIONS = {".bas", ".cls"}

CLASS_HEADER_PREFIXES = ("VERSION 1.0 CLASS", "Attribute VB_")


def create_backup(accdb_path: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(accdb_path)
    backup_path = f"{base}_BACKUP_{ts}{ext}"
    shutil.copy2(accdb_path, backup_path)
    print(f"  Backup created: {backup_path}")
    return backup_path


def strip_cls_header(code: str) -> str:
    return "".join(
        line for line in code.splitlines(keepends=True)
        if not any(line.startswith(p) for p in CLASS_HEADER_PREFIXES)
    )


def import_vba(accdb_path: str, input_dir: str) -> None:
    accdb_path = os.path.abspath(accdb_path)
    input_dir = os.path.abspath(input_dir)

    if not os.path.exists(accdb_path):
        print(f"ERROR: File not found: {accdb_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(input_dir):
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Check for lock file
    lock_file = os.path.splitext(accdb_path)[0] + ".laccdb"
    if os.path.exists(lock_file):
        print(f"ERROR: Lock file detected ({lock_file}). Close Access before importing.", file=sys.stderr)
        sys.exit(1)

    bas_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f)[1].lower() in IMPORTABLE_EXTENSIONS
    ]
    if not bas_files:
        print("No .bas or .cls files found in the input directory. Nothing to import.")
        sys.exit(0)

    print(f"Importing VBA into: {accdb_path}")
    print(f"Source directory:   {input_dir}")
    print(f"Modules to import:  {len(bas_files)}\n")

    create_backup(accdb_path)
    print()

    access = win32com.client.Dispatch("Access.Application")
    access.Visible = False

    try:
        access.OpenCurrentDatabase(accdb_path)
        vbp = access.VBE.ActiveVBProject
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

        print(f"\nDone. {imported} modules imported, {errors} errors.")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            access.CloseCurrentDatabase()
        except Exception:
            pass
        access.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python import_vba_access.py <path_to_accdb> <input_dir>")
        sys.exit(1)
    import_vba(sys.argv[1], sys.argv[2])
