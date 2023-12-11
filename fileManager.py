from customtkinter import *

from components.navBar import NavBarLeft, NavBarRigth
from components.folder import Folder
from components.aside import Aside
from components.home import Home

class FileManager(CTkToplevel):
    def __init__(self, current_dir=os.getcwd()):
        super().__init__()
        self.current_dir = current_dir
        self.parent = Folder(self.current_dir)
        self.listdir = self.parent.list_content
        self.main()

    def configure(self):
        self.title('File Manager')
        self.attributes('-topmost', 1)
        set_appearance_mode('System')
        set_default_color_theme("blue")
        self.minsize(1000, 500)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        NavBarLeft(self)
        NavBarRigth(self)
        self.update_aside()
        self.update_home()

    def update_home(self, parent=None,  listdir=None):
        parent = parent and parent or self.parent
        listdir = listdir and listdir or self.listdir
        Home(self, parent, listdir)

    def update_aside(self):
        self.listdir = Folder(self.current_dir).list_content
        Aside(master=self, listdir=self.listdir)

    def main(self):
        self.configure()
        self.mainloop()

def init(user):
    if user['rol'] == 'admin':
        filemanger = FileManager("Usuarios")
    filemanger = FileManager("Usuarios/"+str(user['id']))
