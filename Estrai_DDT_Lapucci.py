import tkinter as tk
from tkinter import ttk
from tkinter import *
import sys
import pyodbc
import shutil
import paramiko
import time
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *  # Additional Import
from functools import partial
from tkcalendar import Calendar
import logging
    


def contaRecord(cursor_):
    #conto quante righe ci sono nella lista filtrata
    row_c = cursor_.execute("SELECT  COUNT(*) FROM   GAMMAtest.dbo.[1_Lapucci_FTCLI] where [DO11_NUMREG_CO99] not in (select [numreg] from [GAMMAtest].[dbo].[_APPO_LAPUCCI] where elab=0)")
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

    #finchè il count non mi restituisce la stringa [(0, )] (che si presenta quando non ci sono righe nella vista filtrata) esegue il ciclo:
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

        #Divido il risultato della query nei campi corrispondenti:
        #print(stringaIntera)
        stringaDivisa = stringaIntera.split(", ")
        #print(stringaDivisa)
        row_count = contaRecord(cursor)
        print("Rimanenti: "+str(row_count)+"su "+str(row_count_tot)+"| NumReg: " + nreg + "\n")

        #Ricavo il campo myPathName:
        stringa2ConSlash = stringaDivisa[1].replace('\\\\',"/")
        myPathName = stringa2ConSlash.replace("'","")
        print("Path: " + myPathName + "\n")

        #ricavo il campo [myFileName]:
        stringa3SenzaApici = stringaDivisa[2].replace("'","")
        myFileName = stringa3SenzaApici[:-2]
        print("Nome: " + myFileName + "\n")

        #imposto il path temporaneo dove avverrà il renaming del file e rinomino il file:
        nuovoPath = "C:/DDT_Lapucci/" + myFileName
        
        #Copio il file nella cartella temporanea
        shutil.copy(myPathName, nuovoPath)

        print("Il file è stato copiato correttamente, cambio il flag su _APPO_LAPUCCI..."+'\n')
        #Inserisco l'elab nella tabella di appoggio
        cursor.execute("UPDATE [GAMMAtest].[dbo].[_APPO_LAPUCCI] SET [elab] =1 where [_APPO_LAPUCCI].[numreg] = ? ", nreg)
        cnxn.commit()

if __name__ == '__main__':
    main()