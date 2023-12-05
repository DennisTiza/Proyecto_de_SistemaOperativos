from customtkinter import CTkImage
from os import path, rename, startfile
from PIL import Image

from subprocess import run


class File:
    def __init__(self, path: str) -> None:
        self._path = path
        self._name = path.split('\\')[-1]
        self._depth = path.count('\\')
        self._image = self.get_image()

    def get_image(self):
        def ends_with(x): return self._name.endswith(x)
        name = {
            ends_with('.py'): 'py.png',
            ends_with('.js'): 'javascript.png',
            ends_with('.txt'): 'txt-file.png',
            ends_with('.mp4'): 'mp4.png',
            ends_with('.png'): 'image.png',
            ends_with('.jpg'): 'image.png',
            ends_with('.jpeg'): 'image.png',
            ends_with('.pdf'): 'pdf.png',
            ends_with('.rar'): 'zip.png',
            ends_with('.zip'): 'zip.png',
            ends_with('.gz'): 'zip.png',
            ends_with('.tar'): 'zip.png',
            ends_with('.tar.gz'): 'zip.png',
            ends_with('.tar.xz'): 'zip.png',
            ends_with('.sh'): 'sh.png',
            ends_with('.html'): 'html.png',
        }.get(True, 'file.png')

        file_image = Image.open('./components/assets/img/' + name)
        file_image = file_image.resize((100, 100))
        return CTkImage(file_image, size=(100, 100))

    def create(self, name):
        self._name = name
        self._path = path.join(self._path, name)
        run(['touch', self._path])

    def open_file(self):
        # print(self._path)
        # run(['xdg-open', self._path])
        startfile(self._path)
        

    def cut(self, new_path):
        run(['mv', self._path, new_path])
        self._path = path.join(new_path, self._name)

    def copy(self, new_path):
        run(['cp', self._path, new_path])
        self._path = path.join(new_path, self._name)

    def delete(self):
        run(['rm', '-rf', self._path])

    def change_name(self, new_name):
        self._name = new_name
        old_dir, old_base = path.split(self._path)
        new_path = path.join(old_dir, new_name)

        rename(self._path, new_path)
        self._path = new_path

    def __str__(self) -> str:
        return self._name
