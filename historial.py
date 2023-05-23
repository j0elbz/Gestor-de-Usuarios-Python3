import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox

def open_file():
    file_path = "log/system_log.txt"
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text.delete(1.0, tk.END)
            text.insert(tk.END, content)

def search_word():
    keyword = entry.get()
    if keyword:
        content = text.get(1.0, tk.END)
        lines = content.split("\n")
        matching_lines = []
        for line in lines:
            if keyword.lower() in line.lower():
                matching_lines.append(line)
        if matching_lines:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "\n".join(matching_lines))
        else:
            messagebox.showinfo("Sin coincidencias", "No se encontraron coincidencias.")
            result_text.delete(1.0, tk.END)
    else:
        messagebox.showinfo("Palabra clave vacía", "Ingresa una palabra para buscar.")

# Crear la ventana principal
window = tk.Tk()
window.title("Visor de Registros")

window.iconbitmap("images/search_log.ico")

# Crear un widget de Texto para mostrar el contenido del archivo
text = scrolledtext.ScrolledText(window)
text.pack()

# Crear un botón para abrir el archivo
open_button = tk.Button(window, text="Cargar Registros", command=open_file)
open_button.pack()

# Crear una etiqueta y un campo de entrada para buscar palabras
search_label = tk.Label(window, text="Buscar Registros:")
search_label.pack()
entry = tk.Entry(window)
entry.pack()

# Crear un botón para buscar la palabra
search_button = tk.Button(window, text="Buscar", command=search_word)
search_button.pack()

# Crear un widget de Texto para mostrar los resultados de búsqueda
result_text = scrolledtext.ScrolledText(window)
result_text.pack()

# Ejecutar el bucle principal de la ventana
window.mainloop()