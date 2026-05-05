from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import uuid
from config import MONGO_URI

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
# Use a specific database, let's call it 'docsflow'
db = client.docsflow

async def save_document_analysis(filename: str, uploader_id: str, uploader_role: str, text: str, analysis: str, summary: str, classification: str):
    documents_collection = db.documents
    
    doc = {
        "document_id": str(uuid.uuid4()),
        "filename": filename,
        "uploaded_by": uploader_id,
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
