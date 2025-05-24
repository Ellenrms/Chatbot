from flask import Flask, request, jsonify
from gpt4all import GPT4All
import os

app = Flask(__name__)

# --- Model Configuration ---
model_name = os.environ.get("GPT4ALL_MODEL", "ggml-gpt4all-j-v1.3-groovy.bin")
model_path = os.environ.get("GPT4ALL_MODEL_PATH") # Optional: specify a directory for models

try:
    if model_path:
        app.logger.info(f"Attempting to load model: {model_name} from path: {model_path}")
        model = GPT4All(model_name=model_name, model_path=model_path)
    else:
        app.logger.info(f"Attempting to load model: {model_name} (no specific path)")
        model = GPT4All(model_name=model_name)
    app.logger.info("GPT4All model loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading GPT4All model: {e}")
    model = None # Set model to None if loading fails

@app.route('/api/v1/generate', methods=['POST'])
def generate():
    if model is None:
        return jsonify({"error": "Model not loaded. Please check server logs."}), 500

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Invalid request: 'message' key missing or not JSON."}), 400
        
        prompt = data['message']
        app.logger.info(f"Received prompt: {prompt}")

        max_tokens = data.get('max_tokens', 150)
        temp = data.get('temp', 0.7)
        top_k = data.get('top_k', 40)
        top_p = data.get('top_p', 0.9)

        output = model.generate(
            prompt,
            max_tokens=max_tokens,
            temp=temp,
            top_k=top_k,
            top_p=top_p
        )
        app.logger.info(f"Generated response: {output}")
        return jsonify({"response": output})

    except Exception as e:
        app.logger.error(f"Error during generation: {e}")
        return jsonify({"error": "An error occurred during text generation."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7861, debug=True)
