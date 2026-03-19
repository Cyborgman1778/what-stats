import pandas as pd
import io
import zipfile
from typing import List, Dict, Tuple
from app.utils.regex_patterns import detect_message_parts

"""
Params:
file_bytes -> el archivo mismo (debe estar en bytes, asi que hay que usar file = UploadFile de FastAPI y luego file.read() para obtener los bytes)
filename -> el nombre del archivo 
"""
def extract_text_from_memory(file_bytes: bytes, filename: str) -> str:
    """
    Lee los bytes del archivo subido. Si es un ZIP, busca el .txt dentro y lo extrae en RAM.
    Si es directamente un .txt, lo decodifica.
    """
    if filename.endswith(".zip"):
        # Leemos el ZIP directamente desde los bytes en memoria
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            # Buscamos el primer archivo .txt dentro del zip que contenga la palabra "chat"
            txt_filename = next((name for name in z.namelist() if name.lower().endswith(".txt") and "chat" in name.lower()), None)
            if not txt_filename:
                raise ValueError("No se encontró ningún archivo de chat dentro del .zip")
            
            # Leemos el contenido del .txt
            with z.open(txt_filename) as f:
                return f.read().decode("utf-8")
                
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8")
    else:
        raise ValueError("Formato de archivo no soportado. Debe ser .txt o .zip")

def parse_chat_to_dataframe(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """
    Convierte los bytes del archivo subido en un DataFrame de Pandas estructurado,
    gestionando los mensajes multilínia.
    """
    # 1. Obtenemos el texto en bruto (todo en memoria RAM)
    raw_text = extract_text_from_memory(file_bytes, filename)
    
    parsed_data: List[Dict[str, str]] = []
    
    # 2. Leemos línea por línea
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
            
        parts = detect_message_parts(line)
        #TODO: falta añadir la opcion de que sea un mensaje del sistema
        if parts:
            # Es el inicio de un nuevo mensaje (hizo match con la Regex)
            date, time, author, message = parts
            parsed_data.append({
                "Date": date,
                "Time": time,
                "Author": author.strip(),
                "Message": message.strip()
            })
        else:
            # No hizo match. Esto significa que es un mensaje multilínia.
            # Se lo añadimos al último mensaje registrado.
            if parsed_data:
                parsed_data[-1]["Message"] += f"\n{line}"
                
    # 3. Convertimos la lista de diccionarios a un DataFrame de Pandas
    df = pd.DataFrame(parsed_data)
    
    # Opcional (pero muy recomendado para Pandas): Convertir a datetime
    if not df.empty:
        # Combinamos Date y Time en una sola columna temporal real 
        df['Timestampt'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format="mixed", dayfirst=True)
    
    return df