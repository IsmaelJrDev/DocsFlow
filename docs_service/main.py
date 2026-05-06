from fastapi import FastAPI, UploadFile, File, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse, Response
import logging

from auth import verify_jwt, get_user_role
from extractor import extraer_texto
from pipeline.paso1_analisis import analizar_texto
from pipeline.paso2_resumen import generar_resumen
from pipeline.paso3_clasificacion import clasificar_documento

app = FastAPI()

async def get_token_from_header(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado o inválido")
    return authorization.split(" ")[1]

# --- Mapeo de la respuesta de Ollama a los valores que espera el frontend ---
CLASSIFICATION_MAP = {
    "rojo": "red",
    "ámbar": "amber",
    "ambar": "amber",
    "verde": "green",
    # Por si Ollama responde en inglés
    "red": "red",
    "amber": "amber",
    "green": "green",
}

def normalize_classification(raw: str) -> str:
    """Convierte la clasificación de Ollama (Rojo/Ámbar/Verde) al formato del frontend (red/amber/green)."""
    cleaned = raw.strip().lower().rstrip(".,;:!\"'")
    return CLASSIFICATION_MAP.get(cleaned, "amber")  # Default: amber si no se reconoce

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(get_token_from_header)
):
    # 1. Recibir petición
    content = await file.read()
    size = len(content)
    print(f"[DOC_SERVICE] Petición recibida: archivo={file.filename}, size={size} bytes")

    # 2. Verificar JWT
    print("[DOC_SERVICE] Verificando token JWT...")
    payload = await verify_jwt(token)
    user_id = payload.get("id")
    email = payload.get("email")
    print(f"[DOC_SERVICE] Token válido. Usuario ID: {user_id}  Email: {email}")

    # 3 & 4 & 5. Consultar rol
    role = await get_user_role(user_id, token)
    if role == "admin":
        print("[DOC_SERVICE] Acceso denegado. Rol \"admin\" no puede subir documentos")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: el rol 'admin' no tiene permiso para subir documentos"
        )
    elif role == "secretariat":
        print("[DOC_SERVICE] Rol obtenido: secretariat — Acceso permitido")
    else:
        print(f"[DOC_SERVICE] Acceso denegado. Rol desconocido: {role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acceso denegado: rol '{role}' no válido"
        )

    # 6. Extraer texto
    texto = extraer_texto(content, file.content_type)
    print(f"[DOC_SERVICE] Texto extraído: {len(texto)} caracteres")

    # 7. Mandar a Máquina 1
    try:
        analisis = analizar_texto(texto)
        print(f"[DOC_SERVICE] Análisis recibido de Máquina 1. Longitud: {len(analisis)} caracteres")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error comunicándose con el motor de análisis"
        )

    print("[DOC_SERVICE] 🏁 Pipeline Paso 1 completado exitosamente")

    # 8. Mandar a Máquina 2 (Generar Resumen)
    try:
        resumen = generar_resumen(analisis)
        print(f"[DOC_SERVICE] Resumen recibido de Máquina 2. Longitud: {len(resumen)} caracteres")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error comunicándose con el motor de resumen"
        )
        
    print("[DOC_SERVICE] 🏁 Pipeline Paso 2 completado exitosamente")

    # Paso 3: Mandar a Máquina 3 (Clasificación)
    try:
        clasificacion_raw = clasificar_documento(resumen)
        clasificacion = normalize_classification(clasificacion_raw)
        print(f"[DOC_SERVICE] Clasificación recibida de Máquina 3: {clasificacion_raw} → {clasificacion}")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error comunicándose con el motor de clasificación"
        )
        
    print("[DOC_SERVICE] 🏁 Pipeline Paso 3 completado exitosamente")

    # Guardar en base de datos
    from database import save_document_analysis
    try:
        print("[DOC_SERVICE] Guardando documento en la base de datos...")
        saved_doc = await save_document_analysis(
            filename=file.filename,
            content_type=file.content_type,
            file_data=content,
            uploader_id=user_id,
            uploader_email=email,
            uploader_role=role,
            text=texto,
            analysis=analisis,
            summary=resumen,
            classification=clasificacion
        )
        print(f"[DOC_SERVICE] Documento guardado exitosamente con ID: {saved_doc['document_id']}")
    except Exception as e:
        print(f"[DOC_SERVICE] Error guardando en base de datos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error guardando el análisis en la base de datos"
        )

    # 9. Retornar análisis y resumen
    return JSONResponse(content={
        "status": "paso_3_completado",
        "archivo": file.filename,
        "uploaded_by": user_id,
        "rol": role,
        "document_id": saved_doc["document_id"],
        "analisis": analisis,
        "resumen": resumen,
        "clasificacion": clasificacion
    })


# ==========================================
# ENDPOINTS DE CONSULTA (para el frontend)
# ==========================================

@app.get("/list")
async def list_documents(token: str = Depends(get_token_from_header)):
    """Retorna todos los documentos procesados (sin el binario del archivo para eficiencia)."""
    from database import get_all_documents
    try:
        documents = await get_all_documents()
        return JSONResponse(content=documents)
    except Exception as e:
        print(f"[DOC_SERVICE] Error al listar documentos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los documentos"
        )


@app.get("/download/{document_id}")
async def download_document(document_id: str, token: str = Depends(get_token_from_header)):
    """Descarga el archivo original de un documento procesado."""
    from database import get_document_file
    try:
        doc = await get_document_file(document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        return Response(
            content=doc["file_data"],
            media_type=doc.get("content_type", "application/octet-stream"),
            headers={
                "Content-Disposition": f'attachment; filename="{doc["filename"]}"'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[DOC_SERVICE] Error al descargar documento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al descargar el documento"
        )
