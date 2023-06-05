import tkinter as tk
import sys
import time
from threading import Thread

def redirect_stdout_to_text(widget):
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, message):
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)

        def flush(self):
            pass

    sys.stdout = StdoutRedirector(widget)

def print_numbers():
    for i in range(1, 11):
        print(i)
        time.sleep(1)

# Crear la ventana principal
root = tk.Tk()

# Crear un widget Text para mostrar la salida de la consola
text_widget = tk.Text(root)
text_widget.pack()

# Redireccionar la salida estándar a la widget Text
redirect_stdout_to_text(text_widget)

# Crear un hilo para ejecutar el bucle de impresión de números
thread = Thread(target=print_numbers)

# Iniciar el hilo
thread.start()

# Iniciar el bucle principal de Tkinter
root.mainloop()
