# Usa a imagem base da NVIDIA CUDA para suporte a GPU
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04

# Configurações básicas e instalação de dependências do sistema
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y \
    python3 python3-pip ffmpeg git curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Cria um usuário não-root e diretório de trabalho
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

# Define o diretório de trabalho e ajusta permissões
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências Python
COPY --chown=appuser:appuser requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    # Instala a versão fixa do Whisper (v20250625)
    pip3 install --no-cache-dir git+https://github.com/openai/whisper.git@v20250625

# Copia o aplicativo com permissões corretas
COPY --chown=appuser:appuser app.py .

# Cria diretório para uploads temporários (com permissões)
RUN mkdir -p /tmp/whisper_uploads && \
    chown appuser /tmp/whisper_uploads

# Expõe a porta do Flask
EXPOSE 5000

# Define o usuário não-root
USER appuser

# Comando para iniciar o servidor Flask em modo desenvolvimento
CMD ["python3", "app.py"]
