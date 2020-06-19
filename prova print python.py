#FUNZIONE MA APRE ACROBAT
import tempfile
import win32api
import win32print


filename = 'C:/Users/tommolini/Desktop/FATTURAPROVA2.pdf'

#tempprinter = "\\\\ber-ser-2\\Laser CED"
currentprinter = win32print.GetDefaultPrinter()

#win32print.SetDefaultPrinter(tempprinter)
win32api.ShellExecute(0, "print", filename, None,  ".",  0)
#