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
        self.root.attributes('-fullscreen', True)
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
        
        # Frame para el logo y el texto
        tifo = ctk.CTkFrame(master=self.root, corner_radius=40)
        tifo.place(relx=0.5, rely=0.49, anchor=ctk.CENTER)
        
        # Etiqueta para mostrar el logo
        etiqueta = ctk.CTkLabel(master=tifo, image=logo, text="", anchor=ctk.CENTER)
        etiqueta.pack(pady=30, padx=30)

        #Campos de texto
        #Usuario
        ctk.CTkLabel(tifo, text="Usuario", fg_color="transparent").pack()
        self.usuario = ctk.CTkEntry(tifo)
        self.usuario.insert(0, "Usuario")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()


        # Contraseña
        ctk.CTkLabel(tifo, text="Contraseña").pack()
        self.contrase = ctk.CTkEntry(tifo)
        self.contrase.insert(0, "*******")
        self.contrase.bind("<Button-1>", lambda e: self.contrase.delete(0, 'end'))
        self.contrase.pack()
        self.info_login = ctk.CTkLabel(tifo, text="")
        #Boton de inicio de sesion
        ctk.CTkButton(tifo, text="Entrar", command=lambda: self.validar(self.info_login)).pack(pady=10)
        self.info_login.pack(pady=10)
        # Bucle de ejecucion
        self.root.mainloop()


        # Función para validar el login
    def validar(self, login):
        obtener_usuario = self.usuario.get() # Obtenemos el nombre de usuario
        obtener_contrasena = self.contrase.get() # Obtenemos la contraseña
        for user in user_db.users:
        # Verifica si el valor que tiene el usuario o la contraseña o ambos no coinciden
            if obtener_usuario != user.username or obtener_contrasena != user.password:
                # Crea esta etiqueta siempre que el login sea incorrecto
                self.info_login.configure(text="Usuario o contraseña incorrectos")
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
        self.root.attributes('-fullscreen', True)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()        

        # Establece la geometría para ocupar toda la pantalla
        self.root.geometry(f"{screen_width}x{screen_height-60}")
        imagen = ctk.CTkImage(Image.open(os.path.join("Imagenes", "iridescence.png")),size=(screen_width,screen_height))
        background = ctk.CTkLabel(master=self.root, image = imagen, text="")
        background.place(x = 0, y = 0)

        # CREACION DE LA BARRA DE MENU
        barra = ctk.CTkLabel(master=self.root, text="", width= screen_width, height=100,  fg_color=("steel blue", "midnight blue"),corner_radius=8)
        barra.place(relx=0.5, rely=1, anchor=ctk.CENTER)

        listen_thread = threading.Thread(target=ReconocimientoVoz)
        listen_thread.start()
        reloj_thread = threading.Thread(target=Reloj, args=(self.root,))
        reloj_thread.start()
        self.root.mainloop()

class Reloj:
    def __init__(self, ventana):
        # Configura las etiquetas para mostrar la hora, el día y la fecha
        self.texto_hora = ctk.CTkLabel(master=ventana, fg_color=("white", "midnight blue"), font=('Radioland', 14, 'bold'))
        self.texto_hora.place(relx=0.97, rely=0.957, anchor=ctk.CENTER)

        self.texto_fecha = ctk.CTkLabel(master=ventana, fg_color=("midnight blue", "midnight blue"), font=('Radioland', 14, 'bold'))
        self.texto_fecha.place(relx=0.97, rely=0.984, anchor=ctk.CENTER)

        self.actualizar_tiempo()

    def actualizar_tiempo(self):
        # Obtén la hora actual en formato 12 horas con 'am' o 'pm'
        hora = strftime('%I:%M %p')

        # Traducción de los nombres de los días a español
        dias = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        dia = strftime('%A')
        dia_traducido = dias.get(dia, dia)

        # Obtén la fecha actual
        fecha = strftime('%d/%m/%y')

        self.texto_hora.configure(text=hora)
        self.texto_fecha.configure(text=fecha)

        # Programa la actualización periódica cada 1000 ms (1 segundo)
        self.texto_hora.after(1000, self.actualizar_tiempo)


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