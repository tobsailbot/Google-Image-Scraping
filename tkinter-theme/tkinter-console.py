import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sys
import time
from threading import Thread
import sv_ttk

folder_path = ""

def redirect_stdout_to_text(widget):
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, message):
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.insert(tk.END, message)
            self.text_widget.configure(state=tk.DISABLED)
            self.text_widget.see(tk.END)

        def flush(self):
            pass

    sys.stdout = StdoutRedirector(widget)


def print_numbers(input,count,transparent, folder):
    print(input)
    print(count)
    print(transparent)
    print(folder)

def run_thread(input,count,transparent,folder):
    # Crear un hilo para ejecutar el bucle de impresión de números
    thread = Thread(target=print_numbers, args=(input, count, transparent, folder))
    # Iniciar el hilo
    thread.start()



# Crear la ventana principal
root = tk.Tk()

# Main window configuration
root.title("Google Images Downloader")
root.resizable(False, False)

main_frame = ttk.Frame(root)
main_frame.pack(pady=(15,10))


# ingresar la cadena de busqueda
label_1 = ttk.Label(main_frame, text="Search input", width=12)
label_1.grid(column=0, row=0, pady=(5,10), padx=(10,0))

entry_1 = ttk.Entry(main_frame, width=24, font=("TkDefaultFont", 10))
entry_1.grid(column=1, row=0,columnspan=3, pady=(5,10), padx=(0,10), sticky="w")

# cantidad de imagenes
label_2 = ttk.Label(main_frame, text="Images count", width=12)
label_2.grid(column=0, row=1, pady=(15,10), padx=(10,0))

entry_2 = ttk.Entry(main_frame, width=24, font=("TkDefaultFont", 10))
entry_2.insert(0, "5")  # Insertar el valor predeterminado "5"
entry_2.grid(column=1, row=1,columnspan=3, pady=(15,10), sticky="w")

# Crear un widget Checkbutton para activar/desactivar el modo transparente
label_3 = ttk.Label(main_frame, text="Transparent", width=12)
label_3.grid(column=0, row=2, pady=(11,10), padx=(10,0))

CheckVar = tk.IntVar(0)
check_button = ttk.Checkbutton(main_frame, variable=CheckVar)
check_button.grid(column=1, row=2, pady=(11,10), sticky="w")

label_4 = ttk.Label(main_frame, text="Output folder", width=12)
label_4.grid(column=0, row=3, pady=(11,15), padx=(10,0))


# Variable para almacenar el texto actualizado
folder_output = tk.StringVar()
folder_output.set("../")  # Valor inicial de la variable

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()  # Abre el diálogo de selección de carpeta
    if folder_path:
        folder = folder_path.split("/")[-1] 
        folder_output.set('../' + folder)
        print('--------------')
        print("Output folder: ", folder_path)


# Crear un Button para seleccionar una carpeta
browse_folder = ttk.Button(main_frame, text="Browse", command=select_folder)
browse_folder.grid(column=1, row=3, pady=(11,15), sticky="w")

label_4 = ttk.Label(main_frame, textvariable=folder_output, width=12)
label_4.grid(column=2, row=3, pady=(11,15), padx=(0,0), sticky="w")


separator = ttk.Separator(main_frame, orient="horizontal")
separator.grid(column=0, row=4, columnspan=3, sticky="ew", pady=10, padx=(10,0))


def run_thread_with_params():
    # Obtener los valores de los widgets o variables necesarios
    input = entry_1.get()
    count = int(entry_2.get())
    transparent = CheckVar.get()
    global folder_path
    # Llamar a la función run_thread con los parámetros
    if input and count > 0:
        run_thread(input, count, transparent, folder_path)


button = ttk.Button(main_frame, text="Download Images", command=run_thread_with_params, style="Accent.TButton", padding=(10, 5))
button.grid(column=0, row=5, columnspan=3, pady=10)


# Crear un widget Text para mostrar la salida de la consola
text_widget = tk.Text(main_frame, width=40, height=7, font=("Consolas", 10), wrap=tk.WORD, blockcursor=True, state=tk.DISABLED, highlightcolor="gray25", fg="gray75")
text_widget.configure(state=tk.NORMAL)
text_widget.insert(tk.END, 'Download status... \n')
text_widget.configure(state=tk.DISABLED)
text_widget.see(tk.END)
text_widget.grid(column=0, row=6, columnspan=3, sticky="ew", pady=(10,5), padx=(10,0))







# Set dark theme
sv_ttk.set_theme("dark")

# Redireccionar la salida estándar a la widget Text
redirect_stdout_to_text(text_widget)



# Iniciar el bucle principal de Tkinter
root.mainloop()
