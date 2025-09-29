from flask import Flask, request, jsonify, render_template
# CORREGIDO: Solo importamos la función de DeepSeek que estamos utilizando
from model import hf_deepseek_response
import time
import json

app = Flask(__name__)

# NOTA: En un entorno de desarrollo real, necesitarías una carpeta 'templates' 
# con el archivo 'index.html'

@app.route('/', methods=['GET'])
def index():
    # Simulamos el contenido de index.html si no está presente
    # En una aplicación real, este archivo debe existir en la carpeta 'templates'
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Model Selector</title>
        <style>
            body { font-family: sans-serif; margin: 20px; background-color: #f4f7f9; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            label, select, textarea, button { display: block; width: 100%; margin-top: 10px; }
            textarea { height: 100px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; resize: vertical; }
            select, button { padding: 10px; border-radius: 4px; }
            button { background-color: #007bff; color: white; border: none; cursor: pointer; transition: background-color 0.3s; }
            button:hover { background-color: #0056b3; }
            #response-container { margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 4px; white-space: pre-wrap; }
            .error { color: red; }
            .model-disabled { color: orange; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Model Response Generator</h1>

            <label for="model-select">Select Model:</label>
            <select id="model-select">
                <option value="deepseek">DeepSeek (Hugging Face - Text Output)</option>
                <option value="llama3" disabled class="model-disabled">Llama3 (Vertex AI - JSON Output) [DISABLED]</option>
                <option value="granite" disabled class="model-disabled">Granite (Vertex AI - JSON Output) [DISABLED]</option>
                <option value="mixtral" disabled class="model-disabled">Mixtral (Vertex AI - JSON Output) [DISABLED]</option>
            </select>

            <label for="message-input">Your Message:</label>
            <textarea id="message-input" placeholder="Enter your query here..."></textarea>

            <button onclick="generateResponse()">Generate Response</button>

            <div id="response-container">Waiting for input...</div>
        </div>

        <script>
            async function generateResponse() {
                const message = document.getElementById('message-input').value;
                const model = document.getElementById('model-select').value;
                const responseContainer = document.getElementById('response-container');

                responseContainer.innerHTML = 'Generating response...';

                if (!message) {
                    responseContainer.innerHTML = '<span class="error">Please enter a message.</span>';
                    return;
                }

                try {
                    const startTime = Date.now();
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message, model })
                    });
                    responseContainer.innerHTML = 'Processing response...';
                    const data = await response.json();
                    const duration = ((Date.now() - startTime) / 1000).toFixed(2);

                    if (response.ok) {
                        let formattedOutput = '';
                        
                        if (data.type === 'json') {
                            formattedOutput = '--- JSON Response (For Vertex AI Models) ---\n';
                            formattedOutput += JSON.stringify(data.result, null, 2);
                        } else if (data.type === 'text') {
                            formattedOutput = '--- Text Response (For DeepSeek) ---\n';
                            formattedOutput += data.result;
                        }

                        responseContainer.innerHTML = `
                            <strong>Duration:</strong> ${duration}s<br><br>
                            <pre>${formattedOutput}</pre>`;
                    } else {
                        responseContainer.innerHTML = `<span class="error">Error (${response.status}):</span> ${data.error || 'Unknown error'}`;
                    }

                } catch (error) {
                    responseContainer.innerHTML = `<span class="error">Network Error:</span> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_message = data.get('message')
    model = data.get('model')
    
    if not user_message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400
    
    system_prompt = "You are an AI assistant helping with customer inquiries. Provide a helpful and concise response."
    
    start_time = time.time()
    
    try:
        if model in ['llama3', 'granite', 'mixtral']:
            # Devolvemos un error claro para el usuario en lugar de un 403 ilegible
            return jsonify({
                "error": f"Model '{model}' is currently disabled as it requires Google Cloud billing to be enabled.",
                "type": "error"
            }), 403
            
        elif model == 'deepseek':
            result_text = hf_deepseek_response(system_prompt, user_message)
            # Retornamos el resultado como texto
            return jsonify({
                "result": result_text,
                "type": "text",
                "duration": time.time() - start_time
            })
            
        else:
            return jsonify({"error": "Invalid model selection"}), 400
            
    except Exception as e:
        # Esto captura errores de red o errores de token de Hugging Face
        return jsonify({"error": str(e), "type": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
