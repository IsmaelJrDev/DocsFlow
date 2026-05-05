from ollama import Client
from config import OLLAMA_SUMMARIZER_HOST

def generar_resumen(analisis_previo: str) -> str:
    print(f"[DOC_SERVICE] Generando resumen en Máquina 2 (mistral @ {OLLAMA_SUMMARIZER_HOST})...")
    try:
        cliente = Client(host=OLLAMA_SUMMARIZER_HOST)
        respuesta = cliente.chat(
            model='mistral',
            messages=[{
                'role': 'user',
                'content': f'Genera un resumen ejecutivo y conciso basado en el siguiente análisis del documento:\n\n{analisis_previo}'
            }]
        )
        resumen = respuesta.message.content
        return resumen
    except Exception as e:
        print(f"[DOC_SERVICE] Error conectando a Máquina 2 ({OLLAMA_SUMMARIZER_HOST}): {e}")
        raise e
