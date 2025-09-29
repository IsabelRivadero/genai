from model import llama3_response, granite_response, mixtral_response, hf_deepseek_response
import json

def call_all_models(system_prompt, user_prompt):
    print("--- Testing Vertex AI Models (JSON Output) ---")
    
    # 1. Llama3 (Vertex AI)
    try:
        llama_result = llama3_response(system_prompt, user_prompt)
        print("Llama3 (Vertex AI) Response (JSON):\n", json.dumps(llama_result, indent=2))
    except Exception as e:
        # Si la API falla, imprimirá el error sin detener todo el script
        print(f"Llama3 (Vertex AI) FAILED: {e}")

    # 2. Granite (Vertex AI)
    try:
        granite_result = granite_response(system_prompt, user_prompt)
        print("\nGranite (Vertex AI) Response (JSON):\n", json.dumps(granite_result, indent=2))
    except Exception as e:
        print(f"Granite (Vertex AI) FAILED: {e}")

    # 3. Mixtral (Vertex AI)
    try:
        mixtral_result = mixtral_response(system_prompt, user_prompt)
        print("\nMixtral (Vertex AI) Response (JSON):\n", json.dumps(mixtral_result, indent=2))
    except Exception as e:
        print(f"Mixtral (Vertex AI) FAILED: {e}")

    print("\n--- Testing Hugging Face Model (Text Output) ---")
    
    # 4. DeepSeek (Hugging Face)
    try:
        hf_deepseek_result = hf_deepseek_response(system_prompt, user_prompt)
        print("Hugging Face DeepSeek Response (TEXT):\n", hf_deepseek_result)
    except Exception as e:
        print(f"DeepSeek (HF) FAILED: {e}")


# Example call to test all models
call_all_models(
    "You are an AI assistant for a tech support company. Analyze the user's message and return the results as a JSON object, strictly following the required schema.", 
    "My keyboard suddenly stopped working after I installed the new operating system update."
)
