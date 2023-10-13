import pywifi
import time


def obtener_potencia_red_actual():
    wifi = pywifi.PyWiFi() # Inicializar la instancia de PyWiFi
    iface = wifi.interfaces() # Obtener la primera interfaz WiFi disponible

    while True:
        for i in iface:
            estatus = i.status() # Obtener el estado la interfaz WiFi
        if estatus == pywifi.const.IFACE_CONNECTED:
            name = i.network_profiles()[0].ssid
            red = list(filter(lambda x: x.ssid == name, i.scan_results()))[0]
            print(f'Potencia de señal de {red.ssid}: {convertir_dBm_a_porcentaje(red.signal)}%')

        time.sleep(1)


def convertir_dBm_a_porcentaje(potencia_dBm):
    potencia_maxima = -40
    potencia_minima = -100

    # Asegurarse de que la potencia esté dentro del rango de máximo y mínimo
    potencia_dBm = max(potencia_minima, min(potencia_maxima, potencia_dBm))

    # Calcular el porcentaje de potencia
    porcentaje = round((potencia_dBm - potencia_minima) /
    (potencia_maxima - potencia_minima) * 100, 1)

    return porcentaje


obtener_potencia_red_actual()