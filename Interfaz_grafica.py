import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image, ImageTk
from base_datos import UserDatabase
import speech_recognition as sr
import keyboard
import threading
from time import strftime
# Configuraciones Globales modo color y tema
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
user_db = UserDatabase(filename="users.json")

class Login:
    def __init__(self):
        # Creacion de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Sistema Operativo Dx")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Establece la geometría para ocupar toda la pantalla
        self.root.geometry(f"{screen_width}x{screen_height-60}")
        imagen = ctk.CTkImage(Image.open(os.path.join("Imagenes", "monterey.png")),size=(screen_width,screen_height))
        background = ctk.CTkLabel(master=self.root, image = imagen, text="")
        background.place(x = 0, y = 0)
        #self.root.iconbitmap("img/icon.ico")

        # Banner
        banner = ctk.CTkLabel(master=self.root, text="", width=400, height=640, corner_radius=100)
        banner.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        # Contenido de la ventana principal
        # logo
        logo = ctk.CTkImage(
            light_image= Image.open(os.path.join("Imagenes", "DX.png")),
            dark_image= Image.open(os.path.join("Imagenes", "DX.png")),
            size=(250,250))
        
        # Etiqueta para mostrar el logo
        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="", anchor="center")
        etiqueta.pack(pady=55)

        #Campos de texto
        #Usuario
        ctk.CTkLabel(self.root, text="Usuario", fg_color="transparent").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Usuario")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()


        # Contraseña
        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contrase = ctk.CTkEntry(self.root)
        self.contrase.insert(0, "*******")
        self.contrase.bind("<Button-1>", lambda e: self.contrase.delete(0, 'end'))
        self.contrase.pack()

        #Boton de inicio de sesion
        ctk.CTkButton(self.root, text="Entrar", command=self.validar).pack(pady=10)

        # Bucle de ejecucion
        self.root.mainloop()


        # Función para validar el login
    def validar(self):
        obtener_usuario = self.usuario.get() # Obtenemos el nombre de usuario
        obtener_contrasena = self.contrase.get() # Obtenemos la contraseña
        for user in user_db.users:
        # Verifica si el valor que tiene el usuario o la contraseña o ambos no coinciden
            if obtener_usuario != user.username or obtener_contrasena != user.password:
                # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
                if hasattr(self, "info_login"):
                    self.info_login.destroy()
                # Crea esta etiqueta siempre que el login sea incorrecto
                self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos.")
                self.info_login.pack()
            else:
                # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
                if hasattr(self, "info_login"):
                    self.info_login.destroy()
                # Crea esta etiqueta siempre que el login sea correcto
                self. info_login = ctk.CTkLabel(self.root, text=f"Hola, {obtener_usuario}. Espere unos instantes...")
                self.info_login.pack()
                # Se destruye la ventana de login
                self.root.destroy()
                # Se instancia la ventana de opciones
                ventana_principal = VentanaPrincipal()
                break

# Class para la ventana principal
class VentanaPrincipal:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Supra Os")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Establece la geometría para ocupar toda la pantalla
        self.root.geometry(f"{screen_width}x{screen_height-60}")
        imagen = ctk.CTkImage(Image.open(os.path.join("Imagenes", "iridescence.png")),size=(screen_width,screen_height))
        background = ctk.CTkLabel(master=self.root, image = imagen, text="")
        background.place(x = 0, y = 0)
        listen_thread = threading.Thread(target=ReconocimientoVoz)
        listen_thread.start()
        self.root.mainloop()

# Class para el reconocimiento de voz   
class ReconocimientoVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer() 
        hilo = threading.Thread(target=self.start_keyboard_hook)
        hilo.start()   

        # Función para iniciar el reconocimiento de voz
    def start_listening(self):
        with sr.Microphone() as source:
            print("Escuchando... Presiona Ctrl+M nuevamente para detener.")
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio)
            print("Has dicho: {}".format(text))
            if text == 'open system':
                print("Abriendo sistema")
        except sr.UnknownValueError:
            print("No se pudo entender lo que dijiste")
        except sr.RequestError as e:
            print("Error en la solicitud a Google Speech Recognition; {0}".format(e))

    def start_keyboard_hook(self):
        keyboard.hook(self.on_key_event)
        keyboard.wait('esc')
        
            # Función que se ejecutará cuando se presione una tecla
    def on_key_event(self, keyboard_event):
        if keyboard_event.event_type == keyboard.KEY_DOWN and keyboard_event.name == 'm':
            if keyboard.is_pressed('ctrl'):
                print("Presionaste Ctrl+M")
                self.start_listening()