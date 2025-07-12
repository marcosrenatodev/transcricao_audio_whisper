from flask import Flask, request, jsonify
import whisper
import os
import tempfile

app = Flask(__name__)

# Carrega o modelo Whisper globalmente para que seja carregado apenas uma vez
# Você pode mudar 'base' para 'small', 'medium', etc., dependendo da sua GPU e necessidade.
# O idioma padrão será detectado automaticamente se não for especificado na requisição.
print("Carregando o modelo Whisper 'base'...")
model = whisper.load_model("base")
print("Modelo Whisper 'base' carregado com sucesso.")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint para transcrever um arquivo de áudio enviado via POST.
    Espera um arquivo no campo 'file' do formulário.
    """
    if 'file' not in request.files:
        print("Erro: Nenhum arquivo 'file' na requisição.")
        return jsonify({"error": "Nenhum arquivo de áudio fornecido"}), 400

    file = request.files['file']

    if file.filename == '':
        print("Erro: Nome de arquivo vazio.")
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    if file:
        # Cria um arquivo temporário para salvar o áudio
        # Isso é importante porque o Whisper precisa de um caminho de arquivo
        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, file.filename)
        file.save(temp_audio_path)
        print(f"Arquivo temporário salvo em: {temp_audio_path}")

        try:
            # Opcional: Obter idioma da requisição, se fornecido
            # Ex: curl -F "file=@audio.mp3" -F "language=Portuguese" http://localhost:5000/transcribe
            language = request.form.get('language', None)
            print(f"Iniciando transcrição para o idioma: {language if language else 'Auto-detectar'}")

            # Realiza a transcrição
            # O fp16=False é recomendado para GPUs mais antigas ou se você tiver problemas de precisão
            result = model.transcribe(temp_audio_path, language=language, fp16=False)
            transcription = result["text"]
            print("Transcrição concluída.")
            return jsonify({"transcription": transcription}), 200
        except Exception as e:
            print(f"Erro durante a transcrição: {e}")
            return jsonify({"error": f"Erro durante a transcrição: {str(e)}"}), 500
        finally:
            # Limpa o arquivo temporário e o diretório
            os.remove(temp_audio_path)
            os.rmdir(temp_dir)
            print(f"Arquivo temporário {temp_audio_path} e diretório {temp_dir} removidos.")

if __name__ == '__main__':
    # Roda o servidor Flask.
    # host='0.0.0.0' torna o servidor acessível de fora do container.
    # port=5000 é a porta que a API irá escutar dentro do container.
    print("Iniciando o servidor Flask na porta 5000...")
    app.run(host='0.0.0.0', port=5000)
