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

ssh_client = paramiko.SSHClient() 
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh_client.connect(hostname='ftp.archivagroup.it',port=2411,username='berardibulloneriesrl',password='fzU4@wUD_Joy')  
s = ssh_client.open_sftp()
#print (paramiko.__version__)
#print(s)

class t:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Carica DDTC BERARDI")     # Add a title
        self.s = ttk.Style(self.root)
        self.s.theme_use('clam')
        self.root.geometry("300x230") #Width x Height

        self.beginDate = ''
        self.endDate = ''

        self.buttonBeginDate = ttk.Button(self.root, text='Data Inizio', command=self.selectBeginDate).pack(padx=10, pady=10)
        self.buttonEndDate = ttk.Button(self.root, text='Data Fine', command=self.selectEndDate).pack(padx=10, pady=10)
        self.begin = ttk.Button(self.root, text='Procedi', command=self.caricaDDTC).pack(padx=10, pady=10)
        self.buttonExit = ttk.Button(self.root, text='Esci', command=sys.exit).pack(padx=10, pady=10)

        self.root.mainloop()

    def contaRecord(self, cursor_):
        #conto quante righe ci sono nella lista filtrata
        row_c = cursor_.execute("SELECT  COUNT(*) FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= ? AND DataProtocollo <= ? and IdObject not in (select idElab from _APPO_ddtc_archiva)", self.beginDate, self.endDate)
        row_count_ = str(cursor_.fetchall())
        charToDeleteInrow_count="[(,)]"

        for char in charToDeleteInrow_count:
            row_count_ = row_count_.replace(char,"")
        return row_count_

    def connettiSQL(self):
        #Dati di connession SQL
        server = '172.16.1.15' 
        database = 'GAMMAtest' 
        username = 'sa' 
        password = 'ber-sql-sa' 
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        #return cnxn.cursor()
        return cnxn

    def caricaDDTC(self):
        sleep_time_default_value = 5
        sleep_time_selected = int(input("Secondi di sleep (default=5)? ")) or sleep_time_default_value

        cnxn = self.connettiSQL()
        cursor = cnxn.cursor()
        row_count = self.contaRecord(cursor)
        row_count_tot = row_count
        print(row_count_tot+'record da processare\n')

        #finchè il count non mi restituisce la stringa [(0, )] (che si presenta quando non ci sono righe nella vista filtrata) esegue il ciclo:
        while row_count!='0 ':

            #Eseguo la query:
            row = cursor.execute("SELECT  top 1 [IdObject], [myPathName], [myFileName] FROM   GAMMAtest.dbo.[1_Archiva_DDTC] where isnull(NomeFilePerArchiva,'') <>'' AND DataProtocollo >= ? AND DataProtocollo <= ? and IdObject not in (select idElab from _APPO_ddtc_archiva) order by [NumeroProtocollo], [myDataFileName] desc", self.beginDate, self.endDate)
            rows = cursor.fetchall()

            #Divido il risultato della query nei campi corrispondenti:
            stringaIntera=str(rows)
            stringaDivisa=stringaIntera.split(", ")

            #Ricavo il numero di righe rimanenti:
            row_count = self.contaRecord(cursor)

            #Ricavo il campo IdObject:
            stringa1SenzaParentesi=stringaDivisa[0].replace("[(","")
            print("Rimanenti: "+row_count+"su "+row_count_tot+"| IdObject: " + stringa1SenzaParentesi + "\n")

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

            s.put(pathFileTemporaneo, '/SPOOL/DDTC/'+ "2019_" +stringa3SenzaApici2)        #DA CAMBIARE

            #Controllo se dopo l'upload il file esiste sull'sftp (se non esiste è andato male qualcosa e fermo il ciclo (potrò poi riprendere da dove mi sono fermato grazie all'IdObject:
            try:
                #print('/TEST/'+ stringa3SenzaApici2)
                print(s.stat('/SPOOL/DDTC/'+ "2019_" +stringa3SenzaApici2))             #DA CAMBIARE
                print("Il file è stato caricato correttamente, scrivo l'IdObject sul _APPO_ddtc_archiva"+'\n')
                #Inserisco l'IdObject nella tabella di appoggio
                cursor.execute("INSERT INTO [GAMMAtest].[dbo].[_APPO_ddtc_archiva] (idElab) VALUES  ("+stringa1SenzaParentesi+")")
                cnxn.commit()

            except IOError:
                print("L'upload del file "+stringa3SenzaApici2+" non è riuscito. Il suo IdObject non sarà inserito in tabella di appoggio"+'\n')

            #Elimino il file temporaneo
            os.remove(pathFileTemporaneo)
            time.sleep(sleep_time_selected)

        #conto quante righe ci sono nella lista filtrata
        row_count = self.contaRecord(cursor)
        print("L'upload è concluso. Mancano "+row_count+" record da processare."+'\n')

    def selectBeginDate(self):
        def printSelectedBeginDate():
            print('"{}"'.format(cal.selection_get()))
            self.beginDate = str(cal.selection_get())
            exit()
        def exit():
            top.destroy()

        top = tk.Toplevel(self.root)

        cal = Calendar(top, font="Arial 14", selectmode='day', cursor="hand1", year=2019, month=1, day=1)
        cal.pack(fill="both", expand=True)

        ttk.Button(top, text="OK", command=printSelectedBeginDate).pack()
        ttk.Button(top, text="Annulla", command=exit).pack()

    def selectEndDate(self):
        def printSelectedEndDate():
            print('"{}"'.format(cal.selection_get()))
            self.endDate = str(cal.selection_get())
            exit()
        def exit():
            top.destroy()

        top = tk.Toplevel(self.root)

        cal = Calendar(top, font="Arial 14", selectmode='day', cursor="hand1", year=2019, month=1, day=1)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=printSelectedEndDate).pack()
        ttk.Button(top, text="Annulla", command=exit).pack()    

tt = t()