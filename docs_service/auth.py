import jwt
import httpx
from fastapi import HTTPException, status
from config import JWT_SECRET, USER_SERVICE_URL

async def verify_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("[DOC_SERVICE] Error en verificación de token: Token expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except jwt.InvalidTokenError:
        print("[DOC_SERVICE] Error en verificación de token: Token inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

async def get_user_role(user_id: str, token: str) -> str:
    print("[DOC_SERVICE] Consultando rol en User Service...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}/perfiles/{user_id}", headers=headers, timeout=10.0)
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
                
            response.raise_for_status()
            data = response.json()
            return data.get("role", "")
    except httpx.RequestError as e:
        print(f"[DOC_SERVICE] Error consultando User Service: {e}")
        raise HTTPException(status_code=500, detail="Error de comunicación con User Service")
