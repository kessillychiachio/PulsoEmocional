Siga os passos abaixo na raiz do seu terminal para preparar o ambiente local e instalar as dependências necessárias do Backend.

1. Clonar o Repositório

- Baixe o código-fonte do projeto utilizando o Git:

git clone https://github.com/kessillychiachio/PulsoEmocional.git
cd PulsoEmocional

2. Criar o Ambiente Virtual

- Recomendamos criar um ambiente virtual (venv) para isolar as dependências do projeto:

python3.10 -m venv venv

3. Ativar o Ambiente Virtual

A ativação é crucial para garantir que você esteja usando o Python e o pip corretos para o projeto. O comando varia de acordo com o seu sistema operacional:

- Linux/macOS:

source venv/bin/activate

- Windows (Prompt de Comando):
venv\Scripts\activate

- Windows (PowerShell):

venv\Scripts\Activate.ps1

4. Instalar as Dependências do Backend

- Com o ambiente virtual ativo, instale todas as bibliotecas Python listadas no requirements.txt:

pip install -r requirements.txt