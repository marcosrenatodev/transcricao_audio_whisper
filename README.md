# **Transcritor de Áudio Whisper com Docker e GPU**

Este projeto fornece uma solução completa para transcrever áudios usando o modelo [Whisper da OpenAI](https://github.com/openai/whisper), empacotado em um container Docker com suporte a GPU, e uma interface web simples para facilitar o uso.

Neste projeto consegui rodar o modelo `base` ([ver outros modelos disponíveis](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages)) utilizando a minha NVIDIA GeForce GTX 1050 3GB de memória.

## **Visão Geral**

O projeto consiste em três partes principais:

1. **Serviço de API Whisper (Python/Flask):** Um backend leve que carrega o modelo Whisper e expõe um endpoint HTTP para receber arquivos de áudio e retornar suas transcrições.
2. **Container Docker:** Empacota o serviço de API e todas as suas dependências (incluindo suporte a CUDA para GPU) em um ambiente isolado e portátil.
3. **Interface Web (HTML/JavaScript/Tailwind CSS):** Uma página web simples que permite ao usuário selecionar um arquivo de áudio, enviá-lo para o serviço Dockerizado e exibir a transcrição resultante.

## **Pré-requisitos**

Antes de começar, certifique-se de ter os seguintes softwares instalados em seu sistema:

* **Docker:** Instale o Docker Engine.
* **NVIDIA Drivers:** Certifique-se de que seus drivers NVIDIA estão atualizados e corretamente instalados.
* **NVIDIA Container Toolkit:** Este é crucial para permitir que o Docker acesse sua GPU. Siga as instruções de instalação para o seu sistema operacional na documentação oficial: [NVIDIA Container Toolkit Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
* **Git:** Para clonar o repositório.

### **Configuração da GPU Local com Docker**

Para garantir que o Docker possa utilizar sua GPU local, é **fundamental** ter o **NVIDIA Container Toolkit** instalado e configurado corretamente. Este kit permite que o Docker runtime (containerd) interaja com os drivers NVIDIA e as bibliotecas CUDA.

**Importante: Docker Desktop e GPU**

O **Docker Desktop** (especialmente em sistemas Linux via WSL2 no Windows, ou macOS) pode ter um suporte limitado ou apresentar problemas de desempenho com o uso direto da GPU para containers. Ele geralmente não expõe a GPU de forma nativa e eficiente como o Docker Engine instalado diretamente em um sistema Linux.

Se você estiver enfrentando problemas de GPU com o Docker Desktop, é altamente recomendável:

1. **Usar um sistema Linux nativo:** Onde o Docker Engine e o NVIDIA Container Toolkit podem ser instalados diretamente.
2. **Trocar o contexto do Docker:** Se você usa o Docker Desktop e tem o Docker Engine instalado nativamente também, pode ser necessário alternar o contexto do Docker para usar o engine padrão do seu sistema, em vez do engine virtualizado do Docker Desktop. Para fazer isso, execute:
   docker context use default

Isso garantirá que seus comandos docker estejam interagindo com a instalação nativa do Docker que tem acesso à sua GPU.

## **Estrutura do Projeto**

    ├── backend/               # Serviço de API
    │   ├── app.py             # Código Flask
    │   ├── Dockerfile         # Configuração Docker
    │   └── requirements.txt   # Dependências Python
    ├── frontend/              # Interface web
    │   ├── index.html         # Página principal
    │   └── nginx.conf         # Configuração NGINX
    ├── docker-compose.yaml    # Orquestração de containers
    └── README.md              # Documentação

## **Configuração Rápida**

1. **Clonar o repositório:**
    ```
    git clone https://github.com/marcosrenatodev/transcricao_audio_whisper.git
    cd whisper-transcriber
    ```

2. **Executar o projeto:**

    Irá expor a aplicação na porta 80 por padrão.
    ```
    docker compose up
    ```
    É possível passar uma outra porta no comando, conforme exemplo(troque o 8080 pela porta desejada):
    ```
    PORT=8080 docker compose up
    ```
3. **Acessar a interface:**

    Abra no navegador: `http://localhost`


## **Resolução de Problemas**

* **Container não inicia ou para imediatamente:** Verifique os logs do container para erros:
  docker logs my-whisper-transcriber

  Isso pode indicar problemas com dependências, o modelo Whisper ou a configuração da GPU.
* **Problemas com GPU:**
  * Verifique se o NVIDIA Container Toolkit está instalado corretamente.
  * Confirme se seus drivers NVIDIA estão atualizados.
  * Se estiver usando Docker Desktop, considere alternar para o Docker Engine nativo em Linux ou verificar a documentação do Docker Desktop para suporte a GPU.
  * Tente rodar um container de teste da NVIDIA para verificar o acesso à GPU:

        docker run --rm --gpus all nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04 nvidia-smi

    Se isso não funcionar, seu setup de GPU/Docker está incorreto.
