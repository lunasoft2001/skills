# Access VBA Patterns Reference

## Enabling VBA Project Access

In Access: **File → Options → Trust Center → Trust Center Settings → Macro Settings**  
Enable: ✅ *Trust access to the VBA project object model*

Or via registry (run as Administrator):
```reg
[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Access\Security]
"AccessVBOM"=dword:00000001
```
*(Replace `16.0` with your Office version: 15.0 = 2013, 16.0 = 2016/2019/365)*

---

## VBA Component Types in Access

| Component Type | Export Extension | Description |
|---|---|---|
| Standard Module | `.bas` | General-purpose Sub/Function procedures |
| Class Module | `.cls` | Class definitions |
| Form module | *(not exported by vba-access)* | Code behind forms — use **access-analyzer** |
| Report module | *(not exported by vba-access)* | Code behind reports — use **access-analyzer** |

> **vba-access exports only standard modules and class modules.** For form/report code, use the **access-analyzer** skill.

---

## Common Access VBA Patterns

### Database Connection (DAO)
```vba
Dim db As DAO.Database
Dim rs As DAO.Recordset

Set db = CurrentDb()
Set rs = db.OpenRecordset("SELECT * FROM Clientes WHERE Activo = True")

Do While Not rs.EOF
    Debug.Print rs!ClienteID & " - " & rs!Nombre
    rs.MoveNext
Loop

rs.Close
Set rs = Nothing
Set db = Nothing
```

### Database Connection (ADO)
```vba
Dim conn As ADODB.Connection
Dim rs As ADODB.Recordset

Set conn = CurrentProject.Connection
Set rs = New ADODB.Recordset
rs.Open "SELECT * FROM Pedidos WHERE Estado = 'Pendiente'", conn

Do While Not rs.EOF
    Debug.Print rs!PedidoID
    rs.MoveNext
Loop

rs.Close
Set rs = Nothing
Set conn = Nothing
```

### Running a Saved Query
```vba
' Execute an action query (no results)
CurrentDb.Execute "qryActualizarPrecios", dbFailOnError

' Open a select query as recordset
Dim rs As DAO.Recordset
Set rs = CurrentDb.OpenRecordset("qryClientesActivos")
```

### Form Events Pattern
```vba
' Typically in form module (not exported by vba-access)
Private Sub Form_Load()
    Me.txtFecha.Value = Date
End Sub

Private Sub cmdGuardar_Click()
    If IsNull(Me.txtNombre) Then
        MsgBox "El nombre es obligatorio.", vbExclamation
        Me.txtNombre.SetFocus
        Exit Sub
    End If
    DoCmd.RunCommand acCmdSaveRecord
End Sub
```

### Opening and Closing Forms
```vba
' Open a form
DoCmd.OpenForm "frmClientes", acNormal, , "ClienteID = " & Me.ClienteID

' Close a form
DoCmd.Close acForm, "frmClientes", acSaveNo
```

### Error Handling Pattern
```vba
Public Function GetClienteName(ClienteID As Long) As String
    On Error GoTo ErrHandler

    Dim rs As DAO.Recordset
    Set rs = CurrentDb.OpenRecordset("SELECT Nombre FROM Clientes WHERE ClienteID = " & ClienteID)

    If Not rs.EOF Then
        GetClienteName = rs!Nombre
    End If

    rs.Close
    Exit Function

ErrHandler:
    MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
    GetClienteName = ""
End Function
```

### Transaction Handling
```vba
Dim ws As DAO.Workspace
Set ws = DBEngine.Workspaces(0)

ws.BeginTrans
On Error GoTo Rollback
    CurrentDb.Execute "UPDATE Inventario SET Stock = Stock - 1 WHERE ProductoID = 5", dbFailOnError
    CurrentDb.Execute "INSERT INTO Movimientos (ProductoID, Cantidad) VALUES (5, -1)", dbFailOnError
ws.CommitTrans
Exit Sub

Rollback:
    ws.Rollback
    MsgBox "Transaction rolled back: " & Err.Description, vbCritical
```

---

## Accessing the VBA Project Programmatically (Python)

```python
import win32com.client

access = win32com.client.Dispatch("Access.Application")
access.Visible = False
access.OpenCurrentDatabase(r"C:\path\to\MyApp.accdb")
vbproject = access.VBE.ActiveVBProject

for component in vbproject.VBComponents:
    print(f"Name: {component.Name}  Type: {component.Type}  Lines: {component.CodeModule.CountOfLines}")

access.CloseCurrentDatabase()
access.Quit()
```

---

## Module Type Constants (VBA Extensibility)

| Constant | Value | Type |
|---|---|---|
| `vbext_ct_StdModule` | 1 | Standard Module |
| `vbext_ct_ClassModule` | 2 | Class Module |
| `vbext_ct_MSForm` | 3 | UserForm |
| `vbext_ct_Document` | 100 | Form or Report module |

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `Permission denied` on VBA project | Enable "Trust access to the VBA project object model" in Trust Center |
| `.laccdb` lock file present | Another user or process has the database open — close all instances |
| Import fails with `Name conflict` | Rename conflicting module before importing |
| `Access.Application` not found | Access is not installed or COM registration is broken |
| Exported modules show garbled characters | Ensure files are read/written with UTF-8 encoding |
