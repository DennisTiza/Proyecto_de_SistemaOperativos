from customtkinter import *
from tkinter import filedialog, Menu, Listbox
import pygame

class Reproductor:
    def agregar(self):
        canciones = filedialog.askopenfilenames(initialdir="/", title="Selecciona una canción", filetypes=(("Archivos mp3", "*.mp3"), ("all files", "*.*")))
        for cancion in canciones:
            cancion = cancion.replace("C:/Users/Usuario/Downloads/", "")
            cancion = cancion.replace(".mp3", "")
            self.pantalla.insert(END, cancion)

    def play(self):
        cancion = self.pantalla.get(ACTIVE)
        cancion = f'{cancion}.mp3'
        pygame.mixer.music.load(cancion)
        pygame.mixer.music.play(loops=0)

    def stop(self):
        pygame.mixer.music.stop()
        self.pantalla.selection_clear(ACTIVE)

    def siguiente(self):
        proxima = self.pantalla.curselection()
        if proxima:
            proxima = proxima[0] + 1
            cancion = self.pantalla.get(proxima)
            cancion = f'{cancion}.mp3'
            pygame.mixer.music.load(cancion)
            pygame.mixer.music.play(loops=0)
            self.pantalla.selection_clear(0, END)
            self.pantalla.activate(proxima)
            self.pantalla.selection_set(proxima, last=None)

    def anterior(self):
        anterior = self.pantalla.curselection()
        if anterior:
            anterior = anterior[0] - 1
            cancion = self.pantalla.get(anterior)
            cancion = f'{cancion}.mp3'
            pygame.mixer.music.load(cancion)
            pygame.mixer.music.play(loops=0)
            self.pantalla.selection_clear(0, END)
            self.pantalla.activate(anterior)
            self.pantalla.selection_set(anterior, last=None)

    def pausar(self):
        global pausa
        pausa = not pausa
        if pausa:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def borrar(self):
        self.pantalla.delete(ANCHOR)
        pygame.mixer.music.stop()

    def borrar_todo(self):
        self.pantalla.delete(0, END)
        pygame.mixer.music.stop()

    def __init__(self, root):
        pygame.mixer.init()
        global pausa
        pausa = True

        self.pantalla = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
        self.pantalla.pack(pady=20)

        # Botones
        botones = CTkFrame(root)
        botones.pack()

        ante = CTkButton(botones, text="Anterior", command=self.anterior)
        ante.grid(row=0, column=0, padx=10)

        reproducir = CTkButton(botones, text="Reproducir", command=self.play)
        reproducir.grid(row=0, column=1, padx=10)

        pausa_button = CTkButton(botones, text="Pausa", command=self.pausar)
        pausa_button.grid(row=0, column=2, padx=10)

        sigui = CTkButton(botones, text="Siguiente", command=self.siguiente)
        sigui.grid(row=0, column=3, padx=10)

        # Menu
        menubar = Menu(root)
        root.config(menu=menubar)
        añadir_cancion = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Añadir", menu=añadir_cancion)
        añadir_cancion.add_command(label="Añadir canción", command=self.agregar)

        remover = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Borra canciones", menu=remover)
        remover.add_command(label="Borrar una canción de la pantalla", command=self.borrar)
        remover.add_command(label="Borrar todas las canciones de la pantalla", command=self.borrar_todo)


def init(principal):
    root = CTkToplevel(master=principal)
    root.title("Reproductor de música")
    root.attributes('-topmost', 1)
    musica = Reproductor(root)
    principal.mainloop()
