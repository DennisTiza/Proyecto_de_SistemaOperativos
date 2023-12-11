import customtkinter as ctk
from customtkinter import StringVar
from customtkinter import CTkLabel
from customtkinter import filedialog as FileDialog
from tkinter import Menu as tkMenu, Text as Texto
from io import open

def init(principal, rut):
    global ruta  # Declarar ruta como global
    ruta = rut
  
    def nuevo():
        global ruta  # Usa nonlocal para indicar que ruta es la variable en el ámbito superior
        mensaje.set("Nuevo fichero")
        ruta = ""
        texto.delete(1.0, "end")
        root.title("Editor de Texto")

    def abrir():
        global ruta  # Usa nonlocal para indicar que ruta es la variable en el ámbito superior
        mensaje.set("Abrir fichero")
        ruta = FileDialog.askopenfilename(
            initialdir='.', 
            filetypes=(("Ficheros de texto", "*.txt"),),
            title="Abrir un fichero de texto")

        if ruta != "":
            fichero = open(ruta, 'r')
            contenido = fichero.read()
            texto.delete(1.0,'end')
            texto.insert('insert', contenido)
            fichero.close()
            root.title(ruta + " - Editor de Texto")

    def cargar(rut):
        global ruta
        ruta = rut
        mensaje.set("Abrir fichero")
        if ruta != "":
            fichero = open(ruta, 'r')
            contenido = fichero.read()
            texto.delete(1.0,'end')
            texto.insert('insert', contenido)
            fichero.close()
            root.title(ruta + " - Editor de Texto")



    def guardar():
        global ruta  # Usa nonlocal para indicar que ruta es la variable en el ámbito superior
        mensaje.set("Guardar fichero")
        if ruta != "":
            contenido = texto.get(1.0,'end-1c')
            fichero = open(ruta, 'w+')
            fichero.write(contenido)
            fichero.close()
            mensaje.set("Fichero guardado correctamente")
        else:
            guardar_como()

    def guardar_como():
        global ruta  # Usa nonlocal para indicar que ruta es la variable en el ámbito superior
        mensaje.set("Guardar fichero como")

        fichero = FileDialog.asksaveasfile(title="Guardar fichero", 
            mode="w", defaultextension=".txt")

        if fichero is not None:
            ruta = fichero.name
            contenido = texto.get(1.0,'end-1c')
            fichero = open(ruta, 'w+')
            fichero.write(contenido)
            fichero.close()
            mensaje.set("Fichero guardado correctamente")
        else:
            mensaje.set("Guardado cancelado")
            ruta = ""


    # Configuración de la raíz
    root = ctk.CTkToplevel(master=principal)
    root.title("Editor de Texto")
    root.attributes('-topmost', 1)

    # Menú superior
    menubar = tkMenu(root)
    filemenu = tkMenu(menubar, tearoff=0)
    filemenu.add_command(label="Nuevo", command=nuevo)
    filemenu.add_command(label="Abrir", command=abrir)
    filemenu.add_command(label="Guardar", command=guardar)
    filemenu.add_command(label="Guardar como", command=guardar_como)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(menu=filemenu, label="Archivo")

    # Caja de texto central
    texto = Texto(root)
    texto.pack(fill="both", expand=1)
    texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))

    # Monitor inferior
    mensaje = StringVar()
    mensaje.set("Bienvenido a tu Editor")
    monitor = ctk.CTkLabel( master=root, textvariable=mensaje , justify='left')
    monitor.pack(side="top", anchor="center")

    root.config(menu=menubar)

    if ruta != "":
        cargar(ruta)