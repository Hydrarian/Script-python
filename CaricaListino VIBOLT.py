#Import listino prodotti Vibolt

import shutil
import os
import datetime
import zipfile
import ftplib
			
# Path
sourceFolder = "C:/ExportD365/VIBOLT/Intestazioni/"  #"C:/Users/tommolini/Desktop/A/" 
destinationFolder = "C:/ExportD365/VIBOLT/" # "C:/Users/tommolini/Desktop/B/"  
archivedFolder =  "C:/ExportD365/VIBOLT/Archivio/"  #'C:/Users/tommolini/Desktop/B/C' 
listFileInSource = os.listdir(sourceFolder) #lista dei nomi file in sourceFolder

#copio tutti i file .xml presenti nella cartella source nella cartella superiore
for f in listFileInSource:
	if f.endswith(".xml"):
		shutil.copy(sourceFolder + f, destinationFolder)

listFileInDestination = os.listdir(destinationFolder)

#acquisisco data e ora corrente nel formato YYYY-MM-DD HH-MM-SS
now = datetime.datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H:%M:%S")
date_time = now.strftime("%m-%d-%Y, %H-%M-%S")
zipName = '05_PRODOTTI_' + date_time + '.zip'

#creo un oggetto ZipFile
zipObj = zipfile.ZipFile(destinationFolder + zipName, 'w')

#aggiungo i file nello zip (solo .csv e .xml)
for f in listFileInDestination:
	if f.endswith(".csv") or f.endswith(".xml"):
		if f.startswith("VIB "):
			os.rename(destinationFolder + f, destinationFolder + f[4:])
			zipObj.write(destinationFolder + f[4:], os.path.basename(destinationFolder + f[4:]))
			os.rename(destinationFolder +f[4:], destinationFolder  + f)
		else: zipObj.write(destinationFolder + f, os.path.basename(destinationFolder + f))

#chiudo l'oggetto zip
zipObj.close()

ftp = ftplib.FTP_TLS()			#creo connessione FTP
ftp.set_debuglevel(2)
ftp.connect('77.89.18.32', 8021)
ftp.sendcmd('USER UtenteFTP')
ftp.sendcmd('PASS 1a2b3c4d5e!-!')
ftp.dir()

remotePath = '/D365_RIS_IN/Input/' #setto la destinazione su ftp
ftp.cwd(remotePath)
fp = open(destinationFolder + zipName, 'rb')
ftp.storbinary('STOR %s' % zipName, fp)
ftp.quit()
fp.close()		