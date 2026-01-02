"""
Servidor Flask para la aplicación de detección de emociones.
Este módulo define las rutas para procesar texto y devolver análisis de emociones.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_predictor

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emot_detector():
    """
    Analiza el texto recibido y devuelve las puntuaciones de las emociones.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_predictor(text_to_analyze)

    # Gestión de errores para entradas vacías o inválidas (Tarea 7)
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is 'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, 'fear': {response['fear']}, "
        f"'joy': {response['joy']} and 'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
    """
    Renderiza la página principal de la aplicación.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
