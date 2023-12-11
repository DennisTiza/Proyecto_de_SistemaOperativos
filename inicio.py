import customtkinter as ctk
import os
from PIL import Image

from conexion import crear_usuario, editar_usuario

class Inicio:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Gestión de Usuarios")
        self.root.geometry("400x400")

        # Frame principal
        frame_principal = ctk.CTkFrame(master=root)
        frame_principal.pack(padx=10, pady=10)

        # Imagen del usuario
        if user['foto'] is not None:
            foto = ctk.CTkImage(Image.open(os.path.join("Imagenes", user['foto'])), size=(80, 80))
        else:
            foto = ctk.CTkImage(Image.open(os.path.join("Imagenes", "usuario.png")), size=(80, 80))
        cuadro_foto = ctk.CTkLabel(master=frame_principal, image=foto, text="")
        cuadro_foto.grid(row=0, column=0, padx=5, pady=5, rowspan=2)

        # Etiquetas de información del usuario
        etiqueta_nombre = ctk.CTkLabel(master=frame_principal, text=f"Nombre: {user['nombre']} {user['apellido']}")
        etiqueta_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        etiqueta_usuario = ctk.CTkLabel(master=frame_principal, text=f"Usuario: {user['nombre_usuario']}      Rol: {user['rol']}")
        etiqueta_usuario.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tifo = ctk.CTkLabel(master=root, text="")
        tifo.pack()

         # Crear Nuevo Usuario Button
        if user['rol'] == 'admin':
            boton_crear = ctk.CTkButton(master=tifo, text="Crear Nuevo Usuario", command=lambda: self.crearusuario(tifo))
            boton_crear.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Editar Usuario Button
        boton_editar = ctk.CTkButton(master=tifo, text="Editar Usuario", command=lambda: self.editarusuario(tifo, user))
        boton_editar.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    def crearusuario(self, root):
        tifo = ctk.CTkFrame(master=root)
        tifo.grid(row=1, column=1, padx=10, pady=10)
        #Nombre
        ctk.CTkLabel(tifo, text="Nombre", fg_color="transparent").pack()
        nombre = ctk.CTkEntry(tifo)
        nombre.pack()
        #Apellido
        ctk.CTkLabel(tifo, text="Apellido", fg_color="transparent").pack()
        apellido = ctk.CTkEntry(tifo)
        apellido.pack()
        #Usuario
        ctk.CTkLabel(tifo, text="Usuario", fg_color="transparent").pack()
        usuario = ctk.CTkEntry(tifo)
        usuario.pack()
        #Contraseña
        ctk.CTkLabel(tifo, text="Contraseña", fg_color="transparent").pack()
        contraseña = ctk.CTkEntry(tifo, show="*")
        contraseña.pack()
        #Rol
        ctk.CTkLabel(tifo, text="Rol", fg_color="transparent").pack()
        roles = ["admin", "usuario"]
        rol_seleccionado = ctk.CTkComboBox(tifo, values=roles)
        rol_seleccionado.pack(pady=10, padx=10)
        #Informacion
        info = ctk.CTkLabel(tifo, text="")
        #Boton de confirmacion
        ctk.CTkButton(tifo, text="Confirmar", command=lambda: self.confirmar(nombre, apellido, usuario, contraseña, rol_seleccionado, info)).pack()
        info.pack()
        self.root.geometry("400x550")

    def editarusuario(self, root, user):
        tifo = ctk.CTkFrame(master=root)
        tifo.grid(row=1, column=0, padx=10, pady=10)
        #Nombre
        ctk.CTkLabel(tifo, text="Nombre", fg_color="transparent").pack()
        nombre = ctk.CTkEntry(tifo)
        nombre.pack()
        #Apellido
        ctk.CTkLabel(tifo, text="Apellido", fg_color="transparent").pack()
        apellido = ctk.CTkEntry(tifo)
        apellido.pack()
        #Usuario
        ctk.CTkLabel(tifo, text="Usuario", fg_color="transparent").pack()
        usuario = ctk.CTkEntry(tifo)
        usuario.pack()
        #Contraseña
        ctk.CTkLabel(tifo, text="Contraseña", fg_color="transparent").pack()
        contraseña = ctk.CTkEntry(tifo, show="*")
        contraseña.pack()
        #Informacion
        info = ctk.CTkLabel(tifo, text="")
        #Boton de confirmacion
        ctk.CTkButton(tifo, text="Confirmar", command=lambda: self.confirmareditar(user,nombre, apellido, usuario, contraseña,info)).pack()
        info.pack()
        self.root.geometry("400x550")
    
    def confirmareditar(self, user, nombre, apellido, usuario, contraseña, info):
        print(user)
        bandera = False
        
        if nombre.get() != "":
            user['nombre'] = nombre.get()
        if  apellido.get() != "":
            user['apellido'] = apellido.get()
        if usuario.get() != "":
            user['nombre_usuario'] = usuario.get()
        if contraseña.get() != "":
            user['contraseña'] = contraseña.get()
            bandera = True
        info.configure(text="Usuario editado con éxito")
        print(user)
        editar_usuario(user['id'], user['nombre'], user['apellido'], user['nombre_usuario'], user['contraseña'], user['rol'], user['foto'], bandera)



    def confirmar(self, nombre, apellido, usuario, contraseña, rol_seleccionado, info):
    # Validación de datos
        if not nombre or not apellido or not usuario or not contraseña or not rol_seleccionado:
            info.configure(text="Todos los campos son requeridos")
            return
        # Insertar usuario en la base de datos
        info.configure(text="Usuario creado con éxito")
        crear_usuario(nombre, apellido, usuario, contraseña, rol_seleccionado.get())

    
def init(principal, user):
    root = ctk.CTkToplevel(master=principal)
    root.attributes('-topmost', 1)
    app = Inicio(root, user)
    principal.mainloop()
