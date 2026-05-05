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
                'content': f"""Eres un asistente de resumen ejecutivo en un entorno de oficina corporativa.

                Genera un resumen conciso del siguiente análisis con este formato:

                - **Tema principal:** De qué trata el documento en una línea.
                - **Puntos clave:** 2 a 4 puntos relevantes del contenido.
                - **Acción requerida:** Si el documento exige alguna acción, indícala. Si no, escribe "Ninguna".
                - **Urgencia detectada:** Si hay fechas límite, plazos o situaciones críticas, mencionarlos. Si no, escribe "Sin urgencia".

                Sé directo, sin introducciones ni cierres. Solo el resumen estructurado.

                Análisis:

                {analisis_previo}"""
            }]
        )
        resumen = respuesta.message.content
        return resumen
    except Exception as e:
        print(f"[DOC_SERVICE] Error conectando a Máquina 2 ({OLLAMA_SUMMARIZER_HOST}): {e}")
        raise e
