from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# APIRouter para poder gestionar los endpoits de endpoints.py
from app.api.endpoints import router
from app.core.config import settings
from app.core.rate_limiter import limiter


# 1. Inicializar el Rate Limiter (usa la IP del cliente como identificador)

app = FastAPI(
    title="WhatStats API",
    description="API para el análisis de chats de WhatsApp orientada a la privacidad",
    debug=settings.DEBUG,
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
)

# Registrar el manejador de errores cuando alguien se pasa del límite
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)

if settings.trusted_hosts:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.trusted_hosts,
        www_redirect=False,
    )

# 2. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Accept", "Content-Type", "Origin"],
)

# 3. Middleware para limitar el tamaño del archivo (Body Size Limit)
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.MAX_UPLOAD_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": "Payload Too Large: El archivo supera el límite de tamaño permitido."}
            )
    response = await call_next(request)
    return response


@app.get("/healthz", include_in_schema=False)
async def healthz():
    return {"status": "ok"}

# Endpoint de prueba protegido por Rate Limit
@app.get("/")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def root(request: Request):
    return {"message": "WhatStats API funcionando. Privacidad por diseño activa."}
