Estrutura e Operação do Banco de Dados

Este documento descreve a arquitetura e os scripts de operação do banco de dados do projeto, que utiliza SQLAlchemy para gerenciar a persistência de dados.

1. Propósito

O banco de dados, denominado data.db, foi projetado para armazenar as análises de sentimento realizadas pelo sistema. Ele serve como o repositório central para todos os dados classificados, garantindo persistência e acessibilidade para futuras análises e uso pela aplicação.

2. Tecnologias

SQLAlchemy: Utilizado como um ORM (Object-Relational Mapper), permitindo a manipulação dos dados por meio de objetos Python em vez de comandos SQL brutos.

SQLite: Banco de dados relacional leve, ideal para a fase de desenvolvimento e para a portabilidade do projeto.

3. Estrutura do Banco de Dados

O banco de dados consiste em uma única tabela que mapeia a classe de modelo Analise.

Tabela: analises

Coluna	| Tipo	| Descrição
id	| Integer	| Chave primária e identificador único da análise.
texto	| String | 	O texto original que foi analisado.
polaridade	| String |	O resultado da análise (ex: 'POSITIVO', 'NEGATIVO').
origem	| String	| A fonte do texto (ex: 'imdb-reviews').
confianca | 	Float	| O nível de confiança da análise.
criado_em	| DateTime	| Data e hora em que a análise foi registrada.

4. Arquivos e Scripts

A interação com o banco de dados é gerenciada pelos seguintes arquivos, localizados em sua estrutura de pastas:

Arquivo	Descrição
backend/database/db.py	Configuração da Conexão: Inicializa a engine do banco de dados e a classe base Base para os modelos.
backend/models.py	Definição do Modelo: Contém a classe Analise, que define o esquema da tabela analises no banco de dados.
backend/services/crud.py	Operações de Dados: Funções para interagir com o banco de dados, como salvar (salvar_analise) e listar (listar_analises) registros.
create_db.py	Script de Criação: Responsável por criar o banco de dados e todas as tabelas, com base nos modelos definidos. Deve ser executado apenas uma vez.
import_data.py	Script de Importação: Lê dados de uma planilha externa (.xlsx) e os importa para a tabela analises usando as funções de serviço.
5. Guia de Uso

Para configurar e popular o banco de dados, siga as instruções abaixo em seu terminal.

Crie a Estrutura do Banco de Dados:
Este passo cria o arquivo data.db e a tabela analises. Execute-o apenas uma vez.

python create_db.py
Importe os Dados Iniciais:
Este passo lê a planilha de origem e popula a tabela analises com os dados.

python import_data.py