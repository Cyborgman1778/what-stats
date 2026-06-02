# WhatStats Backend

Backend de WhatStats para analizar chats exportados de WhatsApp sin almacenar archivos ni persistir mensajes. La API recibe un `.txt` o `.zip`, procesa el contenido en memoria y devuelve estadisticas listas para consumir desde una web, una app movil o cualquier cliente HTTP.

Este README documenta solo el backend.

## Que hace

- Expone una API HTTP con FastAPI.
- Acepta exports de WhatsApp en formato `.txt` o `.zip`.
- Procesa el chat en memoria.
- Calcula estadisticas de mensajes, participantes, horas activas, calendario, palabras, emojis, mensajes largos y rachas.
- Incluye rate limiting basico por IP.
- Incluye CORS configurable por entorno.
- Incluye healthcheck para despliegues con Docker.

## Stack

| Area | Tecnologia |
| --- | --- |
| API | FastAPI |
| Servidor ASGI | Uvicorn |
| Analisis de datos | Pandas |
| NLP basico | NLTK stopwords |
| Emojis | emoji |
| Configuracion | pydantic-settings + `.env` |
| Rate limit | slowapi |
| Tests | pytest |
| Contenedor | Docker |

## Endpoints

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/` | Mensaje basico de estado de la API. |
| `GET` | `/healthz` | Healthcheck para Docker, Cloudflare Tunnel o monitorizacion. |
| `POST` | `/upload-chat` | Recibe un archivo `.txt` o `.zip` en multipart y devuelve estadisticas. |

El endpoint principal espera un `multipart/form-data` con el campo exacto `file`.

Ejemplo de respuesta exitosa simplificada:

```json
{
  "status": "success",
  "stats": {
    "status": "success",
    "message": "El chat se ha analizado correctamente.",
    "total_messages": 1200,
    "participants": ["Ana", "Luis"],
    "total_users": 2
  }
}
```

## Requisitos

- Git.
- Python 3.11 o superior si lo ejecutas sin Docker.
- Docker si prefieres ejecutarlo en contenedor.

Versiones usadas actualmente:

- Python `3.11` en Docker.
- Dependencias fijadas en `backend/requirements.txt`.
- Dependencias de desarrollo en `backend/requirements-dev.txt`.

## Clonar la rama de produccion backend

Sustituye `<URL_DEL_REPOSITORIO>` por la URL real del repositorio.

```bash
git clone -b prod-backend <URL_DEL_REPOSITORIO>
cd what-stats/backend
```

Si ya tienes el repositorio clonado:

```bash
git fetch origin
git checkout prod-backend
cd backend
```

## Configuracion local

Copia el ejemplo de variables de entorno:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Para desarrollo local puedes usar algo parecido a esto:

```env
ENVIRONMENT=development
DEBUG=true
ENABLE_DOCS=true

HOST=127.0.0.1
PORT=8000

ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://localhost,capacitor://localhost,http://localhost
CORS_ALLOW_CREDENTIALS=false

TRUSTED_HOSTS=localhost,127.0.0.1

MAX_UPLOAD_SIZE=52428800
MAX_DECOMPRESSED_SIZE=52428800
MAX_ZIP_COMPRESSION_RATIO=100

RATE_LIMIT_PER_MINUTE=3
```

Notas importantes:

- `.env` no debe subirse a GitHub.
- `.env.example` si debe subirse a GitHub.
- `ALLOWED_ORIGINS` controla que origins de navegador/WebView pueden llamar a la API.
- CORS no es autenticacion. Clientes como `curl`, Postman o scripts pueden llamar igualmente a una API publica.
- `TRUSTED_HOSTS` valida el header `Host`, por ejemplo `localhost` o `api.whatstats.net`.

## Opcion A: ejecutar con Docker

Esta es la forma recomendada para evitar diferencias entre maquinas.

Construye la imagen desde `backend/`:

```bash
docker build -t whatstats-api:local .
```

Ejecuta el contenedor:

```bash
docker run --rm \
  --name whatstats-api \
  --env-file .env \
  -p 8000:8000 \
  whatstats-api:local
```

En Windows PowerShell:

```powershell
docker run --rm `
  --name whatstats-api `
  --env-file .env `
  -p 8000:8000 `
  whatstats-api:local
```

Comprueba que funciona:

```bash
curl http://127.0.0.1:8000/healthz
```

Respuesta esperada:

```json
{"status":"ok"}
```

Si `ENABLE_DOCS=true`, abre:

```text
http://127.0.0.1:8000/docs
```

## Opcion B: ejecutar con Python local

Crea un entorno virtual desde `backend/`.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m nltk.downloader stopwords
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m nltk.downloader stopwords
```

