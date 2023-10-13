import mysql.connector

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
        cursor.execute('SELECT id, nombre, apellido, nombre_usuario, contraseña FROM usuarios')
        results = cursor.fetchall()
        usuarios = []
        for row in results:
            id, nombre, apellido, nombre_usuario, contraseña = row
            usuario = {
                'id': id,
                'nombre': nombre,
                'apellido': apellido,
                'nombre_usuario': nombre_usuario,
                'contraseña': contraseña
            }
            usuarios.append(usuario)
        cursor.close()
        return usuarios
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None
    
def insertar_usuario(conn, nombre, apellido, nombre_usuario, contraseña):
    """Insertar un nuevo usuario en la tabla de usuarios."""
    if conn is None:
        print('No se pudo establecer la conexión.')
        return

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nombre, apellido, nombre_usuario, contraseña) VALUES (%s, %s, %s, %s)"
        datos_usuario = (nombre, apellido, nombre_usuario, contraseña)
        cursor.execute(sql, datos_usuario)
        conn.commit()
        print('Usuario insertado con éxito.')
        cursor.close()
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        conn.rollback()


