import pandas as pd
import re
from collections import Counter
import emoji
from datetime import timedelta, date
from typing import Dict, List, Any
from app.utils.constants import CHAT_STOPWORDS
from nltk.corpus import stopwords

#Dividimos los calculos de las diferentes estadisticas en diferentes funciones para un codigo mas limpo

def _get_filtered_df_by_user(chat_df: pd.DataFrame, user: str) -> pd.DataFrame:
    """Devuelve un sub-dataframe tomando solo los registros de un usuario en concreto"""
    return chat_df[chat_df['Author'] == user]

def _record_new_streak(finish_date: date, day_lenght: int) -> Dict[str, Any]:
    """Devuelve un diccionario con inicio, fin, y duracion de una racha para la funcion de rachas"""

    init_date = finish_date - timedelta(days=day_lenght - 1)

    return {
        'start': init_date,
        'end': finish_date,
        'duration': day_lenght
    }


def _get_all_chat_users(chat_df: pd.DataFrame) -> List[str]:
    """
    Devuelve una lista con todos lo usuarios del chat 
    OJO: devuelve el telefono si cliente no tiene guardado al usuario en la agenda

    chat_df['Author'].unique() extrae los nombres únicos de la columna 'Author'
    .dropna() elimina los valores nulos (por ejemplo, mensajes del sistema de WhatsApp)
    .tolist() lo convierte a una lista normal de Python para que FastAPI pueda serializarlo a JSON
    """

    return chat_df['Author'].dropna().unique().tolist()


