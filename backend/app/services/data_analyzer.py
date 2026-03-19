import pandas as pd
from typing import Dict, Any

#Dividimos los calculos de las diferentes estadisticas en diferentes funciones para un codigo mas limpo


def _get_basic_stats(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula mensajes totales y participantes."""
    return {
        "total_messages": len(chat_df),

        # chat_df['Author'].unique() extrae los nombres únicos de la columna 'Author'
        # .dropna() elimina los valores nulos (por ejemplo, mensajes del sistema de WhatsApp)
        # .tolist() lo convierte a una lista normal de Python para que FastAPI pueda serializarlo a JSON
        "participants": chat_df['Author'].dropna().unique().tolist(),
        "n_participants": chat_df['Author'].nunique()
    }

def _get_messages_per_user(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula cuantos mensajes envia cada usuario"""
    return {
        "n_messages_per_user": chat_df['Author'].value_counts().to_dict()
    }

def _get_hot_hours(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Cuenta los mensajes que hay en cada hora del dia"""

    # 1. chat_df['Timestampt'].dt.hour extrae solo la hora (0 a 23) de cada mensaje.
    # 2. value_counts() cuenta cuántos mensajes hay en cada hora.
    # 3. sort_index() ordena el resultado de 0 a 23 (vital para que el gráfico salga ordenado).
    # 4. to_dict() lo convierte al formato JSON.
    messages_per_hour = chat_df['Timestampt'].dt.hour.value_counts().sort_index().to_dict()

    #ponemos la fecha en formato legible
    hot_hours = {
        f"{hour:02d}:00": count for hour, count in messages_per_hour.items()
    }

    return {
        "hot_hours": hot_hours
    }

#TODO: Añadir logica para filtrar por usuario
def _get_calendar_stats(chat_df: pd.DataFrame, top_n: int = 10) -> Dict[str, Any]:
    """Obtener numero de mensajes por fechas (dia/mes/año, mes/año, año)"""

    # Obtenemos los mensajes por fechas (dia/mes/año), lo ordenamos y hacemos la fecha legible
    day = chat_df['Timestampt'].dt.date.value_counts().sort_index()
    messages_per_day = {date.strftime("%d/%m/%Y"): count for date, count in day.items()}

    # Obtenemos los mensajes por meses (mes/año), lo ordenamos y hacemos la fecha legible
    month = chat_df['Timestampt'].dt.to_period('M').value_counts().sort_index()
    messages_per_month = {period.strftime('%m/%Y'): count for period, count in month.items()}

    # Obtenemos los mensajes por años, lo ordenamos y hacemos la fecha legible
    year = chat_df['Timestampt'].dt.year.value_counts().sort_index()
    messages_per_year = {str(period): count for period, count in year.items()}

    # Obtenemos los "top_n" dias con mayor cantidad de mensajes
    top = chat_df['Timestampt'].dt.date.value_counts().nlargest(top_n)
    top_messages_per_day = {date.strftime("%d/%m/%Y"): count for date, count in top.items()}

    return {
        "messages_per_day": messages_per_day,
        "messages_per_month": messages_per_month,
        "messages_per_year": messages_per_year,
        "top_messages_per_day": top_messages_per_day
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

    # 2. Estadisticas
    total_messages, participants, total_users = _get_basic_stats(chat_df)

    n_messages_per_user = _get_messages_per_user(chat_df)

    hot_hours = _get_hot_hours(chat_df)

    messages_per_day, messages_per_month, messages_per_year, top_messages_per_day = _get_calendar_stats(chat_df)


    # 4. TODO: Construimos y devolvemos el diccionario de resultados (RF-05)
    return {
        "total_messages": total_messages,
        "total_users": total_users,
        "participants": participants,
        "status": "success"
    }