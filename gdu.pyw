from functions.gdu import *



if __name__ == "__main__":
    if sis_op == "win32" or "win64":
        root = Tk()    
        root = Main(master=root)
        root.mainloop()
    else:
        messagebox.showerror("Error Fatal","¡Sistema Operativo Incompatible!")
