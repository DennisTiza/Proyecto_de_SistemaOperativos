from os import listdir, path, rename
from customtkinter import CTkImage
from subprocess import run
from PIL import Image

from components.file import File


class Folder:
    MAX_DEPTH = 5

    def __init__(self, path) -> None:
        self._image = self.get_image('folder.png')
        self._path = path
        self._name = path.split('\\')[-1]
        self._lst_content = []
        self._depth = path.count('\\')
        self.insert_content()

    @property
    def list_content(self):
        return self._lst_content

    @list_content.setter
    def list_content(self, value):
        self._lst_content = value

    def insert_content(self):
        if self._depth >= self.MAX_DEPTH:
            return

        def insert(p):
            if path.isdir(p):
                self.list_content.append(Folder(p))

            elif path.isfile(p):
                self.list_content.append(File(p))

        try:
            for content in listdir(self._path):
                if not content.startswith('.'):
                    insert(path.join(self._path, content))

        except Exception as e:
            pass

    def create(self, name):
        run(['mkdir', path.join(self._path, name)])
        self.insert_content()

    def cut(self, new_path):
        run(['mv', self._path, new_path])
        self._path = path.join(new_path, self._name)

    def copy(self, new_path):
        run(['cp', self._path, new_path])
        self._path = path.join(new_path, self._name)

    def delete(self):
        run(['rm', '-rf', self._path])

    def get_image(self, name):
        folder_image = Image.open('./components/assets/img/' + name)
        folder_image = folder_image.resize((100, 100))
        return CTkImage(folder_image, size=(100, 100))

    def change_name(self, new_name):
        self._name = new_name
        old_dir, old_base = path.split(self._path)
        new_path = path.join(old_dir, new_name)
        rename(self._path, new_path)
        self._path = new_path

    def __str__(self) -> str:
        return self._name
