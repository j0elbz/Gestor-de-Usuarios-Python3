from functions.config import *

def compare_dates(y_o,m_o,d_o):
    date = datetime.now()
    month = date.month
    day   = date.day
    year  = date.year

    date_input =  datetime(year,month, day)
    date_output = datetime(y_o, m_o, d_o)
    if date_input >= date_output:
        return True
    else:
        return False

def get_date():
    time_info = []
    date = datetime.now()
    current_date = date.date()
    time = date.time().strftime("%H:%M")
    time_info.append(current_date)
    time_info.append(time)
    return time_info

def payment() -> dict:
    date_payment = {"payment":"","expiration":""}
    today = date.today()

    month  = today.month
    day  = today.day
    year = today.year 
    payment_date   = str(day) + "/" + str(month) + "/" + str(year)
    
    expiration_day   = day
    expiration_month = month
    expiration_year  = year


    if expiration_month >= 12:
        expiration_month = 1 
        expiration_year  = expiration_year + 1

    else:
        expiration_month = expiration_month + 1

    expiration_date = str(expiration_day) + "/" + str(expiration_month) + "/" + str(expiration_year) 
   

    date_payment["payment"]    =  payment_date
    date_payment["expiration"] = expiration_date 
        
    return date_payment


def autoincrement_id() -> int:
    try:
        id_qurry = miCursor.execute("select max(id) from users")
        id = id_qurry.fetchone()
        id = id[0]

        id_max = id + 1
    except TypeError:
        id_max = 1
    return id_max

def check_ci(ci) -> bool:
    ci = str(ci)
    length = len(ci)
    if length == 8:
        if  ci.isdigit() == True:
            return True
        else:
            return False
    else:
        return False

def get_display_size():
    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    y = root.winfo_screenheight()
    x = root.winfo_screenwidth()
    root.destroy()
    return y, x

def check_ci_exists():
    ci_check_query = "select ci from users"
    ci_check_run   = miCursor.execute(ci_check_query)
    ci_check       = ci_check_run.fetchall()
    cis_list = []
    for cis in ci_check:
        for ci in cis:
            cis_list.append(ci)
    return cis_list 

def debugging_msg(msg):
    print(msg)
    return True


def system_log(msg):
    time_info = get_date()
    file_log_path = "log/system_log.txt"
    try:
        msg_structure = f"{time_info[0]} {time_info[1]} {msg}"
        file_log = open(file_log_path,"a")
        file_log.write(msg_structure + "\n")

    except FileNotFoundError:
        file_log = open(file_log_path,"w")

def check_string(ci):
    for caracter in ci:
        if caracter.isalpha():
            return True
    
    return False
