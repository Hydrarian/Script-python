import pyodbc
import shutil
import paramiko
import time

#Dati di connession SQL
server = '172.16.1.15' 
database = 'GAMMAtest' 
username = 'sa' 
password = 'ber-sql-sa' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()
#conto quante righe ci sono nella lista filtrata
row_c = cursor.execute("SELECT  COUNT(*) FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= '2019-01-01' and IdObject not in (select idElab from _APPO_ddtc_archiva)")
row_count = str(cursor.fetchall())
print(row_count+' record da processare\n')

#finchè il count non mi restituisce la stringa [(0, )] (che si presenta quando non ci sono righe nella vista filtrata) esegue il ciclo:
while row_count!="[(0, )]":
	#Eseguo la query:
	row = cursor.execute("SELECT  top 1 [IdObject], [myPathName], [myFileName] FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= '2019-01-01' and IdObject not in (select idElab from _APPO_ddtc_archiva) order by IdObject asc")
	rows = cursor.fetchall()

	#print('Prendo il record: ' + str(rows)+'\n')
	#Divido il risultato della query nei campi corrispondenti:
	stringaIntera=str(rows)
	stringaDivisa=stringaIntera.split(", ")

	#Ricavo il campo IdObject:
	stringa1SenzaParentesi=stringaDivisa[0].replace("[(","")
	print("IdObject: " + stringa1SenzaParentesi + "\n")

	#Ricavo il campo myPathName:
	stringa2ConSlash=stringaDivisa[1].replace('\\\\',"/")
	stringa2ConSlash2=stringa2ConSlash.replace("'","")
	print("Path: " + stringa2ConSlash2 + "\n")

	#ricavo il campo myKnosDocumentFileName:
	stringa3SenzaApici=stringaDivisa[2].replace("'","")
	stringa3SenzaApici2=stringa3SenzaApici[:-2]
	print("Nome: " + stringa3SenzaApici2 + "\n")

	#imposto il path temporaneo dove avverra il renaming del file e rinomino il file:
	pathFileTemporaneo="C:/Users/administrator.BERARDI/Desktop/MarcoTEST/2019_" + stringa3SenzaApici2
	#Copio il file nella cartella temporanea
	shutil.copy(stringa2ConSlash2, pathFileTemporaneo)

	#Mi connetto all'sftp
	ssh_client = paramiko.SSHClient() 
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
	ssh_client.connect(hostname='ftp.archivagroup.it',port=2411,username='berardibulloneriesrl',password='fzU4@wUD_Joy') 
	s = ssh_client.open_sftp()
	#Carico il file sull'SFTP
	s.put(pathFileTemporaneo, '/SPOOL/DDTC/'+ "2019_" +stringa3SenzaApici2)        #DA CAMBIARE
	#attendo 2 secondi prima di fare il controllo di avvenuto upload:
	#time.sleep(2)

	#Controllo se dopo l'upload il file esiste sull'sftp (se non esiste è andato male qualcosa e fermo il ciclo (potrò poi riprendere da dove mi sono fermato grazie all'IdObject:
	try:
		#print('/TEST/'+ stringa3SenzaApici2)
		print(s.stat('/SPOOL/DDTC/'+ "2019_" +stringa3SenzaApici2))				#DA CAMBIARE
		print("Il file è stato caricato correttamente, scrivo l'IdObject sul _APPO_ddtc_archiva"+'\n')
		#Inserisco l'IdObject nella tabella di appoggio
		cursor.execute("INSERT INTO [GAMMAtest].[dbo].[_APPO_ddtc_archiva] (idElab) VALUES  ("+stringa1SenzaParentesi+")")
		cnxn.commit()
	except IOError:
	    print("L'upload del file "+stringa3SenzaApici2+" non è riuscito. Il suo IdObject non sarà inserito in tabella di appoggio"+'\n')

	#Elimino il file temporaneo
	os.remove(pathFileTemporaneo)
	#time.sleep(2)
#conto quante righe ci sono nella lista filtrata
row_c = cursor.execute("SELECT  COUNT(*) FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= '2019-01-01' and IdObject not in (select idElab from _APPO_ddtc_archiva)")
row_count = str(cursor.fetchall())
print("L'upload è concluso. Mancano "+row_count+" record da processare."+'\n')