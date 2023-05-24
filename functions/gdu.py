from functions.config import *
from functions.functions import *

class Main(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.__root_config()
        self.__create_treeview()
        self.__create_widgets()
        self.__time()

        self.stop_threads = False
        self.t = threading.Thread(target=self.__thread)
        self.t.start()

    def __root_config(self):
        self.master.configure(bg=background_color)
        self.master.geometry("900x350+0+200")
        self.master.resizable(False,False)
        self.master.title("GDU")
        self.master.iconbitmap(path_ico_gdu)
        self.master.protocol("WM_DELETE_WINDOW", self.__stop_thread)
        
    def __stop_thread(self):
        self.stop_threads = True
        self.master.destroy()

    def __create_treeview(self):
#       debugging_msg("FUNCION : Crear Treeview - Funcionando")
        users_lbl = Label(master=self.master,text="Clientes Al dia",font=font_config_title,fg=font_color,bg=background_color)
        users_lbl.place(x=240,y=10)

        expired_memberships = Label(master=self.master,text="Cuotas Vencidas",font=font_config_title,fg=font_color,bg=background_color)
        expired_memberships.place(x=660,y=10)

        frame_treeview = Frame(master=self.master,bg=background_color)
        frame_treeview.grid(row=0,column=2,padx=(10,100),pady=35)
        
        self.users         = self.__get_all_users()

        self.expired_users = self.__load_expired_partners()

        total_partners = len(self.users)
        total_expired_partners = len(self.expired_users)

        columns_users   = ("Ci","Nombre", "Apellido","Pago","Vencimiento")
        columns_expired = ("Ci","Dia del Vencimiento")

        self.tree_users = ttk.Treeview(frame_treeview, columns=columns_users, show='headings')

        self.expired_users_tree = ttk.Treeview(frame_treeview,columns=columns_expired,show="headings")
        self.check_scroll_users = False


        self.tree_users.column(f"#5",width=130,anchor=CENTER)

        
        for column_heading in range(0,5):
            self.tree_users.column(f"#{column_heading}",width=90,anchor=CENTER)
            self.tree_users.heading(columns_users[column_heading],text=columns_users[column_heading])

        for user in self.users:
            self.tree_users.insert('',END, values=user)
        
        for expired_user in self.expired_users:
            self.expired_users_tree.insert('',END, values=expired_user)

        if total_partners >= 11:
            scroll_users = Scrollbar(master=self.master, command=self.tree_users.yview, width=15)
            scroll_users.place(in_=self.tree_users, relx=1, relheight=1, bordermode="outside")
        
        if total_expired_partners >= 11:
            scrollbar_expired = Scrollbar(master=self.master, command=self.expired_users_tree.yview, width=15)
            scrollbar_expired.place(in_=self.expired_users_tree,relx=1,relheight=1,bordermode="outside")
            self.check_scroll_users = True


        self.expired_users_tree.column(f"#1",width=130,anchor=CENTER)
        self.expired_users_tree.column(f"#2",width=130,anchor=CENTER)
        self.expired_users_tree.heading("Ci",text="Ci")
        self.expired_users_tree.heading("Dia del Vencimiento",text="Dia del Vencimiento")

        self.tree_users.grid(row=0, column=0,pady=(20,0), sticky='nsew')
        self.expired_users_tree.grid(row=0, column=2,pady=(20,0),padx=40, sticky='nsew')

        self.tree_users.bind("<Button-1>",self.__get_ci_partners)
        self.expired_users_tree.bind("<Double-Button-1>",self.__get_ci_partners_expired)
        self.master.bind("<Button-1>",self.__deselect)

    def __get_ci_partners(self, event):
        global ci
        try:
            item = self.tree_users.selection()
            for i in item:
                ci = self.tree_users.item(i, "values")[0]
        except NameError or ValueError:
            messagebox.showerror("Error","Primero debe seleccionar un cliente! (Doble Click)")
    
    def __get_ci_partners_expired(self, event):
        global ci_expired
        try:
            item = self.expired_users_tree.selection()
            for i in item:
                ci_expired = self.expired_users_tree.item(i, "values")[0]
        except NameError or ValueError:
            messagebox.showerror("Error","Primero debe seleccionar un cliente! (Doble Click)")

    def __delete_partner(self):
        try:
            partner = self.__get_partner()
            if ci:
                if askyesno(message=f"¿Seguro que lo desea eliminar?", title="Eliminar Cliente") == True:
                    query = f"DELETE FROM users WHERE ci = {ci}"
                    conection.execute(query)
                    conection.commit()
                    system_log(f"Se elimino un usuario  {partner[3]} ({partner[1]} {partner[2]})")
                    self.__create_treeview()
                else:
                    pass
        except NameError or ValueError:
            messagebox.showerror("Error","Primero debe seleccionar un cliente! (Doble Click)")
                    
    def __show_action(self, event):
        if event.widget == self.boton_new:        
            self.actions['text'] = 'Nuevo'
            self.actions.place(x=(15),y=10)
        
            
        elif event.widget == self.boton_config:
            self.actions['text'] = 'Modificar'
            self.actions.place(x=(10),y=10)
            
        elif event.widget == self.boton_delete:
            self.actions['text'] = 'Eliminar'
            self.actions.place(x=(13),y=10)

        elif event.widget == self.master:
            self.actions['text'] = 'Acciones'
            self.actions.place(x=(9),y=10)
            
        
        elif event.widget == self.boton_exit:
            self.actions['text'] = "Salir"
            self.actions.place(x=(19),y=(10))

        elif event.widget == self.boton_pay:
            self.actions['text'] = "Pagar"
            self.actions.place(x=(15),y=(10))

        elif event.widget == self.search_btn:
            self.actions['text'] = "Buscar"
            self.actions.place(x=(13),y=(10))
    
    def __deselect(self,event):
        if event.widget == self.master:
            for item in self.tree_users.selection():
                    self.tree_users.selection_remove(item)

    def __create_widgets(self):   
#       debugging_msg("FUNCION : Widgets - Funcionando")
        self.actions = Label(master=self.master,text="Acciones",font=("arial",10),fg=font_color,bg=background_color)
        self.actions.place(x=(9),y=10)

        self.master.bind("<Motion>",self.__show_action)

        self.img_new = Image.open(path_new_image)
        self.img_new = self.img_new.resize((45, 45), Image.ANTIALIAS) 
        self.img_new = ImageTk.PhotoImage(self.img_new)

        self.img_pay = Image.open(path_pay_image)
        self.img_pay = self.img_pay.resize((45,45), Image.ANTIALIAS)
        self.img_pay = ImageTk.PhotoImage(self.img_pay)

        self.img_delete = Image.open(path_delete_image)
        self.img_delete = self.img_delete.resize((45, 45), Image.ANTIALIAS) 
        self.img_delete = ImageTk.PhotoImage(self.img_delete)

        self.img_config = Image.open(path_config_image)
        self.img_config = self.img_config.resize((45, 45), Image.ANTIALIAS) 
        self.img_config = ImageTk.PhotoImage(self.img_config)

        self.img_search = Image.open(path_search_image)
        self.img_search = self.img_search.resize((25,25), Image.ANTIALIAS)
        self.img_search = ImageTk.PhotoImage(self.img_search)

        self.img_exit = Image.open(path_exit_image)
        self.img_exit = self.img_exit.resize((35, 35), Image.ANTIALIAS) 
        self.img_exit = ImageTk.PhotoImage(self.img_exit)

        self.frame_buttons = Frame(master=self.master,bg=background_color)
        self.frame_buttons.grid(row=0,column=0,padx=(0,0),pady=(55,0),sticky=NW)
        

        self.boton_new = Button(self.frame_buttons,bg=background_color,cursor="hand2", image=self.img_new,relief='flat',borderwidth=0,activebackground=background_color,bd=0,command=self.__add_partner)
        self.boton_new.image = self.img_new
        self.boton_new.grid(row=0, column=0,padx=10, pady=0)
        self.boton_new.bind("<Motion>", self.__show_action)

        self.boton_config = Button(self.frame_buttons,bg=background_color,cursor="hand2", image=self.img_config,relief='flat',borderwidth=0,activebackground=background_color,bd=0,command=self.__modify_partners)
        self.boton_config.image = self.img_config
        self.boton_config.grid(row=1, column=0,padx=10, pady=10)
        self.boton_config.bind("<Motion>", self.__show_action)

        self.boton_delete = Button(self.frame_buttons,bg=background_color,cursor="hand2", image=self.img_delete,relief='flat',borderwidth=0,activebackground=background_color,bd=0,command=self.__delete_partner)
        self.boton_delete.image = self.img_delete
        self.boton_delete.grid(row=2, column=0,pady=5)
        self.boton_delete.bind("<Motion>", self.__show_action)

        self.boton_pay = Button(self.frame_buttons,bg=background_color,cursor="hand2", image=self.img_pay,relief='flat',borderwidth=0,activebackground=background_color,bd=0,command=lambda :(self.__pay_membership("p_m")))
        self.boton_pay.image = self.img_pay
        self.boton_pay.grid(row=3, column=0,padx=10, pady=10)
        self.boton_pay.bind("<Motion>", self.__show_action)

        self.search_lbl   = Label(master=self.master,text="Busqueda por Ci",background=background_color,fg=font_color)
        self.search_lbl.place(x=280,y=285)

        self.search_btn   = Button(master=self.master,bg=background_color,cursor="hand2", image=self.img_search,relief='flat',borderwidth=0,activebackground=background_color,bd=0,command=self.__view_partner)
        self.search_btn.image = self.img_search
        self.search_btn.place(x=395,y=306)


        self.search_entry = Entry(master=self.master,bg='white',justify='center')
        self.search_entry.place(x=262,y=310)
    

        self.boton_exit = Button(self.master,bg=background_color,cursor="hand2", image=self.img_exit,relief='flat',borderwidth=0,activebackground=background_color,bd=0,command=self.__stop_thread)
        self.boton_exit.image = self.img_delete
        self.boton_exit.place(x=10,y=300)
        self.boton_exit.bind("<Motion>", self.__show_action)

    def __time(self):
        def get_current_time():
            return datetime.now().strftime("%H:%M:%S")

        def refresh_clock():
            hour_now.set(get_current_time())
            self.master.after(REFRESH_CLOCK, refresh_clock)

        
        hour_now = StringVar(self.master, value=get_current_time())
        self.hour = Label(self.master, textvariable=hour_now, bg=background_color,fg=font_color,font=font_config_hour)
        if  self.check_scroll_users == True:
            self.hour.place(x=800,y=295)
        else:
            self.hour.place(x=780,y=305)

        refresh_clock()

    def __msg_accept(self,msg,action):
        check_add = askyesno(message=f"{msg} {self.name_entry.get()} {self.last_name_entry.get()}", title="Nuevo cliente")
        if action == "A":
            if check_add == True:
                self.__add_query() 
                self.__refresh_users()
                
                self.boton_new.grid()
            else:
                pass
        elif action == "M":
            if check_add == True:
                self.__modify_query() 
                
                self.boton_new.grid()
            else:
                pass

    def __on_quit(self,action):  
        if action == "A":
            self.exitFlag_add  = True
            self.top_add.destroy()
            if self.exitFlag_add  == True:
                self.boton_new.grid(row=0, column=0,padx=10, pady=0)
        elif action == "M":
            self.exitFlag_mod  = True
            self.top_mod.destroy()
            if self.exitFlag_mod  == True:
                self.boton_config.grid(row=1, column=0,padx=10, pady=10)
        elif action == "V":
            self.exitFlag_view  = True
            self.top_view.destroy()
            if self.exitFlag_view == True:
                self.search_entry['state'] = NORMAL
                self.search_btn.place(x=395,y=306)
           
        

    def __add_partner(self):
#       debugging_msg("FUNCION : Agregar - Funcionando")
        self.exitFlag_add = False

        self.x_position_top = self.master.winfo_x()

        self.x_position_screen = get_display_size()[1]
        self.x_position_screen = self.x_position_screen 
        self.x_position_screen = round(self.x_position_screen)

        self.y_position_top = self.master.winfo_y()
        self.x_position_top = self.x_position_top + 960
        

        self.top_add = Toplevel(master=self.master)
        self.top_add.configure(background=background_color)
        self.top_add.geometry(f"220x210+{self.x_position_top}+{self.y_position_top}")
        self.top_add.protocol("WM_DELETE_WINDOW",lambda :self.__on_quit("A"))
        self.top_add.resizable(False,False)

        self.boton_new.grid_forget()

        self.payment_date = payment()
        self.payment = self.payment_date['payment']
        

        self.frame_entrys = Frame(master=self.top_add,background=background_color)
        self.frame_entrys.grid(row=0,column=0)

        self.ci_label  = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color, text="CI")
        self.ci_label.grid(row=0,column=0,padx=(0,40))

        self.ci_entry = Entry(master=self.frame_entrys,width=15)
        self.ci_entry.grid(row=0,column=1,sticky=E,padx=(0,10))
        
        self.name_label  = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color,text="Nombre")
        self.name_label.grid(row=1,column=0,padx=(0,40))

        self.name_entry = Entry(master=self.frame_entrys,width=15)
        self.name_entry.grid(row=1,column=1,pady=30,sticky=E,padx=(12,10))

        self.last_name_label = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color,text="Apellido")
        self.last_name_label.grid(row=2,column=0,padx=(0,30))
        

        self.last_name_entry = Entry(master=self.frame_entrys,width=15)
        self.last_name_entry.grid(row=2,column=1,sticky=E,padx=(0,10))

        self.payment_day = Label(master=self.top_add,text=f"Pago {self.payment}",fg="white",font=font_text,background=background_color)
        self.payment_day.place(x=40,y=135)

        self.accept_btn = Button(master=self.top_add,text="Aceptar",fg="white",background=background_color,command=lambda:(self.__msg_accept("Quiere agregar al usuario ","A")))
        self.accept_btn.place(x=50,y=170)

        self.cancel_btn = Button(master=self.top_add,text="Cancelar",fg="white",background=background_color,command=lambda:(self.__on_quit("A")))
        self.cancel_btn.place(x=110,y=170)

    def __modify_partners(self):
        self.exitFlag_mod  = False

        self.x_position_top = self.master.winfo_x()

        self.x_position_screen = get_display_size()[1]
        self.x_position_screen = self.x_position_screen 
        self.x_position_screen = round(self.x_position_screen)

        self.y_position_top = self.master.winfo_y()
        self.x_position_top = self.x_position_top + 960
        
        try:
