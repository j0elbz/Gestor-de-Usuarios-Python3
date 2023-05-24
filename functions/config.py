from functions.instalar_librerias import encontrar_requirements
import subprocess
import sys

sis_op      = sys.platform
try:
    from tkinter.font import  Font
    from tkinter import ttk
    from tkinter.constants import *
    from tkinter import Frame
    from tkinter import Tk
    from tkinter import Button
    from tkinter import PhotoImage
    from tkinter import Label
    from tkinter import StringVar
    from tkinter import Entry, Toplevel
    from tkinter import Scrollbar
    from tkinter.messagebox import showerror


    from PIL import Image,ImageTk

    from tkinter.messagebox import showinfo, askyesno
    from tkinter import messagebox

    from datetime import date
    from datetime import datetime
    import time

    import sqlite3
    from sqlite3 import OperationalError

    import threading

    REFRESH_CLOCK = 300 

    REFRESH_TREE  = 10


    background_color    = "#26687a"
    font_color          = "#FFFFFF"
    font_config_hour    = ("consolas 15")
    font_config_title   = ("consolas") 
    font_text           = ("consolas 12")

    color_background_treeview = "#4D4C5C"
    color_font_treeview       = "#26687a" 

    path_image        = "images/"
    path_new_image    = path_image + "new.png"
    path_delete_image = path_image + "recyfull.png"
    path_config_image = path_image + "config.png"
    path_exit_image   = path_image + "close.png"
    path_pay_image    = path_image + "payout.png"
    path_ico_gdu      = path_image + "ico_gdu.ico"
    path_search_image = path_image + "search.png"

    conection = sqlite3.connect("database/users_db.db",check_same_thread=False)
    miCursor=conection.cursor()

    

except ModuleNotFoundError:
    messagebox.showerror('Error', 'No se encontraron los complementos necesarios!')
    instalar_complementos = messagebox.askokcancel(message="¿Los desea instalar?", title="Instalacion de complementos")
    requeriments = encontrar_requirements()

    if instalar_complementos == True:
        if requeriments == True:
            if sis_op == "win32" or "win64":

                subprocess.run(['pip','install', '-r', 'requirements.txt'])
                messagebox.showinfo(message='la instalacion finalizo satisfactoriamente! ', title='Instalacion de complementos')
            
            elif sis_op == "linux2":
                subprocess.run(['pip3','install', '-r', 'requirements.txt'])
                messagebox.showinfo(message='la instalacion finalizo satisfactoriamente! ', title='Instalacion de complementos')
    
    
    if requeriments == False:
        messagebox.showerror('Error', 'No se encontro el archivo requirements.txt!')
        messagebox.showinfo(message='El archivo requirements.txt fue creado! ', title='Instalacion de complementos')
        messagebox.showinfo(message='Vuelva a iniciar! ', title='Instalacion de complementos')


