import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sys
from threading import Thread
import sv_ttk
import requests
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import subprocess
import base64
import json
import pathlib

curr_dir = str(pathlib.Path().resolve())

# Data to be written
dictionary = {  "output_folder": "" }
 
# Serializing json
json_object = json.dumps(dictionary, indent=4)


# Opening JSON file
try:
    with open(curr_dir + '/' + 'settings.json', 'r') as readfile:
        settings_file = json.load(readfile)
except:
    with open(curr_dir + "/" + "settings.json", "w") as outfile:
        outfile.write(json_object)
    with open(curr_dir + '/' + 'settings.json', 'r') as readfile:
        settings_file = json.load(readfile)


folder_path = settings_file["output_folder"]

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


def image_scraping(input_search, count, is_transp, folder):
    if not input_search:
        print("'Search input' is invalid.")

    elif count < 1 or count > 99:
        print("'Image count' is invalid.")
    
    elif not folder:
        print("'Output folder' is invalid'.")

    else:
        print('--------------')
        print("Downloading...")
        transparent = ''
        if is_transp:
            transparent = '&tbs=ic:trans'

        # Crea la subcarpeta utilizando el input de búsqueda dentro de la carpeta especificada
        subfolder_path = os.path.join(folder, input_search)
        # Verifica si la subcarpeta existe, y si no, la crea
        if not os.path.isdir(subfolder_path):
            os.makedirs(subfolder_path)

        # Open output dir
        if os.path.isdir(subfolder_path):
            if os.name == 'nt':  # Windows
                os.startfile(subfolder_path)
            elif os.name == 'posix':  # macOS o Linux
                subprocess.Popen(['open', subfolder_path])
        else:
            print("Can't open output dir.")


        def download_image(url, num, isb64):
            # write image to file
            if not isb64:
                reponse = requests.get(url)
                if reponse.status_code==200:
                    with open(os.path.join(subfolder_path, input_search+"_"+str(num)+".png"), 'wb') as file:
                        file.write(reponse.content)
            if isb64:
                image_data = base64.b64decode(url.split(",")[1])
                with open(os.path.join(subfolder_path, input_search+"_"+str(num)+".png"), 'wb') as file:
                    file.write(image_data)

        chrome_options = webdriver.ChromeOptions()    
        # Add your options as needed    
        options = [
        # Define window size here
            # "--window-size=1200,1200",
            "--ignore-certificate-errors",
            "--allow-running-insecure-content",
            "--headless",
            "--disable-gpu",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            '--disable-infobars',
            '--incognito',
            '--disable-popup-blocking'
        ]

        for option in options:
            chrome_options.add_argument(option)

        chromedriver_path = os.path.abspath("chromedriver.exe")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(options=chrome_options, service=service)

        search_URL = f"https://www.google.com/search?tbm=isch{transparent}&q={input_search}"
        driver.get(search_URL)

        #Scrolling all the way up
        driver.execute_script("window.scrollTo(0, 0);")

        for i in range(1, count+1):

            xPath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)

            previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
            previewImageElement = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, previewImageXPath))
            previewImageURL = previewImageElement.get_attribute("src")
            # print("preview URL", previewImageURL)

            driver.find_element(By.XPATH, xPath).click()
            time.sleep(1)

            #It's all about the wait
            timeStarted = time.time()
            while True:

                try:
                    # png, jpg
                    imageElement = WebDriverWait(driver, 3).until(lambda x: x.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]"""))
                except:
                    # GIF 
                    imageElement = WebDriverWait(driver, 3).until(lambda x: x.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[2]/div/a/img[1]"""))
                    
                imageURL= imageElement.get_attribute('src')

                if imageURL != previewImageURL:
                    # print("actual URL", imageURL)
                    b64_decode = False
                    break

                else:
                    # making a timeout if the full res image can't be loaded
                    currentTime = time.time()

                    if currentTime - timeStarted > 10:
                        #print("Timeout! Will download a lower resolution image...")
                        b64_decode = True
                        break


            #Downloading image
            try:
                download_image(imageURL, i, b64_decode)
                print("Downloaded image %s/%s." % (i, count))
                print('OK')
            except:
                print("Couldn't download image %s ..."%(i))

        print('--------------')
        print("Finished downloading all images!")
        driver.quit()






def run_thread(input_search,count,transparent,folder):
    # Crear un hilo para ejecutar el bucle de impresión de números
    thread = Thread(target=image_scraping, args=(input_search, count, transparent, folder))
    # Iniciar el hilo
    thread.start()



# Crear la ventana principal
root = tk.Tk()

# Main window configuration
root.title("Google Img Downloader")
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

CheckVar = tk.IntVar()
check_button = ttk.Checkbutton(main_frame, variable=CheckVar)
check_button.grid(column=1, row=2, pady=(11,10), sticky="w")

label_4 = ttk.Label(main_frame, text="Output folder", width=12)
label_4.grid(column=0, row=3, pady=(11,15), padx=(10,0))


# Variable para almacenar el texto actualizado
folder_output = tk.StringVar()
folder_output.set('../' + folder_path.split("/")[-1])  # Valor inicial de la variable

def change_folder():
    global folder_path
    folder_path = filedialog.askdirectory()  # Abre el diálogo de selección de carpeta
    if folder_path:
        folder_output.set('../' + folder_path.split("/")[-1] )
        print('--------------')
        print("Output folder: ", folder_path)
        # Write path into json file
        settings_file["output_folder"] = folder_path
        with open(curr_dir + '/' + 'settings.json', 'w') as writefile:
            json.dump(settings_file, writefile, indent=4)


# Crear un Button para seleccionar una carpeta
browse_folder = ttk.Button(main_frame, text="Browse", command=change_folder)
browse_folder.grid(column=1, row=3, pady=(11,15), sticky="w")

label_4 = ttk.Label(main_frame, textvariable=folder_output, width=12)
label_4.grid(column=2, row=3, pady=(11,15), padx=(0,0), sticky="w")


separator = ttk.Separator(main_frame, orient="horizontal")
separator.grid(column=0, row=4, columnspan=3, sticky="ew", pady=10, padx=(10,0))


def run_thread_with_params():
    # Obtener los valores de los widgets o variables necesarios
    input_search = entry_1.get()
    if entry_2.get():
        count = int(entry_2.get())
    else:
        count = 0
    transparent = bool(CheckVar.get())
    global folder_path
    # Llamar a la función run_thread con los parámetros
    run_thread(input_search, count, transparent, folder_path)


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