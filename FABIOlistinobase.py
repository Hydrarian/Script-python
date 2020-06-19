import shutil
import os
import datetime
import zipfile
			
source = "C:/ExportD365ListinoBase/Intestazioni/" #"C:/Users/tommolini/Desktop/A/"
destination = "C:/ExportD365ListinoBase/" #"C:/Users/tommolini/Desktop/B/" 
archived =  "C:/ExportD365ListinoBase/Archivio/"  
files = os.listdir(source)

for f in files:
	if f.endswith(".xml"):
		shutil.move(source+f, destination)

#acquisisco data e ora corrente nel formato YYYY-MM-DD HH:MM:SS
now = datetime.datetime.now()

year = now.strftime("%Y")
print("year:", year)
month = now.strftime("%m")
print("month:", month)
day = now.strftime("%d")
print("day:", day)
time = now.strftime("%H:%M:%S")
print("time:", time)
date_time = now.strftime("%m-%d-%Y, %H-%M-%S")

filesb = os.listdir(destination)
nomeZip = destination+'LISTINOBASE_03_'+date_time+'.zip'
# create a ZipFile object
zipObj = zipfile.ZipFile(nomeZip, 'w')

	# Add multiple files to the zip
for f in filesb:
	if f.endswith(".csv") or f.endswith(".xml"):
		zipObj.write(destination+f, os.path.basename(destination+f))

# close the Zip File
zipObj.close()

destinationFTP= 'Z:/D365_RIS_IN/Input/'
shutil.move(nomeZip, destinationFTP)		

filesb = os.listdir(destination)
for f in filesb:
	if os.path.isfile(f) and not f.endswith(".exe"):
		shutil.move(destination+f, archived+f)
#shutil.move(source+f, destination)