#            debugging_msg("FUNCION : Modificar - Funcionando")
            partner = self.__get_partner()
            self.ci      = partner[3]
            self.name    = partner[1]
            self.surname = partner[2]
            self.ci_aux  = self.ci 
            self.name_aux = self.name 
            self.surname_aux = self.surname 


            self.top_mod = Toplevel(master=self.master)
            self.top_mod.configure(background=background_color)
            self.top_mod.geometry(f"210x210+{self.x_position_top}+{self.y_position_top}")
            self.top_mod.protocol("WM_DELETE_WINDOW", lambda:(self.__on_quit("M")))
            self.top_mod.resizable(False,False)

            self.boton_config.grid_forget()

            self.payment_date = payment()
            self.payment = self.payment_date['payment']
            

            self.frame_entrys = Frame(master=self.top_mod,background=background_color)
            self.frame_entrys.grid(row=0,column=0)

            self.ci_label  = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color, text="CI")
            self.ci_label.grid(row=0,column=0,padx=(0,40))

            self.ci_entry = Entry(master=self.frame_entrys,width=15)
            self.ci_entry.grid(row=0,column=1,sticky=E,padx=(0,10))
            self.ci_entry.insert(0,self.ci)

            
            self.name_label  = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color,text="Nombre")
            self.name_label.grid(row=1,column=0,padx=(0,30))
            

            self.name_entry = Entry(master=self.frame_entrys,width=15)
            self.name_entry.grid(row=1,column=1,pady=30,sticky=E,padx=(12,10))
            self.name_entry.insert(0,self.name)

            self.last_name_label = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color,text="Apellido")
            self.last_name_label.grid(row=2,column=0,padx=(0,20))
            

            self.last_name_entry = Entry(master=self.frame_entrys,width=15)
            self.last_name_entry.grid(row=2,column=1,sticky=E,padx=(0,10))
            self.last_name_entry.insert(0,self.surname)

            self.accept_btn = Button(master=self.top_mod,text="Aceptar",fg="white",background=background_color,command=lambda :(self.__msg_accept("Modificar ","M")))
            self.accept_btn.place(x=40,y=170)

            self.cancel_btn = Button(master=self.top_mod,text="Cancelar",fg="white",background=background_color,command=lambda :(self.__on_quit("M")))
            self.cancel_btn.place(x=100,y=170)
        except TypeError:
            pass

    def __get_view_user(self):
        try:
            self.ci_entry_v = self.search_entry.get()
            
            
            print("La cedula es valida > ",self.ci_entry_v)
            
            if(check_string(self.ci_entry_v)):
                messagebox.showerror("Error","Usuario no encontrado!")
                self.search_entry['state'] = NORMAL
            else:
                query = f"select * from users where ci = {self.ci_entry_v}"
                partner_run = miCursor.execute(query)
                partners    = partner_run.fetchall()
                for partner in partners:
                    pass
                system_log(f"Se consulto un usuario  {partner[3]} ({partner[1]} {partner[2]})")
                return partner

        except NameError or OperationalError:
            messagebox.showerror("Error","Usuario no encontrado!")
            self.search_entry['state'] = NORMAL

    def __view_partner(self):
        self.exitFlag_view  = False
        self.search_entry['state'] = DISABLED

        self.x_position_top = self.master.winfo_x()

        self.x_position_screen = get_display_size()[1]
        self.x_position_screen = self.x_position_screen 
        self.x_position_screen = round(self.x_position_screen)

        self.y_position_top = self.master.winfo_y()
        self.x_position_top = self.x_position_top + 960
        
        try:
