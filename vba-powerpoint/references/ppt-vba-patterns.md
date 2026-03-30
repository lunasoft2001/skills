# PowerPoint VBA Patterns Reference

## Enabling VBA Project Access

In PowerPoint: **File → Options → Trust Center → Trust Center Settings → Macro Settings**  
Enable: ✅ *Trust access to the VBA project object model*

Or via registry (run as Administrator):
```reg
[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\PowerPoint\Security]
"AccessVBOM"=dword:00000001
```
*(Replace `16.0` with your Office version: 15.0 = 2013, 16.0 = 2016/2019/365)*

---

## VBA Component Types in PowerPoint

| Component Type | Export Extension | Description |
|---|---|---|
| Standard Module | `.bas` | Regular `Sub` / `Function` procedures |
| Class Module | `.cls` | Class definitions |
| UserForm | `.frm` (text only) | Dialog forms — `.frx` binary is skipped |
| ThisPresentation | `.cls` | Presentation-level event handler (Type 100) |
| Slide modules | `.cls` | Per-slide event handlers (Slide1, Slide2, …) |

---

## Common PowerPoint VBA Patterns

### Presentation Events
```vba
' In ThisPresentation module
Private Sub Presentation_Open()
    ' Fires when presentation opens
End Sub

Private Sub Presentation_BeforeClose(Cancel As Boolean)
    ' Fires before close; set Cancel = True to prevent closing
End Sub

Private Sub Presentation_SlideShowBegin(ByVal Wn As SlideShowWindow)
    ' Fires when slideshow starts
End Sub

Private Sub Presentation_SlideShowNextSlide(ByVal Wn As SlideShowWindow)
    ' Fires on every slide advance
End Sub
```

### Iterating Slides and Shapes
```vba
Dim sld As Slide
For Each sld In ActivePresentation.Slides
    Debug.Print "Slide " & sld.SlideIndex & ": " & sld.Name
    Dim shp As Shape
    For Each shp In sld.Shapes
        If shp.HasTextFrame Then
            Debug.Print "  Shape: " & shp.Name & " — " & shp.TextFrame.TextRange.Text
        End If
    Next shp
Next sld
```

### Modifying Text in Shapes
```vba
' Replace text in all text frames
Dim sld As Slide
Dim shp As Shape
For Each sld In ActivePresentation.Slides
    For Each shp In sld.Shapes
        If shp.HasTextFrame Then
            With shp.TextFrame.TextRange.Find("OldText")
                .Text = "NewText"
            End With
        End If
    Next shp
Next sld
```

### Adding and Formatting Shapes
```vba
Dim sld As Slide
Set sld = ActivePresentation.Slides(1)

' Add a rectangle
Dim shp As Shape
Set shp = sld.Shapes.AddShape(msoShapeRectangle, 100, 100, 300, 150)
shp.TextFrame.TextRange.Text = "Hello!"
shp.TextFrame.TextRange.Font.Size = 24
shp.Fill.ForeColor.RGB = RGB(0, 120, 215)
```

### Slide Show Navigation
```vba
' Jump to a specific slide during slideshow
SlideShowWindows(1).View.GotoSlide 5

' End slideshow
SlideShowWindows(1).View.Exit
```

### Exporting Slides as Images
```vba
Dim sld As Slide
For Each sld In ActivePresentation.Slides
    sld.Export "C:\exports\Slide" & sld.SlideIndex & ".png", "PNG"
Next sld
```

---

## Accessing the VBA Project Programmatically (Python)

```python
import win32com.client

ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True  # PowerPoint often requires Visible = True
pres = ppt.Presentations.Open(r"C:\path\to\Deck.pptm")
vbproject = pres.VBProject

for component in vbproject.VBComponents:
    print(f"Name: {component.Name}  Type: {component.Type}  Lines: {component.CodeModule.CountOfLines}")

pres.Close()
ppt.Quit()
```

> **Note:** PowerPoint COM may require `Visible = True` to avoid hangs.

---

## Module Type Constants (VBA Extensibility)

| Constant | Value | Type |
|---|---|---|
| `vbext_ct_StdModule` | 1 | Standard Module |
| `vbext_ct_ClassModule` | 2 | Class Module |
| `vbext_ct_MSForm` | 3 | UserForm |
| `vbext_ct_Document` | 100 | Presentation / Slide module |

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `Permission denied` on VBA project | Enable "Trust access to the VBA project object model" in Trust Center |
| PowerPoint hangs during COM automation | Set `ppt.Visible = True` before opening presentations |
| Export produces empty `.bas` files | Module has zero lines of code — normal |
| Import fails for `ThisPresentation` | Ensure source code does not include the class header line twice |
| Slide modules not found | Slide event modules (`Slide1`, etc.) exist only if events were added manually in the editor |
