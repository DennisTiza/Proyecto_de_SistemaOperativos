import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import imutils

class VisorDeVideo:

    def __init__(self, master):
        self.cap = None
        self.paused = False

        self.btnVisualizador = ctk.CTkButton(master, text="Cargar Video", command=self.cargarvideo)
        self.btnVisualizador.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.lblInfo1 = ctk.CTkLabel(master, text="Video seleccionado:")
        self.lblInfo1.grid(row=1, column=0)

        self.lblInfoVideo = ctk.CTkLabel(master, text="Aún no se ha seleccionado ningún video")
        self.lblInfoVideo.grid(row=1, column=1)
        
        self.lblvideo = ctk.CTkLabel(master, text="", width=650, height=400)
        self.lblvideo.grid(row=2, columnspan=2)

        self.btnPause = ctk.CTkButton(master, text="Pausar", command=self.toggle_pause)
        self.btnPause.grid(row=3, column=0, padx=5, pady=5, columnspan=2)


    def visualizar(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = imutils.resize(frame, width=650)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(im)

                self.lblvideo.configure(image=img)
                self.lblvideo.image = img

                if not self.paused:
                    self.lblvideo.after(10, self.visualizar)
            else:
                self.lblInfoVideo.configure(text="No se ha seleccionado ningún video")
                self.lblvideo.image = ""
                self.cap.release()



    def cargarvideo(self):
        if self.cap is not None:
            self.lblvideo.image = ""
            self.cap.release()
            self.cap = None
            self.paused = False
            self.btnPause.configure(text="Pausar")
        videoPath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if len(videoPath) > 0:
            self.lblInfoVideo.configure(text=videoPath)
            self.cap = cv2.VideoCapture(videoPath)
            self.visualizar()
        else:
            self.lblInfoVideo.configure(text="No se ha seleccionado ningún video")

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.btnPause.configure(text="Reanudar")
        else:
            self.btnPause.configure(text="Pausar")
            self.visualizar()
            

def init(principal):
    root = ctk.CTkToplevel(master=principal)
    root.title("Visor de videos")
    root.attributes('-topmost', 1)
    viewer = VisorDeVideo(root)
    principal.mainloop()