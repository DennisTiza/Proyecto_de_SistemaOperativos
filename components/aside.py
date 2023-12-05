from tkinter import ttk
from customtkinter import *

from components.folder import Folder
from components.file import File
from components.home import Home


class Aside(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=220, height=200)
        self.listdir = kwargs['listdir']
        self.parent = master
        self.configure()

    def configure(self, **kwargs):
        self.config_treeview()
        self.load_content()
        self.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        return super().configure(**kwargs)

    def config_treeview(self):
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview.Heading", font=(
            "TkDefaultFont", 15, "bold"))
        treestyle.configure("Treeview", font=("TkDefaultFont", 11))
        treestyle.configure("Treeview", background='gray17',
                            foreground='#DCE4EE', fieldbackground='gray17', borderwidth=0)
        treestyle.map('Treeview', background=[('selected', 'gray17')], foreground=[
                      ('selected', '#1F6AA5')])

        self.tree = ttk.Treeview(
            self, height=50, columns=('fullpath',), show='tree')
        self.tree.column('#0', width=220, stretch=True)
        self.tree.column('fullpath', stretch=True, width=0)
        self.tree.grid(padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.pack()

    def tree_folder(self, directory_list, parent=''):
        def add_directories(parent, path):
            files = []

            for item in path:
                if isinstance(item, Folder):
                    item_id = self.tree.insert(
                        parent, 'end', text=item, open=False, tags=([item._path, True]))
                    add_directories(item_id, item.list_content)

                if isinstance(item, File):
                    files.append(item)

            for item in files:
                self.tree.insert(parent, 'end', text=item,
                                 open=False, tags=([item._path, False]))

        add_directories(parent, directory_list)

        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def on_tree_select(self, event):
        item = event.widget.focus()
        item = event.widget.item(item)
        path, is_folder = item['tags']

        if is_folder == 'True':
            listdir = Folder(path).list_content
            Home(self.parent, Folder(path), listdir=listdir)

        else:
            File(path).open_file()

    def load_content(self):
        self.tree_folder(self.listdir)
