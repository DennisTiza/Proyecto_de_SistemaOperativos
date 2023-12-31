import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image, ImageTk
import speech_recognition as sr
import conexion as base
import prueba as musica
import inicio as inicio
import mysql.connector 
import editor as Appeditor
import visorImagenes as visor
import visordevideos as visorvideo
import calculadora as calcu
import fileManager as filemanager
import keyboard
import threading
import bcrypt
import psutil
import subprocess
from globals import root
from web import abrir_google
from time import strftime
# Configuraciones Globales modo color y tema
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

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
        self.contrase = ctk.CTkEntry(tifo, show="*")
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
        obtener_usuario = self.usuario.get()  # Obtenemos el nombre de usuario
        obtener_contrasena = self.contrase.get()  # Obtenemos la contraseña

        try:
            conn = base.conexion()  # Conecta a la base de datos
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (obtener_usuario,))
                user = cursor.fetchone()

                if user:
                    stored_hashed_password = user.get('contraseña', '')  # Obtén el hash almacenado en la base de datos

                    # Verifica la contraseña utilizando bcrypt
                    if bcrypt.checkpw(obtener_contrasena.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                        if hasattr(self, "info_login"):
                            self.info_login.destroy()

                        self.info_login = ctk.CTkLabel(self.root, text="Login correcto")
                        self.info_login.pack(pady=10)
                        self.root.destroy()
                        ventana_principal = VentanaPrincipal(user)
                    else:
                        self.info_login.configure(text="Usuario o contraseña incorrectos")
                else:
                    self.info_login.configure(text="Usuario o contraseña incorrectos")
        except mysql.connector.Error as err:
            print(f'Error al conectar a la base de datos: {err}')

# Class para la ventana principal
class VentanaPrincipal:
    def __init__(self, user):
        global root
        self.root = ctk.CTk()
        root = self.root
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

        # CREACION DE LOS BOTONES DE LA BARRA DE MENU
        dx = ctk.CTkImage(Image.open(os.path.join("Imagenes", "DX1.png")),size=(38,38))
        music = ctk.CTkImage(Image.open(os.path.join("Imagenes", "musica.png")),size=(38,38))
        editor = ctk.CTkImage(Image.open(os.path.join("Imagenes", "editor.png")),size=(38,38))
        calculadora = ctk.CTkImage(Image.open(os.path.join("Imagenes", "calculadora.png")),size=(38,38))
        imagen = ctk.CTkImage(Image.open(os.path.join("Imagenes", "imagen.png")),size=(38,38))
        video = ctk.CTkImage(Image.open(os.path.join("Imagenes", "video.png")),size=(38,38))
        carpeta = ctk.CTkImage(Image.open(os.path.join("Imagenes", "carpetas.png")),size=(38,38))
        google = ctk.CTkImage(Image.open(os.path.join("Imagenes", "google.png")),size=(38,38))
        rut = ""

        boton1 = ctk.CTkButton( master=barra, image=dx, text="", width=30, height= 16, command=lambda: inicio.init(self.root, user))
        boton1.place(relx=0.03, rely=0.25, anchor=ctk.CENTER)
        boton2 = ctk.CTkButton(master=barra,image= music, text="", width=30, height= 16, command = lambda: musica.init(self.root))
        boton2.place(relx=0.074, rely=0.25, anchor=ctk.CENTER)
        boton3 = ctk.CTkButton(master=barra,image= editor, text="", width=30, height= 16, command=lambda: Appeditor.init(self.root, rut))
        boton3.place(relx=0.117, rely=0.25, anchor=ctk.CENTER)
        boton4 = ctk.CTkButton(master=barra,image= calculadora, text="", width=30, height= 16, command=lambda: calcu.init(self.root))
        boton4.place(relx=0.16, rely=0.25, anchor=ctk.CENTER)
        boton5 = ctk.CTkButton(master=barra,image= imagen, text="", width=30, height= 16, command=lambda: visor.init(self.root))
        boton5.place(relx=0.203, rely=0.25, anchor=ctk.CENTER)
        boton6 = ctk.CTkButton(master=barra,image= video, text="", width=30, height= 16, command=lambda: visorvideo.init(self.root))
        boton6.place(relx=0.246, rely=0.25, anchor=ctk.CENTER)
        boton7 = ctk.CTkButton(master=barra,image= carpeta, text="", width=30, height= 16, command=lambda: filemanager.init(user))
        boton7.place(relx=0.289, rely=0.25, anchor=ctk.CENTER)
        boton8 = ctk.CTkButton(master=barra,image= google, text="", width=30, height= 16, command=lambda: abrir_google(self.root))
        boton8.place(relx=0.332, rely=0.25, anchor=ctk.CENTER)

        listen_thread = threading.Thread(target=ReconocimientoVoz, args=(self.root,))
        listen_thread.start()
        reloj_thread = threading.Thread(target=Reloj, args=(self.root,))
        reloj_thread.start()
        bateria_thread = threading.Thread(target=BateriaEstado, args=(self.root,))
        bateria_thread.start()
        wifi_thread = threading.Thread(target=WiFiEstado, args=(self.root,))
        wifi_thread.start()

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

class WiFiEstado:
    def __init__(self, ventana):
        self.texto_wifi = ctk.CTkLabel(master=ventana, fg_color=("white", "midnight blue"), font=('Radioland', 14, 'bold'))
        self.texto_wifi.place(relx=0.79, rely=0.967, anchor=ctk.CENTER)
        self.update_wifi_status()

    def get_wifi_info(self):
        cmd = 'netsh wlan show interfaces'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8', 'ignore') .split('\n')
    
        if output:
            for line in output:
                if 'Seal' in line:
                    signal = line.split(':')[1].strip()
        return signal

    def update_wifi_status(self):
        wifi_strength = self.get_wifi_info()
        if wifi_strength is not None:
            wifi_strength_num = int(wifi_strength.rstrip('%'))
            # Convert the strength to a number between 0 and 5 for the bars
            bars = "|" * min(wifi_strength_num // 20, 5)  # Corregido cálculo de las barras
            self.texto_wifi.configure(text=f"Fuerza de señal WiFi: {wifi_strength}\nBarras de conexión: {bars}")
        else:
            self.texto_wifi.configure(text="No se pudo obtener la señal WiFi")

        self.texto_wifi.after(3000, self.update_wifi_status)  # Actualiza cada 3 segundos

class BateriaEstado:
    def __init__(self, ventana):
        self.texto_bateria = ctk.CTkLabel(master=ventana, fg_color=("white", "midnight blue"), font=('Radioland', 14, 'bold'))
        self.texto_bateria.place(relx=0.90, rely=0.966, anchor=ctk.CENTER)
        self.update_battery_status()

    def update_battery_status(self):
        battery = psutil.sensors_battery()
        percent = battery.percent if battery else "Desconocido"
        charging_status = "+" if battery.power_plugged else ""
        self.texto_bateria.configure(text=f"Bateria: {charging_status}{percent}%")
        self.texto_bateria.after(1000, self.update_battery_status)  # Actualiza cada segundo

# Class para el reconocimiento de voz   
class ReconocimientoVoz:
    def __init__(self, ventana):
        global ventana_principal
        ventana_principal = ventana
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
            if text == 'open music':
                musica.init(ventana_principal)
            if text == 'open editor':
                Appeditor.init(ventana_principal)
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

class BarradeTareas:
    def __init__(self, ventana, barra):
        self.recognizer = sr.Recognizer() 
        hilo = threading.Thread(target=self.start_keyboard_hook)
        hilo.start() 
