try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

from tkcalendar import Calendar, DateEntry

def dataInizio():
    top = tk.Toplevel(root)

    ttk.Label(top, text='Scegli data inizio').pack(padx=100, pady=10)

    cal = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)

def dataFine():
    top = tk.Toplevel(root)

    ttk.Label(top, text='Scegli data fine').pack(padx=100, pady=10)

    cal = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    

root = tk.Tk()
root.title("Carica DDTC")     # Add a title
s = ttk.Style(root)
s.theme_use('clam')


ttk.Button(root, text='Data Inizio', command=dataInizio).pack(padx=50, pady=10)
ttk.Button(root, text='Data Fine', command=dataFine).pack(padx=90, pady=10)

root.mainloop()