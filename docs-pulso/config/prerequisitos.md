Para configurar e executar o projeto Pulso Emocional com sucesso, você precisará ter as seguintes ferramentas instaladas e acessíveis em sua máquina (Mac, Linux ou Windows).

🛠️ Ferramentas de Desenvolvimento

Python (3.10 ou superior): Essencial para o Backend (FastAPI, lógica de IA) e para o gerenciador de pacotes pip.

pip: O gerenciador de pacotes padrão do Python, usado para instalar as dependências do requirements.txt.

Node.js e npm: Necessários para o Frontend (React.js) e para gerenciar todas as dependências do lado do cliente.

Git: Utilizado para clonar o repositório do código-fonte.

🔑 Chaves de Acesso (APIs)

O funcionamento da análise de sentimentos depende de duas chaves de API, que devem ser obtidas separadamente e configuradas no arquivo .env.

GEMINI_API_KEY: Chave de acesso à API do Google Gemini, necessária para o processamento e classificação de sentimentos.

YOUTUBE_API_KEY: Chave da API do YouTube Data v3, essencial para a coleta dos comentários dos vídeos.

Verificação de Instalação

Você pode verificar se as ferramentas estão corretamente instaladas e acessíveis no seu terminal:

Bash
python --version
node --version
npm --version