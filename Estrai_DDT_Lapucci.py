import sys
import pyodbc
import shutil
import time
from functools import partial
    


def contaRecord(cursor_):
    #conto quante righe ci sono nella lista filtrata
    row_c = cursor_.execute("SELECT  COUNT(*) FROM GAMMAtest.dbo.[1_Lapucci_FTCLI] where [DO11_NUMREG_CO99] in (select [numreg] from [GAMMAtest].[dbo].[_APPO_LAPUCCI] where elab=0)")
    row_count_ = str(cursor_.fetchall())
    charToDeleteInrow_count="[(,)] "

    for char in charToDeleteInrow_count:
        row_count_ = row_count_.replace(char,"")
    return int(row_count_)

def connettiSQL():
    #Dati di connession SQL
    server = '172.16.1.15' 
    database = 'GAMMAtest' 
    username = 'sa' 
    password = 'ber-sql-sa' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    #return cnxn.cursor()
    return cnxn

def main():
    cnxn = connettiSQL()
    cursor = cnxn.cursor()
    row_count = contaRecord(cursor)
    row_count_tot = row_count
    print(str(row_count_tot)+' record da processare\n')

    #finchè il count non mi restituisce 0:
    while row_count!=0:

        #Eseguo la query:
        row = cursor.execute("SELECT top(1) numreg FROM GAMMAtest.dbo._APPO_LAPUCCI where elab = 0")
        nreg = str(cursor.fetchall())  #prendo il numreg
        #print(nreg)
        charToDeleteInrow_count="[(,)]'"

        for char in charToDeleteInrow_count:
            nreg = nreg.replace(char,"")

        nreg_ = int(nreg)
        #Ricavo il numero di righe rimanenti:
        #print(nreg)
        row = cursor.execute("SELECT  top(1) [IdObject], [myPathName], [myFileName] FROM   GAMMAtest.dbo.[1_Lapucci_FTCLI] where isnull(NomeFilePerArchiva,'') <>''  and DO11_NUMREG_CO99 = ? order by [NumeroProtocollo], [myDataFileName] desc", nreg_)
        stringaIntera = str(cursor.fetchall())
        if stringaIntera=="[]":  #se la stringa è vuota vuol dire che non c'è corrispondenza tra vista e tabella, quindi passo al prossimo numreg
            #print(stringaIntera)
            print(nreg+ " non presente in 1_Lapucci_FTCLI")
            cursor.execute("UPDATE [GAMMAtest].[dbo].[_APPO_LAPUCCI] SET [elab] =1 where [_APPO_LAPUCCI].[numreg] = ? ", nreg)
            cnxn.commit()
            continue
        else: 
            #Divido il risultato della query nei campi corrispondenti:
            #print(stringaIntera)
            stringaDivisa = stringaIntera.split(", ")
            #print(stringaDivisa)
            #print(stringaDivisa)
            row_count = contaRecord(cursor)
            print("Rimanenti: "+str(row_count)+" su "+str(row_count_tot)+" | NumReg: " + nreg + "\n")

            #Ricavo il campo myPathName:
            #print(stringaDivisa[1])
            stringa2ConSlash = stringaDivisa[1].replace('\\\\',"/")
            myPathName = stringa2ConSlash.replace("'","")
            #print("Path: " + myPathName + "\n")

            #ricavo il campo [myFileName]:
            stringa3SenzaApici = stringaDivisa[2].replace("'","")
            myFileName = stringa3SenzaApici[:-2]
            print("Nome: " + myFileName + "\n")

            #imposto il path temporaneo dove avverrà il renaming del file e rinomino il file:
            nuovoPath = "C:/DDT_Lapucci/" + nreg + "_" + myFileName
            
            #Copio il file nella cartella temporanea
            shutil.copy(myPathName, nuovoPath)

            #print("Il file è stato copiato correttamente, cambio il flag su _APPO_LAPUCCI..."+'\n')
            #Inserisco l'elab nella tabella di appoggio
            cursor.execute("UPDATE [GAMMAtest].[dbo].[_APPO_LAPUCCI] SET [elab] =1 where [_APPO_LAPUCCI].[numreg] = ? ", nreg)
            cnxn.commit()

        row_count = contaRecord(cursor)
    print("========= FINE =========")

if __name__ == '__main__':
    main()