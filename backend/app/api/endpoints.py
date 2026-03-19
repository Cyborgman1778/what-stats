from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.whatsapp_chat_parser import parse_chat_to_dataframe
# Importaremos el analizador en el siguiente paso
# from app.services.data_analyzer import analyze_chat_data 

# Creamos el router (un mini-FastAPI para organizar las rutas)
router = APIRouter()

@router.post("/upload-chat")
async def upload_and_analyze_chat(file: UploadFile = File(...)):
    """
    Recibe un archivo exportado de WhatsApp (.txt o .zip), 
    lo procesa en memoria y devuelve estadísticas básicas.
    """
    
    # 1. Validación de entrada (RF-02): Comprobamos la extensión
    if not file.filename.endswith(('.txt', '.zip')):
        raise HTTPException(
            status_code=400, 
            detail="Formato no válido. Por favor, sube un archivo .txt o .zip exportado de WhatsApp."
        )
    
    try:
        # 2. Privacidad por diseño (RNF-01): Leemos el archivo directamente a la memoria RAM
        # El método await file.read() obtiene los bytes sin crear un archivo físico
        file_bytes = await file.read()
        
        # 3. Parseo y normalización (RF-03): Convertimos los bytes en un DataFrame de Pandas
        df = parse_chat_to_dataframe(file_bytes, file.filename)
        
        # 4. Cálculos (RF-04): Aquí llamaremos a tu módulo data_analyzer.py
        # stats = analyze_chat_data(df)
        
        # Por ahora, devolvemos un JSON básico (RF-05) para verificar que el DataFrame se ha creado bien
        return {
            "status": "success",
            "filename": file.filename,
            "total_messages_parsed": len(df),
            "message": "Archivo procesado y destruido de la memoria correctamente."
        }
        
    except ValueError as e:
        # Gestión de errores conocidos (RF-07): Por ejemplo, si suben un ZIP vacío
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # Gestión de errores inesperados (RF-07)
        print(f"Error procesando archivo: {e}") # En producción se usaría un logger seguro
        raise HTTPException(
            status_code=500, 
            detail="Error interno del servidor al procesar el archivo."
        )
        
    finally:
        # Buenas prácticas: liberamos el recurso de FastAPI asociado a la subida
        await file.close()