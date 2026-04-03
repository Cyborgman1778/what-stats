import pandas as pd
import re
from collections import Counter
import emoji
from typing import Dict, List, Any
from app.utils.constants import CHAT_STOPWORDS
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")

#Dividimos los calculos de las diferentes estadisticas en diferentes funciones para un codigo mas limpo

def _get_filtered_df_by_user(chat_df: pd.DataFrame, user: str) -> pd.DataFrame:
    """Devuelve un sub-dataframe tomando solo los registros de un usuario en concreto"""
    return chat_df[chat_df['Author'] == user]


def get_basic_stats(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula mensajes totales y participantes."""
    return {
        "total_messages": len(chat_df),

        # chat_df['Author'].unique() extrae los nombres únicos de la columna 'Author'
        # .dropna() elimina los valores nulos (por ejemplo, mensajes del sistema de WhatsApp)
        # .tolist() lo convierte a una lista normal de Python para que FastAPI pueda serializarlo a JSON
        "participants": chat_df['Author'].dropna().unique().tolist(),
        "n_participants": chat_df['Author'].nunique()
    }

def get_messages_per_user(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula cuantos mensajes envia cada usuario"""
    return {
        "n_messages_per_user": chat_df['Author'].value_counts().to_dict()
    }

# Se puede obtener estadisticas de un solo usuario pasandole este como parametro, si esta vacio se usaran todos los usuarios del chat
def get_hot_hours(chat_df: pd.DataFrame, user: str | None = None) -> Dict[str, Any]:
    """Cuenta los mensajes que hay en cada hora del dia"""

    if user:
        chat_df = _get_filtered_df_by_user(chat_df, user)

    # 1. chat_df['Timestamp'].dt.hour extrae solo la hora (0 a 23) de cada mensaje.
    # 2. value_counts() cuenta cuántos mensajes hay en cada hora.
    # 3. sort_index() ordena el resultado de 0 a 23 (vital para que el gráfico salga ordenado).
    # 4. to_dict() lo convierte al formato JSON.
    messages_per_hour = chat_df['Timestamp'].dt.hour.value_counts().sort_index().to_dict()

    #ponemos la fecha en formato legible
    hot_hours = {
        f"{hour:02d}:00": count for hour, count in messages_per_hour.items()
    }

    return {
        "hot_hours": hot_hours
    }

# Se puede obtener estadisticas de un solo usuario pasandole este como parametro, si esta vacio se usaran todos los usuarios del chat
def get_calendar_stats(chat_df: pd.DataFrame, user: str | None = None, top_n: int = 10) -> Dict[str, Any]:
    """Obtener numero de mensajes por fechas (dia/mes/año, mes/año, año)"""

    if user:
        chat_df = _get_filtered_df_by_user(chat_df, user)
    

    # Obtenemos los mensajes por fechas (dia/mes/año), lo ordenamos y hacemos la fecha legible
    day = chat_df['Timestamp'].dt.date.value_counts().sort_index()
    messages_per_day = {date.strftime("%d/%m/%Y"): count for date, count in day.items()}

    # Obtenemos los mensajes por meses (mes/año), lo ordenamos y hacemos la fecha legible
    month = chat_df['Timestamp'].dt.to_period('M').value_counts().sort_index()
    messages_per_month = {period.strftime('%m/%Y'): count for period, count in month.items()}

    # Obtenemos los mensajes por años, lo ordenamos y hacemos la fecha legible
    year = chat_df['Timestamp'].dt.year.value_counts().sort_index()
    messages_per_year = {str(period): count for period, count in year.items()}

    # Obtenemos los "top_n" dias con mayor cantidad de mensajes
    top = chat_df['Timestamp'].dt.date.value_counts().nlargest(top_n)
    top_messages_per_day = {date.strftime("%d/%m/%Y"): count for date, count in top.items()}

    return {
        "messages_per_day": messages_per_day,
        "messages_per_month": messages_per_month,
        "messages_per_year": messages_per_year,
        "top_messages_per_day": top_messages_per_day
    }

# Se puede obtener estadisticas de un solo usuario pasandole este como parametro, si esta vacio se usaran todos los usuarios del chat
def get_word_stats(chat_df: pd.DataFrame, user: str | None = None, top_n: int = 10) -> Dict[str, Any]:
    """Obtener un top n de las palabras mas usadas en el chat, excluyendo monosilabos y conjunciones"""

    if user:
        chat_df = _get_filtered_df_by_user(chat_df, user)

    STOPWORDS_ES = set(stopwords.words("spanish"))
    ALL_STOPWORDS = STOPWORDS_ES.union(CHAT_STOPWORDS)

    # Unimos todos los mensajes en un solo texto (OJO: esto casi duplica el espacio en memoria)
    text = " ".join(chat_df["Message"].dropna().astype(str))

    # Extraemos palabras en minúsculas, incluyendo acentos y ñ
    words = re.findall(r"\b[a-záéíóúüàèìòùñ]+\b", text.lower())

    filtered_words = [
        w for w in words
        if w not in ALL_STOPWORDS               # Eliminamos las palabras sin sentido
        and len(w) > 2                          # Eliminamos todas las palabras de 2 letras o menos
        and not w.isdigit()                     # Eliminamos los numeros
        and not w.startswith("http")            # Eliminamos links
    ]

    word_counter = Counter(filtered_words)
    return dict(word_counter.most_common(top_n))

# Se puede obtener estadisticas de un solo usuario pasandole este como parametro, si esta vacio se usaran todos los usuarios del chat
def get_emoji_stats(chat_df: pd.DataFrame, user: str | None = None, top_n: int = 10) -> Dict[str, Any]:
    """Obtener un top n de los emojis mas usadas en el chat"""

    if user:
        chat_df = _get_filtered_df_by_user(chat_df, user)

    text = " ".join(chat_df["Message"].dropna().astype(str))
    emoji_list = [item["emoji"] for item in emoji.emoji_list(text)]
    emoji_counter = Counter(emoji_list)
    return dict(emoji_counter.most_common(top_n))

#
def get_length_stats(chat_df: pd.DataFrame, top_n: int = 10) -> List[Dict[str, Any]]:
    """Obtener un top n de los mensajes mas largos, devolviendo el mensaje, la longitud y el autor"""
    
    # Creamos una serie con la longitud de cada mensaje
    lengths = chat_df["Message"].fillna("").str.len()

    # Agregamos la columna, ordenamos el DataFrame completo y extraemos el top seleccionado
    chat_df_with_len = chat_df.assign(Length=lengths)
    chat_df_sorted = chat_df_with_len.sort_values("Length", ascending=False)
    chat_df_cropped = chat_df_sorted.head(top_n)

    # Seleccionamos solo las columnas necesarias
    result = chat_df_cropped[["Author", "Message", "Length"]]
    return result.to_dict(orient="records")
    

def analyze_chat_data(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Recibe un DataFrame de Pandas generado a partir de un chat de WhatsApp
    y calcula estadísticas (RF-04).
    
    Args:
        chat_df (pd.DataFrame): El DataFrame con las columnas Date, Time, Author, Message, Timestamp.
        
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
    total_messages, participants, total_users = get_basic_stats(chat_df)

    n_messages_per_user = get_messages_per_user(chat_df)

    hot_hours = get_hot_hours(chat_df)

    messages_per_day, messages_per_month, messages_per_year, top_messages_per_day = get_calendar_stats(chat_df)


    # 4. TODO: Construimos y devolvemos el diccionario de resultados (RF-05)
    return {
        "total_messages": total_messages,
        "total_users": total_users,
        "participants": participants,
        "status": "success"
    }