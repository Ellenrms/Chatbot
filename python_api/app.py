from flask import Flask, request, jsonify
from gpt4all import GPT4All
import os

app = Flask(__name__)

# --- Model Configuration ---
model_name = os.environ.get("GPT4ALL_MODEL", "orca_mini_v3_7b.Q4_0.gguf")
model_path = os.environ.get("GPT4ALL_MODEL_PATH")  # Optional: specify a directory for models

try:
    if model_path:
        app.logger.info(f"🔄 Carregando modelo: {model_name} do caminho: {model_path}")
        model = GPT4All(model_name=model_name, model_path=model_path)
    else:
        app.logger.info(f"🔄 Carregando modelo: {model_name} (sem caminho específico)")
        model = GPT4All(model_name=model_name)
    app.logger.info("✅ Modelo GPT4All carregado com sucesso.")
except Exception as e:
    app.logger.error(f"❌ Erro ao carregar o modelo GPT4All: {e}")
    model = None

@app.route('/api/v1/generate', methods=['POST'])
def generate():
    if model is None:
        return jsonify({"error": "Model not loaded. Please check server logs."}), 500

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Invalid request: 'message' key missing or not JSON."}), 400
        
        prompt = data['message']
        app.logger.info(f"🟢 Prompt recebido: {prompt}")

        output = model.generate(
            prompt,
            max_tokens=data.get('max_tokens', 150),
            temp=data.get('temp', 0.7),
            top_k=data.get('top_k', 40),
            top_p=data.get('top_p', 0.9)
        )
        app.logger.info(f"🔵 Resposta gerada: {output}")
        return jsonify({"response": output})

    except Exception as e:
        app.logger.error(f"❌ Erro durante a geração: {e}")
        return jsonify({"error": "Erro na geração de texto."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7861, debug=True)
