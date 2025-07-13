docker run -d --name my-whisper-transcriber \
  --gpus all \
  -p 5000:5000 \
  whisper-api-service


curl -X POST -F "file=@audio.ogg" \
     -F "language=Portuguese" \
     http://localhost:5000/transcribe

# **Transcritor de Áudio Whisper com Docker e GPU**

Este projeto fornece uma solução completa para transcrever áudios usando o modelo Whisper da OpenAI, empacotado em um container Docker com suporte a GPU, e uma interface web simples para facilitar o uso.

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
* **Git (opcional):** Para clonar o repositório.

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


    ├── app.py                  \# Código Python da API Flask para o Whisper
    ├── Dockerfile              \# Instruções para construir a imagem Docker
    ├── requirements.txt        \# Dependências Python para a API
    └── index.html              \# Interface web (HTML/JS) para interagir com o serviço

## **Como Usar**

Siga os passos abaixo para configurar e executar o serviço de transcrição.

### **1\. Clonar o Repositório (se aplicável)**

    git clone \<URL\_DO\_SEU\_REPOSITORIO\>
    cd \<nome\_do\_diretorio\>

### **2\. Construir a Imagem Docker**

Certifique-se de estar no diretório raiz do projeto (onde Dockerfile, app.py, requirements.txt estão localizados).

    docker build \-t whisper-api-service .

Este comando construirá a imagem Docker chamada whisper-api-service. Isso pode levar um tempo considerável na primeira vez, pois ele baixará a imagem base da NVIDIA CUDA, instalará as dependências do sistema e as bibliotecas Python (incluindo o modelo Whisper).

### **3\. Rodar o Container Docker como um Serviço**

Após a construção da imagem, você pode iniciar o serviço de transcrição. Certifique-se de que o NVIDIA Container Toolkit esteja configurado corretamente e que você esteja usando o contexto Docker apropriado (se aplicável, docker context use default).

    docker run \-d \--name my-whisper-transcriber \\
      \--gpus all \\
      \-p 5000:5000 \\
      whisper-api-service

* \-d: Roda o container em modo "detached" (em segundo plano).
* \--name my-whisper-transcriber: Atribui um nome amigável ao seu container.
* \--gpus all: Permite que o container acesse e utilize todas as GPUs disponíveis no seu sistema. **Crucial para o desempenho do Whisper.**
* \-p 5000:5000: Mapeia a porta 5000 do seu computador (host) para a porta 5000 dentro do container, onde a API Flask está escutando.

Você pode verificar se o container está rodando com:

docker ps

### **4\. Acessar a Interface Web**

Com o container rodando, você pode abrir a interface web no seu navegador.

1. Localize o arquivo index.html em seu sistema de arquivos.
2. Abra-o com seu navegador web preferido (Google Chrome, Mozilla Firefox, Microsoft Edge, etc.). Você pode arrastar o arquivo para a janela do navegador ou usar a opção "Abrir arquivo" no menu do navegador.

A interface web se comunicará com o serviço Dockerizado na porta 5000 do seu localhost.

### **5\. Transcrever Áudio**

Na interface web:

1. Clique em "Selecione um arquivo de áudio" e escolha um arquivo de áudio (MP3, WAV, etc.) do seu computador.
2. (Opcional) Selecione o idioma do áudio no menu suspenso. Se deixado como "Auto-detectar", o Whisper tentará identificar o idioma automaticamente.
3. Clique no botão "Transcrever Áudio".
4. Aguarde a conclusão da transcrição. O texto transcrito aparecerá na área designada.
5. Você pode usar o botão "Copiar Transcrição" para copiar o texto para a área de transferência.

## **Resolução de Problemas**

* **Erro de CORS (Access-Control-Allow-Origin):** Se você encontrar este erro no console do navegador, certifique-se de que seu `app.py` inclui from flask\_cors import CORS e CORS(app) e que você reconstruiu e reiniciou o container após essas alterações.
* **Container não inicia ou para imediatamente:** Verifique os logs do container para erros:
  docker logs my-whisper-transcriber

  Isso pode indicar problemas com dependências, o modelo Whisper ou a configuração da GPU.
* **Problemas com GPU:**
  * Verifique se o NVIDIA Container Toolkit está instalado corretamente.
  * Confirme se seus drivers NVIDIA estão atualizados.
  * Se estiver usando Docker Desktop, considere alternar para o Docker Engine nativo em Linux ou verificar a documentação do Docker Desktop para suporte a GPU.
  * Tente rodar um container de teste da NVIDIA para verificar o acesso à GPU:
        docker run \--rm \--gpus all nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04 nvidia-smi

    Se isso não funcionar, seu setup de GPU/Docker está incorreto.
