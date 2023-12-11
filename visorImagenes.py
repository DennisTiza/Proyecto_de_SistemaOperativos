import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image, ImageEnhance, ImageTk

class VisualizadorImagenes:
    def __init__(self, root, ruta):
        self.root = root
        self.root.title("Visor de Imágenes")
        self.root.geometry("750x620")

        self.images = []
        self.current_image_index = 0

        self.frame1 = ctk.CTkFrame(master=root, width=650, height=450)
        self.frame1.pack(pady=10)

        self.image_label = ctk.CTkLabel(master=self.frame1, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.frame = ctk.CTkFrame(master=root)
        self.frame.pack()
        
        self.brillo = ctk.CTkLabel(master=self.frame, text="Brillo")
        self.brillo.grid(row=0, column=0, padx=5)
        self.brillo_slider = ctk.CTkSlider(master=self.frame, from_=0.1, to=2, orientation="horizontal", command=self.modificarbrillo)
        self.brillo_slider.set(1.0)
        self.brillo_slider.grid(row=1, column=0, padx=10)


        self.opacidad = ctk.CTkLabel(master=self.frame, text="Opacidad")
        self.opacidad.grid(row=0, column=1, padx=5)
        self.opacidad_slider = ctk.CTkSlider(master=self.frame, from_=0.1, to=1.0, orientation="horizontal", command=self.modificaropacidad)
        self.opacidad_slider.set(1.0)
        self.opacidad_slider.grid(row=1, column=1, padx=10)

        self.cargarboton = ctk.CTkButton(master=self.frame, text="Cargar Imagen", command=self.cargarimagen)
        self.cargarboton.grid(row=2, column=0, columnspan=2, pady=10)

        self.anteriorboton = ctk.CTkButton(master=self.frame, text="Anterior", command=self.imagenprevia)
        self.anteriorboton.grid(row=3, column=0, pady=7)

        self.siguienteboton = ctk.CTkButton(master=self.frame, text="Siguiente", command=self.siguienteimagen)
        self.siguienteboton.grid(row=3, column=1, pady=7)

        self.image = None
        self.display_image = None

        if ruta != "":
            self.images.append(Image.open(ruta))
            self.resize_large_image(self.images[0])
            self.display_current_image()

    def cargarimagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.ppm *.pgm *.tif")])

        if file_path:
            image = Image.open(file_path)
            self.resize_large_image(image)
            self.images.append(image)
            self.current_image_index = len(self.images) - 1
            self.display_current_image()

    def resize_large_image(self, image, max_size=(650, 450)):
        width, height = image.size
        if width > max_size[0] or height > max_size[1]:
            image.thumbnail(max_size)

    def imagenprevia(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_current_image()

    def siguienteimagen(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.display_current_image()

    def display_current_image(self):
        self.image = self.images[self.current_image_index]
        self.display_image = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.display_image)
        self.brillo_slider.set(1.0)
        self.opacidad_slider.set(1.0)

    def modificarbrillo(self, value):
        if self.image:
            brightness = float(value)
            enhanced_image = ImageEnhance.Brightness(self.image).enhance(brightness)
            enhanced_photo = ImageTk.PhotoImage(enhanced_image)
            self.image_label.configure(image=enhanced_photo)
            self.image_label.image = enhanced_photo

    def modificaropacidad(self, value):
        if self.image:
            opacity = int(float(value) * 255)
            image = self.image.copy()
            image.putalpha(opacity)
            opacity_photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=opacity_photo)
            self.image_label.image = opacity_photo

def init(principal):
    rutanula = ""
    root = ctk.CTkToplevel(master=principal)
    root.attributes('-topmost', 1)
    viewer = VisualizadorImagenes(root, rutanula)
    principal.mainloop()

def cargar(principal, ruta):
    root = ctk.CTkToplevel(master=principal)
    root.attributes('-topmost', 1)
    viewer = VisualizadorImagenes(root, ruta)