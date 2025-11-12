Para que o projeto tenha acesso aos serviços de IA (Gemini) e de coleta de dados (YouTube), é necessário fornecer as chaves de API em um arquivo de configuração local.

1. Criar o Arquivo .env

Na raiz do projeto PulsoEmocional (ao lado do main.py e da pasta backend), crie um novo arquivo chamado .env

2. Adicionar as Chaves

Preencha o arquivo .env com as seguintes linhas, substituindo as aspas vazias ("") pelas chaves que você obteve nas plataformas Google Gemini e Google Cloud (para o YouTube):

GEMINI_API_KEY=""
YOUTUBE_API_KEY=""

Observação de Segurança e Privacidade: O arquivo .env nunca deve ser incluído no controle de versão (Git) para proteger suas credenciais. Certifique-se de que a linha .env esteja presente no arquivo .gitignore.