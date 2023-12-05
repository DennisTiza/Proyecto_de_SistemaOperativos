from tkinter import Menu
from customtkinter import *

from components.folder import Folder
from components.file import File


class Home(CTkScrollableFrame):
    list_to_paste = []

    def __init__(self, master, parent: Folder, listdir: list):
        super().__init__(master, width=800, height=200)
        self.listdir: list[Folder] = listdir
        self.master = master
        self.parent = parent
        self.menu = None
        self.entry = None
        self.cut = False
        self.configure()
        self.load_content()

    def configure(self, **kwargs):
        self.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.bind('<ButtonPress-1>', lambda event: self.close_menu())
        self.bind('<Button-3>',
                  lambda event: self.options(event, self.parent))
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        self.propagate(False)
        return super().configure(**kwargs)

    def content(self, listdir=None):
        if listdir:
            list_sort = sorted(listdir, key=lambda x: isinstance(x, File))

            for i, content in enumerate(list_sort):
                row, col = divmod(i, 5)
                element = CTkButton(self, text=content._name[:20], image=content._image, compound='top',
                                    width=120, height=100, bg_color='gray17', fg_color='gray17')
                element.grid(row=row, column=col,
                             sticky='nsew', padx=10, pady=5)
                element.bind('<Button-1>', lambda event,
                             c=content: self.open_element(event, c))
                element.bind('<Button-3>', lambda event,
                             c=content: self.options(event, c))

        else:
            element = CTkLabel(self, text='No hay elementos en esta carpeta',
                               bg_color='gray17', fg_color='gray17', font=('Arial', 20))
            element.grid(row=0, column=2, sticky='nsew', padx=10, pady=5)

    def options(self, event, element):
        self.close_menu()
        self.menu = Menu(self, borderwidth=1, tearoff=0, takefocus=0)
        self.menu.configure(bg='gray17', bd=0, relief='solid', border=1)
        self.menu.configure(font=('Arial', 15), activebackground='gray')
        self.menu.configure(activeforeground='white', foreground='white')

        self.menu.add_command(label='Abrir',
                              command=lambda: self.open_element(None, element))
        self.menu.add_separator()
        self.menu.add_command(label='Cortar',
                              command=lambda: self.cut_element(element))
        self.menu.add_command(label='Copiar',
                              command=lambda: self.copy_element(element))
        self.menu.add_command(label='Pegar',
                              command=lambda: self.paste_element(element, self.cut))
        self.menu.add_command(label="Renombrar",
                              command=lambda: self.rename_file(event, element))
        self.menu.add_separator()
        self.menu.add_command(label='Eliminar',
                              command=lambda: self.delete(element))
        self.menu.post(event.x_root, event.y_root)

    def close_menu(self):
        if self.menu:
            self.menu.destroy()

    def open_element(self, event, element):
        if isinstance(element, Folder):
            self.change_dir(None, element)
        else:
            element.open_file()

    def cut_element(self, element):
        self.cut = True
        self.list_to_paste.append(element)

    def copy_element(self, element):
        self.cut = False
        self.list_to_paste.append(element)

    def paste_element(self, element, cut=False):
        for item in self.list_to_paste:
            if cut:
                item.cut(element._path)
            else:
                item.copy(element._path)

        self.list_to_paste = []
        self.master.update_aside()
        self.update(self.parent)

    def delete(self, element):
        element.delete()
        self.master.update_aside()
        self.update(self.parent)

    def rename_file(self, event, element):
        self.close_entry()
        self.close_menu()
        row, col = 0, 0

        for i in range(len(self.winfo_children())):
            item = self.winfo_children()[i]

            if item.cget('text').startswith(element._name):
                row, col = item.grid_info()['row'], item.grid_info()['column']
                break

        self.entry = CTkEntry(self, width=100, bg_color='gray17',
                              text_color='white', border_width=1)
        self.entry.insert(0, element._name)
        self.entry.bind('<Return>', lambda event, e=self.entry,
                        c=element: self.change_name(item, e, c))
        self.entry.bind('<Escape>', lambda event: self.close_entry(event))
        self.entry.grid(row=row, column=col, padx=10, pady=0, sticky='s')
        self.entry.focus_set()

    def change_name(self, item, entry, element):
        if len(entry.get()) >= 3:
            element.change_name(entry.get())

        self.close_entry()
        self.load_content()
        self.master.update_aside()

    def close_entry(self, event=None):
        if self.entry:
            self.entry.destroy()

    def change_dir(self, event, folder: Folder):
        self.update(folder)

    def load_content(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.content(self.listdir)

    def update(self, folder: Folder):
        self.parent = Folder(folder._path)
        self.listdir = self.parent.list_content
        self.load_content()
