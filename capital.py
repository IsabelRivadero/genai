from huggingface_hub import InferenceClient
import os
from config import HF_TOKEN

# 🚨 El archivo original usaba librerías de IBM, ahora lo reemplazamos
# con una llamada simple al modelo de Hugging Face.

def get_deepseek_response(prompt):
    """Genera una respuesta de texto usando el cliente de DeepSeek de Hugging Face."""
    # Establece el token de HF (si no está ya en el entorno)
    os.environ["HF_TOKEN"] = HF_TOKEN
    
    try:
        client = InferenceClient()
        
        # Formato de chat simple
        mensajes = [
            {"role": "system", "content": "You are an expert assistant who provides concise and accurate answers."},
            {"role": "user", "content": prompt}
        ]
        
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=mensajes
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error al llamar a Hugging Face: {e}"

# Ejecutar el ejemplo
prompt = "What is the capital of Canada? Tell me a cool fact about it as well"
print("DeepSeek Response:")
print(get_deepseek_response(prompt))
