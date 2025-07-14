FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DEFAULT_TIMEOUT=300 \
    PIP_NO_CACHE_DIR=off \
    TORCH_CUDA_ARCH_LIST="8.6"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip ffmpeg git curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser && mkdir /app && chown appuser:appuser /app
WORKDIR /app

# Instala dependências Python em etapas (cache-friendly)
COPY --chown=appuser:appuser requirements.txt .

# 1. Instala torch separadamente com índices otimizados
RUN pip3 install --no-cache-dir -U pip && \
    pip3 install --no-cache-dir torch==2.3.1 torchaudio==2.3.1 \
    --index-url https://download.pytorch.org/whl/cu121

# 2. Instala outras dependências
RUN pip3 install --no-cache-dir -r requirements.txt

# 3. Instala Whisper com fallback para timeout estendido
RUN pip3 install --no-cache-dir --timeout 600 \
    git+https://github.com/openai/whisper.git@v20250625

# Copia aplicação e configura ambiente
COPY --chown=appuser:appuser app.py .
RUN mkdir -p /tmp/whisper_uploads && chown appuser /tmp/whisper_uploads

# Configurações finais
EXPOSE 5000
USER appuser
CMD ["python3", "app.py"]
