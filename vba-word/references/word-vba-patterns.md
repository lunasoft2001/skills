# Word VBA Patterns Reference

## Enabling VBA Project Access

In Word: **File → Options → Trust Center → Trust Center Settings → Macro Settings**  
Enable: ✅ *Trust access to the VBA project object model*

Or via registry (run as Administrator):
```reg
[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Word\Security]
"AccessVBOM"=dword:00000001
```
*(Replace `16.0` with your Office version: 15.0 = 2013, 16.0 = 2016/2019/365)*

---

## VBA Component Types in Word

| Component Type | Export Extension | Description |
|---|---|---|
| Standard Module | `.bas` | Regular `Sub` / `Function` procedures |
| Class Module | `.cls` | Class definitions |
| UserForm | `.frm` (text only) | Dialog forms — `.frx` binary is skipped |
| ThisDocument | `.cls` | Document-level event handler (Type 100) |

---

## Common Word VBA Patterns

### Document Events
```vba
Private Sub Document_Open()
    ' Fires when the document opens
End Sub

Private Sub Document_Close()
    ' Fires before document closes
End Sub

Private Sub Document_BeforeSave(ByVal SaveAsUI As Boolean, Cancel As Boolean)
    ' Fires before save; set Cancel = True to prevent saving
End Sub

Private Sub Document_ContentControlOnEnter(ByVal ContentControl As ContentControl)
    ' Fires when user enters a content control
End Sub
```

### Working with Ranges and Selection
```vba
' Iterate all paragraphs
Dim para As Paragraph
For Each para In ActiveDocument.Paragraphs
    Debug.Print para.Range.Text
Next para

' Find and replace all occurrences
With ActiveDocument.Content.Find
    .Text = "OldText"
    .Replacement.Text = "NewText"
    .Execute Replace:=wdReplaceAll
End With

' Insert text at cursor
Selection.TypeText "Hello, World!"
```

### Working with Tables
```vba
Dim tbl As Table
For Each tbl In ActiveDocument.Tables
    Dim r As Integer, c As Integer
    For r = 1 To tbl.Rows.Count
        For c = 1 To tbl.Columns.Count
            Debug.Print tbl.Cell(r, c).Range.Text
        Next c
    Next r
Next tbl
```

### Bookmarks
```vba
' Update a bookmark's text
ActiveDocument.Bookmarks("MyBookmark").Range.Text = "New Value"

' Check if bookmark exists
If ActiveDocument.Bookmarks.Exists("MyBookmark") Then
    ' ...
End If
```

### Content Controls
```vba
Dim cc As ContentControl
For Each cc In ActiveDocument.ContentControls
    If cc.Tag = "CompanyName" Then
        cc.Range.Text = "Contoso Ltd."
    End If
Next cc
```

### Updating All Fields
```vba
ActiveDocument.Fields.Update
' Also update headers/footers
Dim sec As Section
For Each sec In ActiveDocument.Sections
    sec.Headers(wdHeaderFooterPrimary).Range.Fields.Update
    sec.Footers(wdHeaderFooterPrimary).Range.Fields.Update
Next sec
```

---

## Accessing the VBA Project Programmatically (Python)

```python
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
doc = word.Documents.Open(r"C:\path\to\MyDoc.docm")
vbproject = doc.VBProject

for component in vbproject.VBComponents:
    print(f"Name: {component.Name}  Type: {component.Type}  Lines: {component.CodeModule.CountOfLines}")

doc.Close(False)
word.Quit()
```

---

## Module Type Constants (VBA Extensibility)

| Constant | Value | Type |
|---|---|---|
| `vbext_ct_StdModule` | 1 | Standard Module |
| `vbext_ct_ClassModule` | 2 | Class Module |
| `vbext_ct_MSForm` | 3 | UserForm |
| `vbext_ct_Document` | 100 | Document module (ThisDocument) |

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `Permission denied` on VBA project | Enable "Trust access to the VBA project object model" in Trust Center |
| Export produces empty files | Module has zero lines of code — this is normal |
| `Word.Application` not found | Word is not installed or COM registration is broken |
| Import fails silently | Check that module names match exactly (case-sensitive) |
| `.frx` binary missing after export | Binary UserForm resources are not text-exportable; skip them |
