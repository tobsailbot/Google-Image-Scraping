import tkinter as tk
from idlelib.tooltip import Hovertip
    
app = tk.Tk()

myBtn = tk.Button(app,text='?')
myBtn.pack(pady=30)
myTip = Hovertip(myBtn,'This is \na multiline tooltip.')

label = tk.Label(app, text="Esto es un texto")
label.pack()
label.config(fg='white')
labelTip = Hovertip(label,'Que onda negro xd')

app.mainloop()