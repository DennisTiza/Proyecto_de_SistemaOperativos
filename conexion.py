import os
import mysql.connector
import bcrypt

def conexion():
    # Configura la conexión a la base de datos
    config = {
        'user': 'root',
        'password': '1234',
        'host': 'localhost',
        'database': 'sistema',
        'port': '3306',  # Reemplaza 'tu_puerto' con el puerto correcto
        'raise_on_warnings': True
    }
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print('Conexión establecida')
            return conn
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None


def obtener_usuarios(conn):
    """Obtener los datos de la tabla de usuarios."""
    if conn is None:
        print('No se pudo establecer la conexión.')
        return

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, apellido, nombre_usuario, contraseña, rol FROM usuarios')
        results = cursor.fetchall()
        usuarios = []
        for row in results:
            id, nombre, apellido, nombre_usuario, contraseña, rol, foto = row
            usuario = {
                'id': id,
                'nombre': nombre,
                'apellido': apellido,
                'nombre_usuario': nombre_usuario,
                'contraseña': contraseña,
                'rol': rol,
                'foto': foto
            }
            usuarios.append(usuario)
        cursor.close()
        return usuarios
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None
    
def insertar_usuario(conn, nombre, apellido, nombre_usuario, contraseña, rol, foto):
    if conn is None:
        print('No se pudo establecer la conexión.')
        return

    try:
        cursor = conn.cursor()
        # Utiliza bcrypt para hashear la contraseña
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO usuarios (nombre, apellido, nombre_usuario, contraseña, rol, foto) VALUES (%s, %s, %s, %s, %s, %s)"
        datos_usuario = (nombre, apellido, nombre_usuario, hashed_password.decode('utf-8'), rol, foto)
        cursor.execute(sql, datos_usuario)
        conn.commit()
        print('Usuario insertado con éxito.')
        
        # Obtén el ID del usuario recién insertado
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_usuario = cursor.fetchone()[0]

        # Commit para aplicar los cambios en la base de datos
        conn.commit()

        print('Usuario insertado con éxito. ID del usuario:', id_usuario)
        # Crea la carpeta con el nombre del ID del usuario
        carpeta_usuarios = os.path.join(os.getcwd(), 'Usuarios')
        carpeta_usuario = os.path.join(carpeta_usuarios, str(id_usuario))
        os.makedirs(carpeta_usuario, exist_ok=True)
        print(f'Carpeta para el usuario creada: {carpeta_usuario}')

        cursor.close()
    except mysql.connector.Error as err:
        print(f'Error al insertar usuario: {err}')
        conn.rollback()

def editar_usuarios(conn, id_usuario, nombre, apellido, nombre_usuario, contraseña, rol, foto, bandera):
    if conn is None:
        print('No se pudo establecer la conexión.')
        return

    try:
        cursor = conn.cursor()

        # Utiliza bcrypt para hashear la nueva contraseña si se proporciona
        if bandera == True :
            hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
            sql = "UPDATE usuarios SET nombre=%s, apellido=%s, nombre_usuario=%s, contraseña=%s, rol=%s, foto=%s WHERE id=%s"
            datos_usuario = (nombre, apellido, nombre_usuario, hashed_password.decode('utf-8'), rol, foto, id_usuario)
        else:
            sql = "UPDATE usuarios SET nombre=%s, apellido=%s, nombre_usuario=%s, rol=%s, foto=%s WHERE id=%s"
            datos_usuario = (nombre, apellido, nombre_usuario, rol, foto, id_usuario)

        cursor.execute(sql, datos_usuario)
        conn.commit()
        print(f'Usuario con ID {id_usuario} actualizado con éxito.')

        cursor.close()
    except mysql.connector.Error as err:
        print(f'Error al editar usuario: {err}')
        conn.rollback()

def crear_usuario(nombre, apellido, nombre_usuario, contraseña, rol):
    conexion_bd = conexion()

    if conexion_bd:
        # Obtener información del nuevo usuario
        nombre = nombre.get()
        apellido = apellido.get()
        nombre_usuario = nombre_usuario.get()
        contraseña = contraseña.get()
        foto = None
        # Llamar a la función insertar_usuario para agregar el nuevo usuario
        insertar_usuario(conexion_bd, nombre, apellido, nombre_usuario, contraseña, rol, foto)
        # Cerrar la conexión al finalizar
        conexion_bd.close()

def editar_usuario(id_usuario, nombre, apellido, nombre_usuario, contraseña, rol, foto, bandera):
    conexion_bd = conexion()
    if conexion_bd:
        # Obtener información del usuario actualizado
        nombre = nombre
        apellido = apellido
        nombre_usuario = nombre_usuario
        contraseña = contraseña
        foto = None
        # Llamar a la función editar_usuario para actualizar el usuario
        editar_usuarios(conexion_bd, id_usuario, nombre, apellido, nombre_usuario, contraseña, rol, foto, bandera)
        # Cerrar la conexión al finalizar
        conexion_bd.close()