#            debugging_msg("FUNCION : Modificar - Funcionando")
            partner = self.__get_view_user()
            self.ci      = partner[3]
            self.name    = partner[1]
            self.surname = partner[2]
            self.state   = partner[6]

            self.top_view = Toplevel(master=self.master)
            self.top_view.configure(background=background_color)
            self.top_view.geometry(f"210x210+{self.x_position_top}+{self.y_position_top}")
            self.top_view.protocol("WM_DELETE_WINDOW", lambda:(self.__on_quit("V")))
            self.top_view.resizable(False,False)

            #self.boton_config.grid_forget()

            self.payment_date = payment()
            self.payment = self.payment_date['payment']
            

            self.frame_entrys = Frame(master=self.top_view,background=background_color)
            self.frame_entrys.grid(row=0,column=0)

            self.ci_label  = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color, text="CI")
            self.ci_label.grid(row=0,column=0,padx=(0,40))

            self.ci_entry = Entry(master=self.frame_entrys,width=15)
            self.ci_entry.grid(row=0,column=1,sticky=E,padx=(0,10))
            self.ci_entry.insert(0,self.ci)
            self.ci_entry['state'] = DISABLED
            
            self.name_label  = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color,text="Nombre")
            self.name_label.grid(row=1,column=0,padx=(0,30))
            

            self.name_entry = Entry(master=self.frame_entrys,width=15)
            self.name_entry.grid(row=1,column=1,pady=30,sticky=E,padx=(12,10))
            self.name_entry.insert(0,self.name)
            self.name_entry['state'] = DISABLED

            self.last_name_label = Label(master=self.frame_entrys,font=font_text,fg="white",background=background_color,text="Apellido")
            self.last_name_label.grid(row=2,column=0,padx=(0,20))
            

            self.last_name_entry = Entry(master=self.frame_entrys,width=15)
            self.last_name_entry.grid(row=2,column=1,sticky=E,padx=(0,10))
            self.last_name_entry.insert(0,self.surname)
            self.last_name_entry['state'] = DISABLED

            self.search_btn.place_forget()

            self.payment_day = Label(master=self.top_view,text=f"CUOTA {self.state}",fg="white",font=font_text,background=background_color)
            self.payment_day.place(x=50,y=135)
        

            self.cancel_btn = Button(master=self.top_view,text="Volver",fg="white",background=background_color,command=lambda :(self.__on_quit("V")))
            self.cancel_btn.place(x=85,y=170)

            if self.state == "AL DIA":
                pass
            else:
                self.pay_btn = Button(master=self.top_view,text="Pagar",fg="white",background=background_color,command=lambda :(self.__pay_membership("p_v")))
                self.pay_btn.place(x=60,y=170)
                self.cancel_btn.place(x=110,y=170)

        except TypeError:
            pass


    def __add_query(self):
