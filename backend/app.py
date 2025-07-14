from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import tempfile
import logging
import subprocess

# Configurações da aplicação
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# CORS(app, origins=["http://localhost:5500", "http://127.0.0.1:5500"])
# Libere todas as origens para desenvolvimento
CORS(app, resources={r"/*": {"origins": "*"}})
# Configura os logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega o modelo Whisper uma única vez
model_name = os.getenv("WHISPER_MODEL", "base")
logger.info(f"Carregando o modelo Whisper '{model_name}'...")
try:
    model = whisper.load_model(model_name)
    logger.info(f"Modelo Whisper '{model_name}' carregado com sucesso.")
except Exception as e:
    logger.error(f"Falha crítica ao carregar o modelo: {str(e)}")
    raise SystemExit(1)  # Encerra o aplicativo se o modelo não carregar

def preprocess_audio(input_path):
    """Converte o áudio para 16kHz mono (formato ideal para Whisper)"""
    output_path = input_path + "_processed.wav"
    subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-ar", "16000",     # Taxa de amostragem: 16kHz
        "-ac", "1",         # Mono
        "-c:a", "pcm_s16le", # Codec áudio PCM 16-bit
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_path

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint para transcrever áudio.
    Aceita apenas arquivos nos formatos: .wav, .mp3, .ogg, .flac, .opus
    """
    if 'file' not in request.files:
        logger.error("Nenhum arquivo enviado na requisição")
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    logger.info(f"Arquivo recebido: {file.filename}")

    # Validações do arquivo
    if file.filename == '':
        logger.error("Nome de arquivo vazio")
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    if not file.filename.lower().endswith(('.wav', '.mp3', '.ogg', '.flac', '.opus', '.m4a')):
        logger.error(f"Formato não suportado: {file.filename}")
        return jsonify({"error": "Formato não suportado. Use: .wav, .mp3, .ogg, .flac, .opus ou .m4a"}), 400

    # Processamento do áudio
    original_filename = file.filename
    temp_dir = tempfile.mkdtemp()
    temp_audio_path = os.path.join(temp_dir, file.filename)
    processed_audio_path = None

    try:
        # Salva o arquivo original temporariamente
        file.save(temp_audio_path)

        # Pré-processamento: converte para 16kHz mono
        processed_audio_path = preprocess_audio(temp_audio_path)
        logger.info(f"Áudio pré-processado: {processed_audio_path}")

        # Parâmetros de transcrição
        language = request.form.get('language', None)
        logger.info(f"Iniciando transcrição (idioma: {'auto-detect' if not language else language})")

        # Transcrição
        result = model.transcribe(
            processed_audio_path,
            language=language,
            fp16=False,
            task="transcribe"
        )

        return jsonify({
            "transcription": result["text"],
            "language": result["language"],
            "filename":  original_filename
        }), 200

    except subprocess.CalledProcessError as e:
        logger.error(f"Erro no pré-processamento: {str(e)}")
        return jsonify({"error": "Falha ao processar áudio"}), 500

    except Exception as e:
        logger.error(f"Erro na transcrição: {str(e)}")
        return jsonify({"error": f"Falha na transcrição: {str(e)}"}), 500

    finally:
        # Limpeza dos arquivos temporários
        try:
            for path in [temp_audio_path, processed_audio_path]:
                if path and os.path.exists(path):
                    os.remove(path)
            os.rmdir(temp_dir)
        except Exception as e:
            logger.warning(f"Erro ao limpar arquivos temporários: {str(e)}")

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask em modo desenvolvimento...")
    app.run(host='0.0.0.0', port=5000, debug=True)
