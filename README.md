# Pulso Emocional: um MicroSaaS para Análise Automática de Sentimentos baseada em Inteligência Artificial

O Pulso Emocional é uma aplicação web que oferece uma funcionalidade específica e focada: a análise de sentimentos de comentários do YouTube através da IA.

## Pré-requisitos

Python 3.10 ou superior

pip (gerenciador de pacotes do Python)

## Instalação

1) Clone o Repositório:

git clone https://github.com/kessillychiachio/PulsoEmocional.git

cd PulsoEmocional

2) Crie o Ambiente Virtual:

python3.13 -m venv venv

3) Ative o ambiente virtual:

source venv/bin/activate

4) Instale as Dependências:

pip install -r requirements.txt

## Como Rodar o Projeto - para testes

cd backend
cd testes

python inicializacao_IA.py

python inicializacao_banco.py

python classificador.py

python classificador_youtube.py --video-id <videoid> // passa o video id no shell para determinar o video que sera analisado, sem as <> // O video que foi usado para fazer a avaliacao do projeto foi o: https://www.youtube.com/watch?v=D2KIu_yDeJk

python validadores_humanos.py

python coeficiente_kappa.py

## Como Rodar o Projeto - back e front
Com a venv ativa
Em um terminal, va ate a pasta backend e rode uvicorn main:app --reload
Em outro terminal, va ate a pasta frontend e rode npm run dev 