#        debugging_msg("FUNCION : Agregar - Funcionando")
        id             = autoincrement_id()
        ci             = self.ci_entry.get()
        ci_check       = check_ci_exists()
        if int(ci) in ci_check:
            messagebox.showerror("Error","Este usuario ya Existe!")
        else:
            name           = self.name_entry.get().lower().capitalize()
            surname        = self.last_name_entry.get().lower().capitalize()
            ci_valid       = check_ci(ci)
    
            if ci_valid == True: 
                if len(name) >= 1 and len(surname) >= 1:
                    payment_day    = payment()['payment']
                    expiration_day = payment()['expiration']
                    path_img       = "/"
                    query = f"insert into users(id,name,surname,ci,payment_date,expiration_date,state,path_image) VALUES('{id}','{name}','{surname}',{ci},'{payment_day}','{expiration_day}','AL DIA','{path_img}')"
                    miCursor.execute(query)
                    conection.commit()
                    system_log(f"Un usuario fue creado {ci} ({name} {surname})")
                    self.__on_quit("A")
                else:
                    messagebox.showerror("Error","Nombre o Apellido Invalido!")
                
            else:
                messagebox.showerror("Error","Ci invalida!")

    def __modify_query(self):
        ci = self.ci_entry.get()
        name = self.name_entry.get().lower().capitalize()
        surname = self.last_name_entry.get().lower().capitalize()
        query = f"update users set name='{name}', surname='{surname}',ci='{ci}' where ci={ci}"
        miCursor.execute(query)
        conection.commit()
        system_log(f"Se modifico el usuario {ci} de ({name} {surname}) a ({self.name_aux} {self.surname_aux})")
        self.__refresh_users()
        self.__on_quit("M")
        

    def __get_partner(self):
