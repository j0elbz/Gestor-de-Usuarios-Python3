from functions.gdu import *



if __name__ == "__main__":
    if sis_op == "Windows":
        root = Tk()    
        root = Main(master=root)
        root.mainloop()
    else:
        messagebox.showerror("Error Fatal","¡Sistema Operativo Incompatible!")
