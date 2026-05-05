from fastapi import FastAPI, UploadFile, File, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from auth import verify_jwt, get_user_role
from extractor import extraer_texto
from pipeline.paso1_analisis import analizar_texto
from pipeline.paso2_resumen import generar_resumen

app = FastAPI()

async def get_token_from_header(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado o inválido")
    return authorization.split(" ")[1]

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

    # 9. Retornar análisis y resumen
    return JSONResponse(content={
        "status": "paso_2_completado",
        "archivo": file.filename,
        "uploaded_by": user_id,
        "rol": role,
        "analisis": analisis,
        "resumen": resumen
    })