def get_basic_stats(chat_df: pd.DataFrame) -> Dict[str, Any]:
    """Calcula mensajes totales y participantes."""
    return {
        "total_messages": len(chat_df),
        "participants": _get_all_chat_users(chat_df),
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

# Se puede obtener estadisticas de un solo usuario pasandole este como parametro, si esta vacio se usaran todos los usuarios del chat
def get_length_stats(chat_df: pd.DataFrame, user: str | None = None, top_n: int = 10) -> List[Dict[str, Any]]:
    """Obtener un top n de los mensajes mas largos, devolviendo el mensaje, la longitud y el autor"""

    if user:
        chat_df = _get_filtered_df_by_user(chat_df, user)
    
    # Creamos una serie con la longitud de cada mensaje
    lengths = chat_df["Message"].fillna("").str.len()

    # Agregamos la columna, ordenamos el DataFrame completo y extraemos el top seleccionado
    chat_df_with_len = chat_df.assign(Length=lengths)
    chat_df_sorted = chat_df_with_len.sort_values("Length", ascending=False)
    chat_df_cropped = chat_df_sorted.head(top_n)

    # Seleccionamos solo las columnas necesarias
    result = chat_df_cropped[["Author", "Message", "Length"]]
    return result.to_dict(orient="records")

#
def get_streak_stats(chat_df: pd.DataFrame, top_n: int = 3) -> List[Dict[str, Any]]:
    """
    Obtener las rachas de dias seguidos con mensajes mas largas del chat.

    Se puede seleccionar un top N o, por defecto, seran las 3 mas altas.

    Se tomaran como rachas si se cumplen las siguientes caracteristicas:
        - Mas de 1 usuario escribe en el chat cada dia.
        - No hay un dia sin mensajes en medio.
        - Como caso limite, se permite un dia de gracia si al menos un usuario ha escrito y, el dia anterior
          y el siguiente, alguien mas, aparte de ese usuario, ha participado en el chat. (Pueden haber varios dias
          de gracia dentro de la misma racha pero no seguidos)
        - Las rachas seran de 3 dias como minimo

    """
    chat_df_with_date = chat_df.assign(Date=chat_df['Timestamp'].dt.date)

    # Dejamos solo un registro por cada autor/fecha, recortamos el DF para quedarnos solo con esas columnas y lo ordenamos por fechas
    chat_df_cropped = chat_df_with_date.drop_duplicates(subset=['Author', 'Date'], keep='first')
    chat_df_sorted = chat_df_cropped[['Author', 'Date']].sort_values(by='Date')
    chat_df_sorted = chat_df_sorted.reset_index(drop=True)

    streaks = []
    ant_date = None
    daily_user_count = 0
    day_count = 0
    grace_period = False
    last_confirmed_date = None

    for index, row in chat_df_sorted.iterrows():
        act_date = row['Date']
        if index == 0:
            ant_date = act_date
            day_count = 0
            daily_user_count = 1
            continue

        if act_date != ant_date:
            if act_date == ant_date + timedelta(days=1):
                if daily_user_count == 1: #Si el dia anterior solo ha hablado una persona
                    if grace_period:
                        if day_count >= 3 and last_confirmed_date is not None:
                            streaks.append(_record_new_streak(last_confirmed_date, day_count))
                        day_count = 0
                        last_confirmed_date = None
                        grace_period = False #Se pone false porq ue quiere decir qe ha habido dos dias seguidos con 1 solo usuario
                    else:
                        if day_count > 0:
                            grace_period = True # La unica forma de que grace_period se ponga a True es que el dia anterior haya sido un dia de racha valido (>2 usuarios)
                        else:
                            grace_period = False
                else: 
                    grace_period = False
            else: # Se rompe la racha por salto de fechas
                if day_count >= 3 and last_confirmed_date is not None:
                    streaks.append(_record_new_streak(last_confirmed_date, day_count))
                day_count = 0
                last_confirmed_date = None
                grace_period = False

            daily_user_count = 0


        if act_date == ant_date: #Cada vez que entra aqui es un usuario mas que habla
            daily_user_count += 1
            if daily_user_count == 2: # Solo entra cuando se llega a 2 usuarios en un dia, no puede entrar mas de 1 vez por dia
                day_count += 1
                if grace_period:
                    day_count += 1
                last_confirmed_date = act_date
                grace_period = False
        elif act_date == ant_date + timedelta(days=1): #Cada vez que entra aqui es que es el primero en hablar despues de un dia donde ya se ha hablado
            daily_user_count = 1
        else: #Si entra aqui quiere decir que nadie ha hablado en el dia anterior y este es el primer usuario
            daily_user_count = 1

        ant_date = act_date

    if day_count >= 3 and last_confirmed_date is not None:
        streaks.append(_record_new_streak(last_confirmed_date, day_count))

    streaks.sort(key=lambda x: x['duration'], reverse=True)

    return streaks[:top_n]





    

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
            "status": "failed",
            "message": "El chat analizado no contiene mensajes válidos.",
            "total_messages": 0,
            "participants": [],
            "total_users": 0,
            "n_messages_per_user": {},
            "hot_hours": {},
            "messages_per_day": {},
            "messages_per_month": {},
            "messages_per_year": {},
            "top_messages_per_day": {},
            "top_words": {},
            "top_emojis": {},
            "longest_messages": [],
            "top_streaks": []
        }

    # 2. Estadisticas
    basic_stats = get_basic_stats(chat_df)
    n_messages_per_user = get_messages_per_user(chat_df)
    hot_hours = get_hot_hours(chat_df)
    calendar_stats = get_calendar_stats(chat_df)

    top_words = get_word_stats(chat_df)

    top_emojis = get_emoji_stats(chat_df)

    longest_messages = get_length_stats(chat_df)

    top_streaks = get_streak_stats(chat_df)


    # 4. Construimos y devolvemos el diccionario de resultados (RF-05)
    return {
        "status": "success",
        "message": "El chat se ha analizado correctamente.",
        "total_messages": basic_stats["total_messages"],
        "participants": basic_stats["participants"],
        "total_users": basic_stats["n_participants"],
        "n_messages_per_user": n_messages_per_user["n_messages_per_user"],
        "hot_hours": hot_hours["hot_hours"],
        "messages_per_day": calendar_stats["messages_per_day"],
        "messages_per_month": calendar_stats["messages_per_month"],
        "messages_per_year": calendar_stats["messages_per_year"],
        "top_messages_per_day": calendar_stats["top_messages_per_day"],
        "top_words": top_words,
        "top_emojis": top_emojis,
        "longest_messages": longest_messages,
        "top_streaks": top_streaks
    }
