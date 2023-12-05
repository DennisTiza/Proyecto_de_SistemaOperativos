import customtkinter as ctk
from tkinter import END
import math



def init(principal):
    root = ctk.CTkToplevel(master=principal)
    root.attributes('-topmost', 1)
    calculadora = Calculadora(root)
    principal.mainloop()


#Funciones
class Calculadora:
    i = 0
    def click_boton(self, valor, e_texto):
        global i
        if valor == "√(":
            i+=1
        if valor == "^(":
            i+=1
        e_texto.insert(i, valor)
        i += 1

    def borrar(self ,e_texto):
        e_texto.delete(0, END)
        i = 0

    def hacer_operacion(self,e_texto):
        global i
        ecuacion = e_texto.get()

        # Verificar si la letra 'e' está presente en la ecuación
        if 'e' in ecuacion:
            ecuacion = ecuacion.replace('e', str(math.e))  # Reemplazar 'e' con el número de Euler
            i+=16
        if 'π' in ecuacion:
            ecuacion = ecuacion.replace('π', str(math.pi)) # Reemplazar 'π' con el número pi
            i+=16
        if '√(' in ecuacion:
            ecuacion = ecuacion.replace('√(', 'math.sqrt(')
            i+= len(ecuacion)+1
    
        if '^(' in ecuacion:
            ecuacion = ecuacion.replace('^(', '**(')
            i+= len(ecuacion)+1

        if ')!' in ecuacion:
            ecuacion = ecuacion.replace(')!', ')')
            if '(' in ecuacion:
                ecuacion = ecuacion.replace('(', 'math.factorial(')
            i+= len(ecuacion)+1

        try:
            resultado = eval(ecuacion)
            e_texto.delete(0, END)
            e_texto.insert(0, resultado)
        except Exception as e:
            e_texto.delete(0, END)
            e_texto.insert(0, "Error")  # Manejar errores de evaluación
    

    def __init__(self, ventana):
        global i
        i = 0
        self.ventana = ventana
        ventana.title("Calculadora")

        e_texto = ctk.CTkEntry(master=ventana, height=40, width=250)
        e_texto.grid(row = 0, column = 0, columnspan = 5, padx = 5, pady = 5)
        boton1 = ctk.CTkButton(master=ventana, text = "1", width= 40, height = 40, command = lambda: self.click_boton(1, e_texto))
        boton2 = ctk.CTkButton(master=ventana, text = "2", width= 40, height = 40, command = lambda: self.click_boton(2, e_texto))
        boton3 = ctk.CTkButton(master=ventana, text = "3", width= 40, height = 40, command = lambda: self.click_boton(3, e_texto))
        boton4 = ctk.CTkButton(master=ventana, text = "4", width= 40, height = 40, command = lambda: self.click_boton(4, e_texto))
        boton5 = ctk.CTkButton(master=ventana, text = "5", width= 40, height = 40, command = lambda: self.click_boton(5, e_texto))
        boton6 = ctk.CTkButton(master=ventana, text = "6", width= 40, height = 40, command = lambda: self.click_boton(6,e_texto))
        boton7 = ctk.CTkButton(master=ventana, text = "7", width= 40, height = 40, command = lambda: self.click_boton(7, e_texto))
        boton8 = ctk.CTkButton(master=ventana, text = "8", width= 40, height = 40, command = lambda: self.click_boton(8, e_texto))
        boton9 = ctk.CTkButton(master=ventana, text = "9", width= 40, height = 40, command = lambda: self.click_boton(9, e_texto))
        boton0 = ctk.CTkButton(master=ventana, text = "0", width= 80, height = 40, command = lambda: self.click_boton(0,e_texto))

        boton_borrar = ctk.CTkButton(master=ventana, text = "AC", width= 40, height = 40, command = lambda: self.borrar(e_texto))
        boton_parentesis1 = ctk.CTkButton(master=ventana, text = "(", width= 40, height = 40, command = lambda: self.click_boton("(", e_texto))
        boton_parentesis2 = ctk.CTkButton(master=ventana, text = ")", width= 40, height = 40, command = lambda: self.click_boton(")", e_texto))
        boton_punto = ctk.CTkButton(master=ventana, text = ".", width= 40, height = 40, command = lambda: self.click_boton(".", e_texto))

        boton_div = ctk.CTkButton(master=ventana, text = "/", width= 40, height = 40, command = lambda: self.click_boton("/", e_texto))
        boton_mult = ctk.CTkButton(master=ventana, text = "x", width= 40, height = 40, command = lambda: self.click_boton("*", e_texto))
        boton_sum = ctk.CTkButton(master=ventana, text = "+", width= 40, height = 40, command = lambda: self.click_boton("+", e_texto))
        boton_rest = ctk.CTkButton(master=ventana, text = "-", width= 40, height = 40, command = lambda: self.click_boton("-", e_texto))
        boton_e = ctk.CTkButton(master=ventana, text = "e", width= 40, height = 40, command = lambda: self.click_boton("e", e_texto))
        boton_pi = ctk.CTkButton(master=ventana, text = "π", width= 40, height = 40, command = lambda: self.click_boton("π", e_texto))
        boton_raiz = ctk.CTkButton(master=ventana, text = "√", width= 40, height = 40, command = lambda: self.click_boton("√(", e_texto))
        boton_exp = ctk.CTkButton(master=ventana, text = "^", width= 40, height = 40, command = lambda: self.click_boton("^(", e_texto))
        boton_fact = ctk.CTkButton(master=ventana, text = "!", width= 40, height = 40, command = lambda: self.click_boton(")!", e_texto))

        boton_igual = ctk.CTkButton(master=ventana, text = "=", width= 40, height = 40, command = lambda: self.hacer_operacion(e_texto))

        #Agregar botones en pantalla

        boton_e.grid(row = 5, column = 0, padx = 5, pady = 5)
        boton_pi.grid(row = 4, column = 0, padx = 5, pady = 5)
        boton_raiz.grid(row = 3, column = 0, padx = 5, pady = 5)
        boton_exp.grid(row = 2, column = 0, padx = 5, pady = 5)
        boton_fact.grid(row = 1, column = 0, padx = 5, pady = 5)

        boton_borrar.grid(row = 1, column = 1, padx = 5, pady = 5)
        boton_parentesis1.grid(row = 1, column = 2, padx = 5, pady = 5)
        boton_parentesis2.grid(row = 1, column = 3, padx = 5, pady = 5)
        boton_div.grid(row = 1, column = 4, padx = 5, pady = 5)

        boton7.grid(row= 2, column = 1, padx = 5, pady = 5)
        boton8.grid(row= 2, column = 2, padx = 5, pady = 5)
        boton9.grid(row= 2, column = 3, padx = 5, pady = 5)
        boton_mult.grid(row= 2, column = 4, padx = 5, pady = 5)

        boton4.grid(row= 3, column = 1, padx = 5, pady = 5)
        boton5.grid(row= 3, column = 2, padx = 5, pady = 5)
        boton6.grid(row= 3, column = 3, padx = 5, pady = 5)
        boton_sum.grid(row= 3, column = 4, padx = 5, pady = 5)

        boton1.grid(row= 4, column = 1, padx = 5, pady = 5)
        boton2.grid(row= 4, column = 2, padx = 5, pady = 5)
        boton3.grid(row= 4, column = 3, padx = 5, pady = 5)
        boton_rest.grid(row= 4, column = 4, padx = 5, pady = 5)

        boton0.grid(row= 5, column = 1, columnspan = 2, padx = 5, pady = 5)
        boton_punto.grid(row= 5, column = 3, padx = 5, pady = 5)
        boton_igual.grid(row= 5, column = 4, padx = 5, pady = 5)


        ventana.mainloop()