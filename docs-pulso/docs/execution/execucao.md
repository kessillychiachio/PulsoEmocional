O projeto é composto por serviços de Backend e Frontend que precisam ser iniciados simultaneamente, cada um em seu próprio terminal.

1. Iniciar o Backend (Servidor FastAPI)

O Backend deve ser iniciado primeiro, pois ele hospeda a lógica da API e a orquestração da IA.

Certifique-se de que a venv esteja ativa.

- Na raiz do projeto (/PulsoEmocional), execute o servidor Uvicorn:

uvicorn main:app --reload

ℹ️ Endereço: O Backend estará acessível em http://127.0.0.1:8000 (porta padrão). O parâmetro --reload é útil para desenvolvimento, pois reinicia o servidor automaticamente após alterações no código Python.

2. Iniciar o Frontend (Interface React)

O Frontend gerencia a interface do usuário e se comunica com o Backend.

>>> Abra um novo terminal.

- Navegue até o diretório do Frontend:

cd frontend

- Instale as dependências do Node.js (Necessário apenas na primeira execução):

npm install

- Inicie o servidor de desenvolvimento do Frontend:

npm run dev