Arranca la API:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Comprueba que responde:

```bash
curl http://127.0.0.1:8000/healthz
```

## Probar subida de un chat

Con `curl`:

```bash
curl -X POST http://127.0.0.1:8000/upload-chat \
  -F "file=@/ruta/a/tu/chat.txt"
```

Con JavaScript en un cliente web:

```js
const formData = new FormData()
formData.append("file", file)

const response = await fetch("http://127.0.0.1:8000/upload-chat", {
  method: "POST",
  body: formData,
})

const data = await response.json()
```

No establezcas manualmente el header `Content-Type` cuando uses `FormData`; el navegador debe generarlo con su boundary.

## Ejecutar tests

Instala dependencias de desarrollo:

```bash
python -m pip install -r requirements-dev.txt
```

Ejecuta la suite:

```bash
pytest -q
```

Si `TRUSTED_HOSTS` bloquea tests locales, puedes permitir hosts solo durante la ejecucion de tests.

Linux/macOS:

```bash
TRUSTED_HOSTS='*' pytest -q
```

Windows PowerShell:

```powershell
$env:TRUSTED_HOSTS='*'; pytest -q
```

Audita dependencias runtime:

```bash
pip-audit -r requirements.txt
```

Comprueba conflictos instalados:

```bash
python -m pip check
```

## Variables de entorno

| Variable | Descripcion |
| --- | --- |
| `ENVIRONMENT` | Nombre del entorno: `development`, `production`, etc. |
| `DEBUG` | Activa debug de FastAPI. Debe ser `false` en produccion. |
| `ENABLE_DOCS` | Activa `/docs`, `/redoc` y `/openapi.json`. Debe ser `false` en produccion publica. |
| `HOST` | Host informativo para ejecucion local. |
| `PORT` | Puerto informativo para ejecucion local. |
| `ALLOWED_ORIGINS` | Origins permitidos por CORS separados por coma. |
| `CORS_ALLOW_CREDENTIALS` | Permite cookies/credenciales CORS. Por defecto `false`. |
| `TRUSTED_HOSTS` | Hosts validos para el header `Host`, separados por coma. |
| `MAX_UPLOAD_SIZE` | Tamano maximo del archivo subido, en bytes. |
| `MAX_DECOMPRESSED_SIZE` | Tamano maximo permitido tras descomprimir ZIP, en bytes. |
| `MAX_ZIP_COMPRESSION_RATIO` | Ratio maximo permitido para archivos ZIP. |
| `RATE_LIMIT_PER_MINUTE` | Peticiones permitidas por minuto por IP. |

## Codigos de respuesta importantes

| Codigo | Significado |
| --- | --- |
| `200` | Peticion procesada. Revisa tambien `stats.status`. |
| `400` | Archivo invalido o chat no procesable. |
| `413` | Payload demasiado grande. |
| `429` | Rate limit excedido. |
| `500` | Error interno inesperado. |

## Privacidad y seguridad

- El backend no guarda archivos de chat en disco.
- El archivo se procesa en memoria.
- No hay base de datos en este backend.
- No loguees contenido de chats ni datos personales.
- Para produccion publica, usa tambien protecciones externas como Cloudflare WAF, rate limiting y, si aplica, Turnstile.

## Estructura principal

```text
backend/
  app/
    api/
      endpoints.py
    core/
      config.py
      rate_limiter.py
    schemas/
      response_models.py
    services/
      data_analyzer.py
      whatsapp_chat_parser.py
    utils/
      constants.py
      regex_patterns.py
    main.py
  tests/
  Dockerfile
  requirements.txt
  requirements-dev.txt
  .env.example
```

## Despliegue

El backend esta preparado para ejecutarse en Docker. En produccion se recomienda:

- Ejecutar el contenedor detras de un reverse proxy o Cloudflare Tunnel.
- Publicar solo HTTPS.
- Mantener `DEBUG=false`.
- Mantener `ENABLE_DOCS=false`.
- Definir `ALLOWED_ORIGINS` con dominios reales.
- Definir `TRUSTED_HOSTS` con el host publico real de la API.
- No abrir el puerto del backend directamente a internet si no es necesario.

Ejemplo de ejecucion en servidor:

```bash
docker run -d \
  --name whatstats-api \
  --restart unless-stopped \
  --env-file /opt/whatstats/backend/.env \
  -p 127.0.0.1:8000:8000 \
  whatstats-api:latest
```

## Licencia

Este backend se publica bajo licencia MIT. Consulta el archivo `LICENSE` para mas detalles.