#        debugging_msg("FUNCION : Obtener Usuario - Funcionando")

        try:
            query = f"select * from users where ci = {ci}"
            partner_run = miCursor.execute(query)
            partners    = partner_run.fetchall()
            for partner in partners:
                pass
            return partner
        except NameError:
            messagebox.showerror("Error","Primero debe seleccionar un usuario! (Doble Click)")
    
    def __load_expired_partners(self):
#       debugging_msg("FUNCION : Cargar Expirados - funcionando")

        tuple_expired = []
        query = "select ci,payment_date,expiration_date from users"
        expired_user_run = miCursor.execute(query)
        expired_user_get  = expired_user_run.fetchall()
        for expired_user in expired_user_get:         
            date_expired = str(expired_user[2])
            date_expired = date_expired.split("/")
            day_expired          = int(date_expired[0])
            month_expired        = int(date_expired[1])
            year_expired         = int(date_expired[2])
            if compare_dates(year_expired,month_expired,day_expired) == True:
                ci           = expired_user[0]
                update_state_query = f"update users set state = 'VENCIDA' where ci = {ci}"
                update_state_run   = miCursor.execute(update_state_query)
                tuple_expired.append(expired_user)

            conection.commit()
        return tuple_expired
    
    def __get_all_users(self):
        datos = miCursor.execute("select ci,name,surname,payment_date,expiration_date from users")
        self.users = datos.fetchall()
        return self.users

    def __refresh_users(self):
