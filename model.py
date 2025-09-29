import os
import json
# Importaciones de Vertex AI (Necesarias para la estructura, pero los modelos están deshabilitados)
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
# Importaciones de Hugging Face
from huggingface_hub import InferenceClient

# Importamos la configuración
# NOTA: Debes asegurar que estas variables existan en un archivo llamado config.py en el mismo directorio.
from config import PARAMETERS, LLAMA3_MODEL_ID, GRANITE_MODEL_ID, MIXTRAL_MODEL_ID, HF_TOKEN

# Variables de entorno para Vertex AI (se asume que están configuradas para inicializar los clientes a None si fallan)
# GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", None)
# GCP_REGION = os.getenv("GCP_REGION", None)

# --- 1. Inicialización de clientes (Deshabilitado si no hay facturación) ---
# Inicialización simulada para evitar ImportError en app.py si se quitan las variables
# Si no usas Vertex AI, estas funciones se inicializarán a None y el app.py las bloqueará
llama3_response = None
granite_response = None
mixtral_response = None

# --- 6. Función de respuesta de Hugging Face (Salida de texto simple) ---
# Usamos una función separada para que su salida no intente ser tratada como JSON
def hf_deepseek_response(system_prompt, user_prompt):
    """Obtiene respuesta de texto simple de un modelo DeepSeek de Hugging Face."""
    
    # --- LOG DE DEPURACIÓN (CRÍTICO) ---
    # Imprimimos el estado del token
    print(f"DEBUG: Intentando llamar a DeepSeek con el token: {'[TOKEN OK]' if HF_TOKEN else '[TOKEN MISSING/EMPTY]'}")
    # -----------------------------------
    
    # Necesario para que la librería Hugging Face encuentre el token
    os.environ["HF_TOKEN"] = HF_TOKEN
    
    try:
        # 1. Inicializar el cliente
        client = InferenceClient()
        
        mensajes = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # --- LOG DE DEPURACIÓN (CRÍTICO) ---
        print("DEBUG: Enviando solicitud a Hugging Face (Timeout de 30s)...")
        # -----------------------------------
        
        # 2. Llamar a la API de chat con un TIMEOUT EXPLÍCITO
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=mensajes
            #timeout=30 # <--- AÑADIDO: Forzamos un timeout de 30 segundos
        )
        
        # --- LOG DE DEPURACIÓN (CRÍTICO) ---
        print("DEBUG: Solicitud completada exitosamente.")
        # -----------------------------------
        
        # 3. Retornar el texto
        return completion.choices[0].message.content
        
    except Exception as e:
        # --- LOG DE DEPURACIÓN (CRÍTICO) ---
        print(f"ERROR FATAL DE HUGGING FACE: {e}")
        # -----------------------------------
        # Devolvemos un mensaje de error claro al frontend
        return f"Error calling Hugging Face: {e}"

# Código de inicialización de los modelos Vertex AI (MANTENER para evitar errores de importación en app.py)

# ... (El resto del código si lo tuvieras, por ahora solo necesitamos esto)
