import tkinter as tk
from tkinter import ttk
import sys
import time
from threading import Thread
import sv_ttk

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

x = 0
def print_numbers():
    global x  # Declarar la variable x como global
    for i in range(1, 11):
        x = x + 1
        print(x)
        time.sleep(0.5)

def run_thread():
    # Crear un hilo para ejecutar el bucle de impresión de números
    thread = Thread(target=print_numbers)
    # Iniciar el hilo
    thread.start()

# Crear la ventana principal
root = tk.Tk()
# Main window configuration
root.title("Google Images Downloader")
root.resizable(False, False)

main_frame = ttk.Frame(root)
main_frame.pack(pady=(15,15))


# ingresar la cadena de busqueda
label_1 = ttk.Label(main_frame, text="Search input", width=12)
label_1.grid(column=0, row=0, pady=(10,10), padx=(10,0))

entry_1 = ttk.Entry(main_frame, width=24, font=("TkDefaultFont", 10))
entry_1.grid(column=1, row=0,columnspan=3, pady=(10,10), padx=(0,10), sticky="w")

# cantidad de imagenes
label_2 = ttk.Label(main_frame, text="Images count", width=12)
label_2.grid(column=0, row=1, pady=(15,10), padx=(10,0))

entry_1 = ttk.Entry(main_frame, width=24, font=("TkDefaultFont", 10))
entry_1.grid(column=1, row=1,columnspan=3, pady=(15,10), sticky="w")

# Crear un widget Checkbutton para activar/desactivar el modo transparente
label_3 = ttk.Label(main_frame, text="Transparent", width=12)
label_3.grid(column=0, row=2, pady=(11,10), padx=(10,0))

CheckVar = tk.IntVar(0)
check_button = ttk.Checkbutton(main_frame, variable=CheckVar)
check_button.grid(column=1, row=2, pady=(11,10), sticky="w")

label_4 = ttk.Label(main_frame, text="Output folder", width=12)
label_4.grid(column=0, row=3, pady=(11,15), padx=(10,0))

# Crear un Button para seleccionar una carpeta
browse_folder = ttk.Button(main_frame, text="Browse")
browse_folder.grid(column=1, row=3, pady=(11,15), sticky="w")

label_4 = ttk.Label(main_frame, text="./folder_output", width=12)
label_4.grid(column=2, row=3, pady=(11,15), padx=(0,0), sticky="w")

separator = ttk.Separator(main_frame, orient="horizontal")
separator.grid(column=0, row=4, columnspan=3, sticky="ew", pady=10, padx=(10,0))

button = ttk.Button(main_frame, text="Download Images", command=run_thread, style="Accent.TButton", padding=(10, 5))
button.grid(column=0, row=5, columnspan=3, pady=10)


# Crear un widget Text para mostrar la salida de la consola
text_widget = tk.Text(main_frame, width=40, height=7, font=("Consolas", 10), wrap=tk.WORD, blockcursor=True, state=tk.DISABLED)
text_widget.configure(state=tk.NORMAL)
text_widget.insert(tk.END, 'Download status... \n')
text_widget.configure(state=tk.DISABLED)
text_widget.see(tk.END)
text_widget.grid(column=0, row=6, columnspan=3, sticky="ew", pady=10, padx=(10,0))







# Set dark theme
sv_ttk.set_theme("dark")

# Redireccionar la salida estándar a la widget Text
redirect_stdout_to_text(text_widget)



# Iniciar el bucle principal de Tkinter
root.mainloop()
