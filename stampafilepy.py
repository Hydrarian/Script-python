#FUNZIONA MA STAMPA COI BORDI TAGLIATI

import win32api
import win32print
import shutil


GHOSTSCRIPT_PATH = "\\\\BER-OFFICE\\FattureB2B\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = "\\\\BER-OFFICE\\FattureB2B\\GSPRINT\\gsprint.exe"

# YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
currentprinter = win32print.GetDefaultPrinter()

#per tutti i file dentro la cartella fare questo:
filename = 'C:/Users/tommolini/Desktop/FATTURAPROVA2.pdf'

win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" ""'+filename, '.', 0)

#shutil.copy(filename, 'C:/Users/tommolini/Desktop/A/')