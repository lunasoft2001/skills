"""
export_vba_ppt.py — Export all VBA modules from a PowerPoint .pptm / .potm file.

Usage:
    python export_vba_ppt.py <path_to_pptm> [output_dir]

Requirements:
    pip install pywin32
    PowerPoint must be installed.
    "Trust access to the VBA project object model" must be enabled in PowerPoint Trust Center.
"""

import sys
import os
import win32com.client

# Maps VBA component types to file extensions
VBA_EXTENSIONS = {
    1: ".bas",    # vbext_ct_StdModule   — standard module
    2: ".cls",    # vbext_ct_ClassModule — class module
    3: ".frm",    # vbext_ct_MSForm      — UserForm (text only; .frx binary skipped)
    100: ".cls",  # vbext_ct_Document    — ThisPresentation and slide modules
}


def export_vba(pptm_path: str, output_dir: str) -> None:
    pptm_path = os.path.abspath(pptm_path)
    output_dir = os.path.abspath(output_dir)

    if not os.path.exists(pptm_path):
        print(f"ERROR: File not found: {pptm_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print(f"Exporting VBA from: {pptm_path}")
    print(f"Output directory:   {output_dir}\n")

    # PowerPoint often requires Visible = True to avoid COM hangs
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = True
    pres = None

    try:
        pres = ppt.Presentations.Open(pptm_path, WithWindow=False)
        vbp = pres.VBProject
        exported = 0
        skipped = 0

        for comp in vbp.VBComponents:
            ext = VBA_EXTENSIONS.get(comp.Type)
            if ext is None:
                print(f"  Skipped (unknown type {comp.Type}): {comp.Name}")
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

        print(f"\nDone. {exported} modules exported, {skipped} skipped.")
        print(f"Output: {output_dir}")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if pres is not None:
            pres.Close()
        ppt.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_vba_ppt.py <path_to_pptm> [output_dir]")
        sys.exit(1)

    pptm = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.abspath(pptm))[0] + "_vba"
    export_vba(pptm, out)
