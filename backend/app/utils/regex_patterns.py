import re

# Se necesitan dos patrones regex porque el formato de exportacion es diferente en Android y en IOS:
#TODO: se deberia ahcer otro regex para detectar mensajes del sistema, OJO que son diferentes en IOS y android

# Patrón para Android: "dd/mm/yyyy, hh:mm - Autor: Mensaje"
# Nota: La fecha puede venir con 2 o 4 dígitos para el año.
ANDROID_PATTERN = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)$")

# Patrón para iOS: "[dd/mm/yyyy, hh:mm:ss] Autor: Mensaje"
# Nota: iOS incluye corchetes y los segundos en la hora.
IOS_PATTERN = re.compile(r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.*)$")

def detect_message_parts(line: str):
    """
    Intenta hacer match con los formatos conocidos.
    Retorna (fecha, hora, autor, mensaje) si es exitoso, o None si es una línea de continuación.
    """
    # Probamos iOS primero
    match = IOS_PATTERN.match(line)
    if match:
        return match.groups()
    
    # Si no es iOS, probamos Android
    match = ANDROID_PATTERN.match(line)
    if match:
        return match.groups()
    
    return None