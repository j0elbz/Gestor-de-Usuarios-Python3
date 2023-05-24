def encontrar_requirements() -> bool:
    try:
        librerias_requirements = ["icmplib==3.0.3\n","Pillow==9.2.0\n","PyAutoGUI==0.9.53\n",
        "PyGetWindow==0.0.9\n","PyMsgBox==1.0.9\n","pyperclip==1.8.2\n",
        "PyRect==0.2.0\n","PyScreeze==0.1.28\n","pytweening==1.0.4\n",
        "pywin32==304\n","scapy==2.4.5\n","setuptools==63.2.0\n"]
        
        requirements_ruta = "requirements.txt"
        requirements_archivo = open(requirements_ruta,"r")
        
        return True
    
    except FileNotFoundError:
        requirements_archivo = open(requirements_ruta,"w")
        
        for libreria in librerias_requirements:
            requirements_archivo.write(libreria) 
        
        return False
