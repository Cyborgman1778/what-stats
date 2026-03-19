import pandas as pd
from typing import Dict, Any

#Dividimos los calculos de las diferentes estadisticas en diferentes funciones para un codigo mas limpo



def _get_basic_stats(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula mensajes totales y participantes."""
    return {
        "total_messages": len(chat_df),
        "participants": chat_df['Author'].dropna().unique().tolist(),
        "n_participants": chat_df['Author'].nunique()
    }

def analyze_chat_data(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Recibe un DataFrame de Pandas generado a partir de un chat de WhatsApp
    y calcula estadísticas (RF-04).
    
    Args:
        chat_df (pd.DataFrame): El DataFrame con las columnas Date, Time, Author, Message, Datetime.
        
    Returns:
        Dict[str, Any]: Un diccionario con las estadísticas calculadas, listo para
                        ser devuelto por la API en formato JSON (RF-05).
    """
    # 1. Comprobación de seguridad: Si el DataFrame está vacío, devolvemos ceros
    if chat_df.empty:
        return {
            "total_messages": 0,
            "total_users": 0,
            "participants": [],
            "message": "El chat analizado no contiene mensajes válidos."
        }

    # 2. Contador total de mensajes
    # len(df) nos da el número de filas del DataFrame, que equivale al número de mensajes
    total_messages, participants, total_users = _get_basic_stats(chat_df)

    # 3. Análisis de Usuarios (Participantes)
    # df['Author'].unique() extrae los nombres únicos de la columna 'Author'
    # .dropna() elimina los valores nulos (por ejemplo, mensajes del sistema de WhatsApp)
    # .tolist() lo convierte a una lista normal de Python para que FastAPI pueda serializarlo a JSON
    participants = chat_df['Author'].dropna().unique().tolist()
    
    # Contamos cuántos usuarios únicos hay
    total_users = len(participants)

    # 4. Construimos y devolvemos el diccionario de resultados (RF-05)
    return {
        "total_messages": total_messages,
        "total_users": total_users,
        "participants": participants,
        "status": "success"
    }