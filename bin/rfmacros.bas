Rem Attribute VB_Name = "NewMacros"
Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Sub rtfconv()
'
' rtfconv Macro
'
'
' Edit as needed, but keep trailing backslashes
  Const strSourcePath = "C:\work\bamca\tmp\"
  Const strTargetPath = "C:\work\bamca\tmp\"
  Dim strFile As String
  Dim doc As Document

  On Error GoTo ErrHandler

  strFile = Dir(strSourcePath & "*.doc")
  Do While Not strFile = ""
    intPos = InStrRev(strFile, ".")
    strOutFile = Left(strFile, intPos - 1)

    Set doc = Documents.Open(FileName:=strSourcePath & strFile, AddToRecentFiles:=False)
    doc.SaveAs FileName:=strTargetPath & strOutFile, FileFormat:=wdFormatRTF
    doc.Close SaveChanges:=wdDoNotSaveChanges
    strFile = Dir
    Sleep 100
  Loop

ExitHandler:
  Set doc = Nothing
  donefile = FreeFile()
  Open strTargetPath & "done.txt" For Output As donefile
  Print #donefile, "finished"
  Close #donefile
Exit Sub

ErrHandler:
  MsgBox Err.Description, vbExclamation
Resume ExitHandler
End Sub

Sub htmlconv()
'
' htmlconv Macro
'
'
' Edit as needed, but keep trailing backslashes
  Const strSourcePath = "C:\work\bamca\tmp\"
  Const strTargetPath = "C:\work\bamca\tmp\"
  Dim strFile As String
  Dim doc As Document

  On Error GoTo ErrHandler

  strFile = Dir(strSourcePath & "*.doc")
  Do While Not strFile = ""
    intPos = InStrRev(strFile, ".")
    strOutFile = Left(strFile, intPos - 1)

    Set doc = Documents.Open(FileName:=strSourcePath & strFile, AddToRecentFiles:=False)
    doc.SaveAs FileName:=strTargetPath & strOutFile, FileFormat:=wdFormatHTML
    doc.Close SaveChanges:=wdDoNotSaveChanges
    strFile = Dir
    Sleep 100
  Loop

ExitHandler:
  Set doc = Nothing
  donefile = FreeFile()
  Open strTargetPath & "done.txt" For Output As donefile
  Print #donefile, "finished"
  Close #donefile
Exit Sub

ErrHandler:
  MsgBox Err.Description, vbExclamation
Resume ExitHandler
End Sub



