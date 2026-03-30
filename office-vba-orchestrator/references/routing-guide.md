# Office VBA Suite — Routing Guide

This reference details how to detect the target Office application and select the correct skill.

## File Type Detection

### By File Extension

| Extension | Application | Skill |
|-----------|-------------|-------|
| `.xlsm` | Excel (macro-enabled workbook) | **vbaExcel** |
| `.xlam` | Excel (add-in) | **vbaExcel** |
| `.xltm` | Excel (macro-enabled template) | **vbaExcel** |
| `.docm` | Word (macro-enabled document) | **vba-word** |
| `.dotm` | Word (macro-enabled template) | **vba-word** |
| `.pptm` | PowerPoint (macro-enabled presentation) | **vba-powerpoint** |
| `.potm` | PowerPoint (macro-enabled template) | **vba-powerpoint** |
| `.ppsm` | PowerPoint (macro-enabled show) | **vba-powerpoint** |
| `.accdb` | Access (database) | **vba-access** |
| `.mdb` | Access (legacy database) | **vba-access** |
| `.otm` | Outlook (template) | ❌ **Not supported** |

### By User Intent Keywords

| Keyword / phrase | Likely skill |
|------------------|--------------|
| Excel, xlsm, workbook, spreadsheet | **vbaExcel** |
| Word, docm, document, dotm | **vba-word** |
| PowerPoint, pptm, presentation, slides | **vba-powerpoint** |
| Access, accdb, database (VBA only) | **vba-access** |
| Access, accdb, full analysis, tables, queries, forms | **access-analyzer** |
| Outlook | ❌ Not supported |

---

## Routing Decision Tree

```
User mentions an Office VBA task
        │
        ├─ File extension or app name identifiable?
        │       ├─ YES → Map via table above → delegate to skill
        │       └─ NO  → Ask user: "Which Office application? (Excel / Word / PowerPoint / Access)"
        │
        ├─ User wants VBA code only (modules, classes)?
        │       └─ YES → Use vbaExcel / vba-word / vba-powerpoint / vba-access
        │
        ├─ User wants full Access DB analysis (tables, queries, forms, reports)?
        │       └─ YES → Use access-analyzer instead of vba-access
        │
        └─ User mentions Outlook?
                └─ YES → Inform: Outlook VBA is not supported in this suite
```

---

## Scope Boundaries

### vba-access vs access-analyzer

| Capability | vba-access | access-analyzer |
|---|---|---|
| Export standard/class modules | ✅ | ✅ |
| Export form & report code | ❌ | ✅ |
| Export table structures | ❌ | ✅ |
| Export queries | ❌ | ✅ |
| Export macros | ❌ | ✅ |
| Git integration | ❌ | ✅ |
| Full refactoring plan | ❌ | ✅ |

**Rule:** If the user only needs to edit VBA code → `vba-access`. If they need full database analysis or refactoring → `access-analyzer`.

---

## Parallel Processing (Multiple File Types)

If the user needs to process more than one Office application in the same session:

1. Backup **all** files before starting any imports.
2. Run each skill independently and sequentially.
3. Validate each application after import before moving to the next.

Example sequence:
```
1. Backup workbook.xlsm + MyDoc.docm
2. Export workbook.xlsm → vbaExcel
3. Export MyDoc.docm → vba-word
4. Refactor both in VS Code
5. Import workbook.xlsm → vbaExcel (validate)
6. Import MyDoc.docm → vba-word (validate)
```

---

## Prerequisites by Application

| Application | Python package | COM object | VBOM registry key path |
|---|---|---|---|
| Excel | `pywin32` | `Excel.Application` | `Office\16.0\Excel\Security` |
| Word | `pywin32` | `Word.Application` | `Office\16.0\Word\Security` |
| PowerPoint | `pywin32` | `PowerPoint.Application` | `Office\16.0\PowerPoint\Security` |
| Access | `pywin32` | `Access.Application` | `Office\16.0\Access\Security` |

All require Windows + the respective Office application installed.
