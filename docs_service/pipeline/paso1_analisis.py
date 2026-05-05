from ollama import Client
from config import OLLAMA_ANALYZER_HOST

def analizar_texto(texto: str) -> str:
    print(f"[DOC_SERVICE] 🤖 Enviando a Máquina 1 (llama3 @ {OLLAMA_ANALYZER_HOST})...")
    try:
        cliente = Client(host=OLLAMA_ANALYZER_HOST)
        respuesta = cliente.chat(
            model='llama3',
            messages=[{
                'role': 'user',
                'content': f'Analiza el siguiente texto y extrae las ideas principales:\n\n{texto}'
            }]
        )
        analisis = respuesta.message.content
        return analisis
    except Exception as e:
        print(f"[DOC_SERVICE] ❌ Error conectando a Máquina 1 ({OLLAMA_ANALYZER_HOST}): {e}")
        raise e
