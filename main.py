import Interfaz_grafica as gui
import conexion as base 
##ventana_login = gui.Login()
basec = base.conexion()
usuario1 = base.insertar_usuario(basec, 'Juan', 'Perez', 'juanp', '1234')
usuarios = base.obtener_usuarios(basec)

print(usuarios)