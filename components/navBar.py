from customtkinter import *
from PIL import Image

from .home import Home
from .folder import Folder
from .file import File


class NavBarLeft(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=100, height=45, **kwargs)
        self.parent = master.parent
        self.listdir = master.listdir
        self.content()
        self.configure()

    def configure(self):
        self.grid(row=0, column=0, sticky='nsew', padx=10, pady=(5, 0))
        self.rowconfigure(0, weight=1)
        return super().configure()

    def content(self):
        actions = {
            'back': lambda: print(),
            'next': lambda: print(),
            'home': self.home
        }

        for i, (k, v) in enumerate(actions.items()):
            self.action(k, v, col=i)
            self.grid_columnconfigure(i, weight=1)

        menu = CTkOptionMenu(self, width=7, values=[
                             'Folder', 'File'], command=lambda name: self.add_element(name))
        menu.set('Add')
        menu.bind('<Return>', lambda event: self.add_element(event))
        menu.grid(row=0, column=4,  sticky='nsew', padx=(0, 5), pady=5)

    def action(self, icon_name, func, col=0):
        img_icon = Image.open(f'./components/assets/img/{icon_name}.png')
        print(img_icon)
        img_icon = img_icon.resize((20, 20))
        img_icon = CTkImage(img_icon)
        back = CTkButton(self, image=img_icon, text='', bg_color='gray17', fg_color='gray17', width=10, height=10)
        back.grid(row=0, column=col, sticky='nsew', padx=(0, 10), pady=5)
        back.bind('<Button-1>', lambda event: func())

    def home(self):
        Home(self.master, self.parent, self.listdir)

    def add_element(self, name):
        element = CTkInputDialog(
            text=f'Enter the name of the {name.lower()}', title='Add')

        new_name = element.get_input()
        if len(new_name) < 3:
            top_level = CTkToplevel(self, width=200, height=150)
            label = CTkLabel(top_level,
                             text='Nombre no permitido, debe tener al menos 3 caracteres')
            label.pack(padx=20, pady=20)
            top_level.focus()
            element.destroy()

        elif name == 'Folder':
            self.parent = self.master.parent
            self.parent.create(new_name)
        elif name == 'File':
            File(self.parent._path).create(new_name)

        self.parent = Folder(self.parent._path)
        self.master.update_home(self.parent, self.parent.list_content)
        self.master.update_aside()


class NavBarRigth(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=100, height=50, **kwargs)
        self.parent = master.parent
        self.listdir = master.listdir
        self.configure()

    def configure(self):
        self.grid(row=0, column=1, sticky='nsew', padx=10, pady=(5, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.content()
        return super().configure()

    def content(self):
        input = CTkEntry(self, width=40, bg_color='gray17', fg_color='gray17')
        input.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        input.bind('<Return>', lambda event: self.search(event, input))

        img_icon = Image.open('./components/assets/img/search.png')
        img_icon = img_icon.resize((20, 20))
        img_icon = CTkImage(img_icon)
        search = CTkButton(self, image=img_icon, text='',
                           bg_color='gray17', fg_color='gray17', width=10, height=10)
        search.grid(row=0, column=1, sticky='nsew', padx=(0, 10), pady=5)

    def search(self, event, input):
        lst_found = []

        def search_depth(listdir: list):
            for i in listdir:
                if i._name.lower().startswith(input.get().lower()):
                    lst_found.append(i)

                if isinstance(i, Folder):
                    search_depth(i.list_content)

        if input.get():
            self.listdir = Folder(self.parent._path).list_content
            search_depth(self.listdir)

        Home(self.master, self.parent, lst_found and lst_found or self.listdir)
