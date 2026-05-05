import pdfplumber
import io

def extraer_texto(contenido: bytes, mimetype: str) -> str:
    print("[DOC_SERVICE] Extrayendo texto del archivo...")
    if "pdf" in mimetype:
        with pdfplumber.open(io.BytesIO(contenido)) as pdf:
            texto = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return texto
    return contenido.decode("utf-8", errors="ignore")
