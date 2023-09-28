import speech_recognition as sr
import keyboard
import Interfaz_grafica as gui

recognizer = sr.Recognizer()

def start_listening():
    with sr.Microphone() as source:
        print("Escuchando... Presiona Ctrl+M nuevamente para detener.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Has dicho: {}".format(text))
            if text == 'open system':
                print("Bienvenido administrador")
                ven
                


        except sr.UnknownValueError:
            print("No se pudo entender lo que dijiste")
        except sr.RequestError as e:
            print("Error en la solicitud a Google Speech Recognition; {0}".format(e))

# Función que se ejecutará cuando se presione una tecla
def on_key_event(keyboard_event):
    if keyboard_event.event_type == keyboard.KEY_DOWN and keyboard_event.name == 'm':
        if keyboard.is_pressed('ctrl'):
            start_listening()

# Registra la función on_key_event para los eventos de presionar una tecla
keyboard.hook(on_key_event)

# Mantén el programa en ejecución
keyboard.wait('esc')  # Espera hasta que se presione la tecla "esc" para salir del programa