#       debugging_msg("FUNCION : Refrescar Tree View - funcionando")

        self.tree_users.delete(*self.tree_users.get_children())

        users = self.__get_all_users()
        for row in users:
            self.tree_users.insert('','end', values = (row[0], row[1], row[2], row[3], row[4]))

    def __refesh_users_expired(self):        
        self.expired_users_tree.delete(*self.expired_users_tree.get_children())

        users_expired = self.__load_expired_partners()
        for row in users_expired:
            self.expired_users_tree.insert('','end', values = (row[0], row[1]))


    def __check_state(self,p_op):
        try:
            global ci_expired
            if p_op == "p_v":
                self.aux_ci_entry = self.ci_entry.get() 
                if self.aux_ci_entry:
                    ci_expired = self.aux_ci_entry 
     

            state_query = f"select state from users where ci = {ci_expired}"
            state_query_run = miCursor.execute(state_query)
            states           = state_query_run.fetchone()
            for state in states:
                pass
            return state
        except NameError:
            messagebox.showerror("Error","Primero debe seleccionar un cliente! (Doble Click)")

    def __pay_membership(self,p):
#       debugging_msg("FUNCION : Pago - Funcionando")
        
        try:
            check_state = self.__check_state(p)
            
            if check_state == "VENCIDA":
                system_log(f"Se pago una cuota del usuario {ci_expired}")
                payment_day    = payment()['payment']
                expiration_day = payment()['expiration']
                pay_query = f"update users set payment_date = '{payment_day}', expiration_date = '{expiration_day}', state = 'AL DIA' where ci = {ci_expired}"
                check_pay = messagebox.askquestion("Pago","Quiere pagar esta cuota?")
                if check_pay == 'yes':
                    pay_query_run = miCursor.execute(pay_query)
                    conection.commit()
                    showinfo("Exito!",f"Cuota de {ci_expired} al dia!")
                    
                        
                    self.__refesh_users_expired()
                    self.__refresh_users()

                    self.search_entry['state'] = NORMAL
                    self.search_btn.place(x=395,y=306)
                    self.top_view.destroy()
                    
            if check_state == "AL DIA":
                messagebox.showwarning("Alerta","Este usuario esta al dia!")
                
        except AttributeError or NameError:
            pass

    def __thread(self):
#       debugging_msg("FUNCION : Thread - Funcionando")
        while True:
            self.stop_threads = False
            self.__refresh_users()
            self.__refesh_users_expired()

            time.sleep(REFRESH_TREE)
            if self.stop_threads == True:
                break