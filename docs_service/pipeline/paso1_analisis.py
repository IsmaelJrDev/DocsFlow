from ollama import Client
from config import OLLAMA_ANALYZER_HOST

def analizar_texto(texto: str) -> str:
    print(f"[DOC_SERVICE] Enviando a Máquina 1 (llama3 @ {OLLAMA_ANALYZER_HOST})...")
    try:
        cliente = Client(host=OLLAMA_ANALYZER_HOST)
        respuesta = cliente.chat(
            model='llama3',
            messages=[{
                'role': 'user',
                'content': f"""Eres un asistente de análisis de documentos en un entorno de oficina corporativa.

                Analiza el siguiente texto y extrae la información relevante bajo estos criterios:

                - **Tipo de documento:** (contrato, reporte, correo, manual, solicitud, CV, otro)
                - **Ideas principales:** Lista las 3 a 5 ideas más importantes del contenido.
                - **Entidades mencionadas:** Personas, empresas, fechas, montos o lugares relevantes.
                - **Indicadores de urgencia:** Palabras o frases que sugieran plazos, deadlines o situaciones críticas. Si no hay, escribe "Ninguno".
                - **Tono del documento:** (formal, informal, técnico, legal, informativo)

                Sé directo y estructurado. No agregues introducciones ni conclusiones propias.

                Texto:

                {texto}"""
            }]
        )
        analisis = respuesta.message.content
        return analisis
    except Exception as e:
        print(f"[DOC_SERVICE] Error conectando a Máquina 1 ({OLLAMA_ANALYZER_HOST}): {e}")
        raise e
