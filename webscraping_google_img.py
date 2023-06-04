
import requests
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import easygui as eg
import subprocess
import base64

# Define la ruta de la carpeta donde se guardarán las imágenes
folder_path = r'D:\TOBI-PC\Descargas\3-VIDEO PROJECTS\1.VIDEO EDITING RESOURCES\MEDIA\IMAGES'
cantidad_imgs = 5

campos = ['Search input', 'Transparent(t) or Normal(n)', "Imgs Ammount", 'Images folder']

default = ['', "t",cantidad_imgs, folder_path]

# Creates a window with multiple input boxes
box = eg.multenterbox(msg=f'Download {cantidad_imgs} google images:',title='Google Image Downloader',fields=campos, values=default)

if not box == None:
    # Obtiene el input de búsqueda del usuario
    search_input = box[0]
    cantidad_imgs = int(box[2])
    transparent = ''

    # Obtiene el input de búsqueda del usuario mediante una ventana emergente
    if box[1] == 't':
        transparent = '&tbs=ic:trans'
    if box[1] == 'n':
        pass

    # Crea la subcarpeta utilizando el input de búsqueda dentro de la carpeta especificada
    subfolder_path = os.path.join(folder_path, search_input)

    # Verifica si la subcarpeta existe, y si no, la crea
    if not os.path.isdir(subfolder_path):
        os.makedirs(subfolder_path)


    def download_image(url, num, isb64):
        # write image to file
        if not isb64:
            reponse = requests.get(url)
            print(reponse.status_code)
            if reponse.status_code==200:
                with open(os.path.join(subfolder_path, search_input+"_"+str(num)+".png"), 'wb') as file:
                    file.write(reponse.content)
        if isb64:
            image_data = base64.b64decode(url.split(",")[1])
            with open(os.path.join(subfolder_path, search_input+"_"+str(num)+".png"), 'wb') as file:
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

    search_URL = f"https://www.google.com/search?tbm=isch{transparent}&q={search_input}"
    driver.get(search_URL)

    # open the media folders
    subprocess.Popen(f'explorer "{subfolder_path}"')

    #Scrolling all the way up
    driver.execute_script("window.scrollTo(0, 0);")




    for i in range(1, cantidad_imgs+1):

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
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    b64_decode = True
                    break


        #Downloading image
        try:
            download_image(imageURL, i, b64_decode)
            print("Downloaded element %s out of %s total." % (i, cantidad_imgs))
        except:
            print("Couldn't download an image %s, continuing downloading the next one"%(i))

    print("Finished downloading all images!")
    driver.quit()
