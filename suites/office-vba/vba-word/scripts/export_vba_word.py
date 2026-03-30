"""
export_vba_word.py — Export all VBA modules from a Word .docm / .dotm file.

Usage:
    python export_vba_word.py <path_to_docm> [output_dir]

Requirements:
    pip install pywin32
    Word must be installed.
    "Trust access to the VBA project object model" must be enabled in Word Trust Center.
"""

import sys
import os
import win32com.client

# Maps VBA component types to file extensions
VBA_EXTENSIONS = {
    1: ".bas",    # vbext_ct_StdModule  — standard module
    2: ".cls",    # vbext_ct_ClassModule — class module
    3: ".frm",    # vbext_ct_MSForm      — UserForm (text only; .frx binary skipped)
    100: ".cls",  # vbext_ct_Document    — ThisDocument and document-level class
}


def export_vba(docm_path: str, output_dir: str) -> None:
    docm_path = os.path.abspath(docm_path)
    output_dir = os.path.abspath(output_dir)

    if not os.path.exists(docm_path):
        print(f"ERROR: File not found: {docm_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print(f"Exporting VBA from: {docm_path}")
    print(f"Output directory:   {output_dir}\n")

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = None

    try:
        doc = word.Documents.Open(docm_path)
        vbp = doc.VBProject
        exported = 0
        skipped = 0

        for comp in vbp.VBComponents:
            ext = VBA_EXTENSIONS.get(comp.Type)
            if ext is None:
                print(f"  Skipped (unknown type {comp.Type}): {comp.Name}")
                skipped += 1
                continue

            line_count = comp.CodeModule.CountOfLines
            if line_count == 0:
                print(f"  Empty (0 lines): {comp.Name}{ext}")
                # Still write an empty file to preserve the module list
                code = ""
            else:
                code = comp.CodeModule.Lines(1, line_count)

            filename = comp.Name + ext
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"  Exported: {filename} ({line_count} lines)")
            exported += 1

        print(f"\nDone. {exported} modules exported, {skipped} skipped.")
        print(f"Output: {output_dir}")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_vba_word.py <path_to_docm> [output_dir]")
        sys.exit(1)

    docm = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.abspath(docm))[0] + "_vba"
    export_vba(docm, out)
