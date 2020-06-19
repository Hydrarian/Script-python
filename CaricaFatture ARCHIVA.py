import pyodbc
import shutil

#Dati di connession SQL
server = '172.16.1.15' 
database = 'VITMAN' 
username = 'sa' 
password = 'ber-sql-sa' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

L=[] # creo un array per contenere i risultati della query
cursor = cnxn.cursor()
row = cursor.execute("SELECT  [IdObject], [myPathName], [myKnosDocumentFileName] FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= '2019-01-01' and IdObject not in (select idElab from _APPO_ddtc_archiva) order by IdObject asc")
rows = cursor.fetchall()

# riempio la lista con tutte le righe del risultato della query
for row in rows:
    L.append(row)

#i=0
for i in range(len(L)):
	print(L[i])
	StringaIntera=str(L[i])
	stringaDivisa=StringaIntera.split(", ")
	print("1: " + stringaDivisa[0] + "\n")
	Stringa1ConSlash=stringaDivisa[1].replace('\\\\',"/")
	Stringa1ConSlash2=Stringa1ConSlash.replace("'","")
	print("2: " + Stringa1ConSlash2 + "\n")
	print("3: " + stringaDivisa[2] + "\n")
	Stringa2SenzaApici=stringaDivisa[2].replace("'","")
	Stringa2SenzaApici2=Stringa2SenzaApici[:-1]
	print(Stringa2SenzaApici2)

	shutil.copy(Stringa1ConSlash2, "C:/Users/administrator.BERARDI/Desktop/MarcoTEST/2019_" + Stringa2SenzaApici2)
#for i in range(len(L)):
	#print(L[i])