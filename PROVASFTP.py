import pyodbc
import shutil
import paramiko

#Dati di connession SQL
server = '172.16.1.15' 
database = 'GAMMAtest' 
username = 'sa' 
password = 'ber-sql-sa' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()
row = cursor.execute("SELECT  top 1 [IdObject], [myPathName], [myKnosDocumentFileName] FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= '2019-01-01' and IdObject not in (select idElab from _APPO_ddtc_archiva) order by IdObject asc")
rows = cursor.fetchone()

print(rows)
