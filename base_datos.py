import json
import os

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    @staticmethod
    def from_dict(user_dict):
        return User(user_dict['id'], user_dict['username'], user_dict['password'])


class UserDatabase:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.load_from_file()

    def create_user(self, username, password):
        self.current_id += 1  # Increment current_id
        user = User(self.current_id, username, password)
        self.users.append(user)
        self.save_to_file()  # Save to file after creating a user
        return user


    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def update_user(self, user_id, new_username, new_password):
        user = self.get_user_by_id(user_id)
        if user:
            user.username = new_username
            user.password = new_password
            return True
        return False

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False

    def get_all_users(self):
        return self.users
    
    def load_from_file(self):
        self.users = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                user_dicts = json.load(file)
                self.users = [User.from_dict(user_dict) for user_dict in user_dicts]
                # Set the current_id to the maximum existing id + 1
                self.current_id = max([user.id for user in self.users], default=0)
        else:
            self.current_id = 0  # Initialize current_id if file doesn't exist

    def save_to_file(self):
        user_dicts = [user.to_dict() for user in self.users]
        with open(self.filename, 'w') as file:
            json.dump(user_dicts, file)

'''
# Ejemplo de uso
user_db = UserDatabase(filename="users.json") 

# Crear usuarios
user_db.create_user("usuario1", "password1")
user_db.create_user("usuario2", "password2")

# Obtener todos los usuarios
print("Usuarios:")
for user in user_db.users:
    print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}")

# Actualizar un usuario
user_db.update_user(1, "usuario1_actualizado", "nueva_password1")

# Obtener un usuario por ID
user = user_db.get_user_by_id(1)
if user:
    print(f"Usuario con ID 1: {user.username}")

# Eliminar un usuario
user_db.delete_user(2)

# Obtener todos los usuarios después de eliminar uno
print("Usuarios después de eliminar:")
for user in user_db.users:
    print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}")

# Guardar los usuarios en un archivo
user_db.save_to_file()

'''