from ollama import Client
from config import OLLAMA_CLASSIFIER_HOST

def clasificar_documento(resumen: str) -> str:
    print(f"[DOC_SERVICE] Clasificando documento en Máquina 3 (phi3 @ {OLLAMA_CLASSIFIER_HOST})...")
    try:
        cliente = Client(host=OLLAMA_CLASSIFIER_HOST)
        respuesta = cliente.chat(
            model='phi3',
            messages=[{
                'role': 'user',
                'content': f"""
                Eres un asistente de clasificación de documentos en un entorno de oficina corporativa.

                Tu trabajo es asignar la prioridad a un documento según:

                    **Rojo (Alta prioridad):**
                    - Contiene fechas límite inmediatas (hoy, mañana, esta semana)
                    - Requiere acción urgente o decisión crítica
                    - Involucra problemas legales, financieros o de seguridad
                    - Escalaciones, quejas formales o incidentes activos

                    **Ámbar (Prioridad media):**
                    - Tareas o seguimientos sin fecha límite inmediata
                    - Reuniones, reportes o revisiones programadas
                    - Solicitudes pendientes de respuesta no urgente
                    - Proyectos en progreso sin bloqueos críticos

                    **Verde (Baja prioridad):**
                    - Información general, comunicados internos o boletines
                    - Documentos de referencia, manuales o CVs
                    - Confirmaciones, acuses de recibo o notificaciones rutinarias
                    - Contenido sin acción requerida

                    Responde ÚNICAMENTE con una palabra: "Rojo", "Ámbar" o "Verde".

                    Resumen:

                {resumen}"""
            }]
        )
        clasificacion = respuesta.message.content.strip()
        return clasificacion
    except Exception as e:
        print(f"[DOC_SERVICE] Error conectando a Máquina 3 ({OLLAMA_CLASSIFIER_HOST}): {e}")
        raise e
