"""
export_vba_access.py — Export standard and class VBA modules from an Access .accdb / .mdb file.

Usage:
    python export_vba_access.py <path_to_accdb> [output_dir]

Scope:
    Exports only standard modules (.bas) and class modules (.cls).
    Form and report code modules are NOT exported — use the access-analyzer skill for those.

Requirements:
    pip install pywin32
    Access must be installed.
    "Trust access to the VBA project object model" must be enabled in Access Trust Center.
"""

import sys
import os
import win32com.client

# Only export standard and class modules (types 1 and 2)
EXPORTABLE_TYPES = {
    1: ".bas",   # vbext_ct_StdModule
    2: ".cls",   # vbext_ct_ClassModule
}


def export_vba(accdb_path: str, output_dir: str) -> None:
    accdb_path = os.path.abspath(accdb_path)
    output_dir = os.path.abspath(output_dir)

    if not os.path.exists(accdb_path):
        print(f"ERROR: File not found: {accdb_path}", file=sys.stderr)
        sys.exit(1)

    # Check for lock file
    lock_file = os.path.splitext(accdb_path)[0] + ".laccdb"
    if os.path.exists(lock_file):
        print(f"WARNING: Lock file detected ({lock_file}). Ensure Access is closed before exporting.")

    os.makedirs(output_dir, exist_ok=True)
    print(f"Exporting VBA from: {accdb_path}")
    print(f"Output directory:   {output_dir}\n")

    access = win32com.client.Dispatch("Access.Application")
    access.Visible = False

    try:
        access.OpenCurrentDatabase(accdb_path)
        vbp = access.VBE.ActiveVBProject
        exported = 0
        skipped = 0

        for comp in vbp.VBComponents:
            ext = EXPORTABLE_TYPES.get(comp.Type)
            if ext is None:
                print(f"  Skipped (type {comp.Type} = form/report/document): {comp.Name}")
                skipped += 1
                continue

            line_count = comp.CodeModule.CountOfLines
            code = comp.CodeModule.Lines(1, line_count) if line_count > 0 else ""

            filename = comp.Name + ext
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"  Exported: {filename} ({line_count} lines)")
            exported += 1

        print(f"\nDone. {exported} modules exported, {skipped} skipped (form/report/document modules).")
        print(f"Output: {output_dir}")

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
    if len(sys.argv) < 2:
        print("Usage: python export_vba_access.py <path_to_accdb> [output_dir]")
        sys.exit(1)

    accdb = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.abspath(accdb))[0] + "_vba"
    export_vba(accdb, out)
