import customtkinter as ctk
import tkinterweb

def abrir_google(principal):
    root = ctk.CTkToplevel(master=principal)
    root.attributes('-topmost', 1)
    root.title("Google Window")
    web_view = tkinterweb.HtmlFrame(root)
    web_view.load_website("https://www.google.com")  # Carga un sitio web
    web_view.pack(fill="both", expand=True)
    root.mainloop() 