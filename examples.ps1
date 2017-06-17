Set-Location ".\examples"
Get-ChildItem -Filter *.md |
Foreach-Object {
    Remove-Item ($_.BaseName + '.tex')
    python ..\mdtotex.py $_.FullName
}
Set-Location ".."
