Sub convert_to_csv()
    'VBA code to convert Excel documents to csv.
    'Requires the following ranges to be labeled:
    '   inpath - root path of input files
    '   outpath - root path of output files
    '   files - column of filenames with the left cell
    '           containing the subpath
    Set inpath = Range("inpath")
    Set outpath = Range("outpath")
    Set fnames = Range("files")
    Set test = Range("test")
    
    For Each fname In fnames
        fullin = inpath & fname.Offset(0, -1)
        fullout = outpath & fname.Offset(0, -1)
        Workbooks.Open Filename:=fullin & fname
        If Dir(fullout, vbDirectory) = "" Then
            MkDir fullout
        End If
        For Each ws In ActiveWorkbook.Worksheets
            ws.Activate
            ActiveWorkbook.SaveAs Filename:=fullout & "fname_" & fname _ 
                & "_sheet_" & ws.Name & ".csv", FileFormat:=xlCSV, _
                CreateBackup:=False
        Next
        ActiveWorkbook.Close savechanges:=False
    Next
End Sub
