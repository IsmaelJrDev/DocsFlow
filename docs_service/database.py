from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import uuid
import base64
from config import MONGO_URI

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
# Use a specific database, let's call it 'docsflow'
db = client.docsflow

async def save_document_analysis(
    filename: str,
    content_type: str,
    file_data: bytes,
    uploader_id: str,
    uploader_email: str,
    uploader_role: str,
    text: str,
    analysis: str,
    summary: str,
    classification: str
):
    documents_collection = db.documents
    
    doc = {
        "document_id": str(uuid.uuid4()),
        "filename": filename,
        "content_type": content_type,
        "file_data": base64.b64encode(file_data).decode("utf-8"),  # Store as base64 string
        "uploaded_by": uploader_id,
        "uploader_email": uploader_email,
        "uploader_role": uploader_role,
        "text_extracted": text,
        "analysis": analysis,
        "summary": summary,
        "classification": classification,
        "created_at": datetime.datetime.utcnow()
    }
    
    result = await documents_collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


async def get_all_documents():
    """Retorna todos los documentos SIN el binario del archivo (para listado eficiente)."""
    documents_collection = db.documents
    cursor = documents_collection.find(
        {},
        {
            "file_data": 0,        # Excluir el archivo binario
            "text_extracted": 0,    # Excluir texto completo
            "analysis": 0,          # Excluir análisis completo (pesado)
        }
    ).sort("created_at", -1)  # Más recientes primero
    
    docs = []
    async for doc in cursor:
        docs.append({
            "_id": str(doc["_id"]),
            "document_id": doc.get("document_id", ""),
            "title": doc.get("filename", "Sin título"),
            "type": _get_file_type(doc.get("filename", "")),
            "status": doc.get("classification", "amber"),
            "date": doc.get("created_at", datetime.datetime.utcnow()).strftime("%d/%m/%Y"),
            "summary": doc.get("summary", ""),
            "author": doc.get("uploader_email", "Desconocido"),
        })
    return docs


async def get_document_file(document_id: str):
    """Retorna el archivo original de un documento."""
    documents_collection = db.documents
    doc = await documents_collection.find_one(
        {"document_id": document_id},
        {"file_data": 1, "filename": 1, "content_type": 1}
    )
    if not doc:
        return None
    
    return {
        "file_data": base64.b64decode(doc["file_data"]),
        "filename": doc.get("filename", "archivo"),
        "content_type": doc.get("content_type", "application/octet-stream"),
    }


def _get_file_type(filename: str) -> str:
    """Extrae la extensión del archivo para mostrar en el frontend."""
    if "." in filename:
        ext = filename.rsplit(".", 1)[1].upper()
        return ext
    return "ARCHIVO"
