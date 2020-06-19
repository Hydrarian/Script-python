import os
import shutil
import win32api
import win32print
import subprocess

currentprinter = win32print.GetDefaultPrinter()
print(currentprinter)
GHOSTSCRIPT_PATH = "\\\\BER-OFFICE\\FattureB2B\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = "\\\\BER-OFFICE\\FattureB2B\\GSPRINT\\gsprint.exe"

file_path = 'C:/Users/tommolini/Desktop/FATTURAPROVA2.pdf'
p = subprocess.Popen([r"//BER-OFFICE/FattureB2B/GSPRINT/gsprint.exe",  "C:/Users/tommolini/Desktop/FATTURAPROVA2.pdf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate() # waits for the gs process to end
print(stdout)
print(stderr)
#shutil.move('C:/Users/tommolini/Desktop/FATTURAPROVA2.pdf','C:/Users/tommolini/Desktop/A/') # now the file can be removed
#muove il file  dentro la cartella A in Desktop




