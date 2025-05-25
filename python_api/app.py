from flask import Flask, request, jsonify
from gpt4all import GPT4All
import os

app = Flask(__name__)

# --- Configuração do Modelo ---
# Modelo padrão que você confirmou estar usando: orca_mini_v3_7b.Q4_0.gguf
model_name = os.environ.get("GPT4ALL_MODEL", "orca_mini_v3_7b.Q4_0.gguf")
model_path = os.environ.get("GPT4ALL_MODEL_PATH") 

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
        # Mensagem de erro se o modelo não carregou
        return jsonify({"error": "Modelo GPT4All não carregado. Verifique os logs do servidor."}), 500

    try:
        data = request.get_json()
        if not data:
            # Validação se o JSON está vazio ou não é JSON
            return jsonify({"error": "Requisição JSON inválida ou vazia."}), 400

        # Obter 'prompt' (em vez de 'message')
        prompt = data.get('prompt')
        if not prompt:
            # Validação se a chave 'prompt' está presente
            return jsonify({"error": "Chave 'prompt' faltando ou vazia no JSON da requisição."}), 400
        
        app.logger.info(f"🟢 Prompt recebido: {prompt}")

        # Obter 'max_new_tokens' (em vez de 'max_tokens')
        max_tokens = data.get('max_new_tokens', 150) 
        temp = data.get('temp', 0.7)
        top_k = data.get('top_k', 40)
        top_p = data.get('top_p', 0.9)

        output = model.generate(
            prompt,
            max_tokens=max_tokens, # A variável interna do gpt4all pode ainda ser max_tokens
            temp=temp,
            top_k=top_k,
            top_p=top_p
        )
        app.logger.info(f"🔵 Resposta gerada: {output}")

        # Retornar no formato esperado pelo Spring Boot: {"results": [{"text": "..."}]}
        return jsonify({"results": [{"text": output}]})

    except Exception as e:
        app.logger.error(f"❌ Erro durante a geração: {e}")
        return jsonify({"error": "Erro interno na geração de texto."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7861, debug=True)