O projeto Pulso Emocional é uma aplicação full-stack que utiliza Python no backend para processamento de IA e React no frontend para a interface. O sistema atua como um orquestrador que conecta a coleta de dados de mídia social à análise de sentimento.

🌐 Visão Geral dos Componentes Centrais

A lógica da aplicação é separada em três camadas principais, sendo o Backend em FastAPI o responsável por gerenciar a comunicação e o fluxo de dados.

Frontend (Interface do Usuário)

Tecnologia: Node.js/npm e React.js

Função: Prover a interface interativa onde o usuário insere a URL do YouTube e visualiza o Dashboard de Pulso Emocional com os resultados.

Backend (Lógica de Aplicação)

Tecnologia: Python e FastAPI

Função: Servir como o core de orquestração. Gerencia as requisições, coordena a chamada de APIs externas, executa a lógica de negócios e realiza o cálculo de métricas (e.g., Coeficiente Kappa).

Banco de Dados

Tecnologia: SQLite

Função: Garante a persistência dos dados, armazenando os resultados consolidados das análises de vídeo para consultas futuras.

Integração Essencial(IA e Dados) - A funcionalidade do sistema depende da comunicação direta com dois serviços externos, ambos orquestrados pelo Backend:

Google Gemini: Motor principal de IA responsável pela classificação do sentimento dos comentários (Positivo, Negativo, Neutro).

YouTube Data API: Fonte de dados para a coleta dos comentários do vídeo.

🔄 Fluxo de Análise de Sentimento (Workflow Detalhado)

O processo é uma sequência automatizada de 6 passos que transforma uma simples URL em insights de sentimento:

Início da Análise: O usuário submete a URL do vídeo via Frontend, que envia uma requisição HTTP POST ao Backend.

Coleta de Dados: O Backend utiliza a API do YouTube para coletar um volume de comentários associados ao video-id.

Classificação pela IA: Os comentários são enviados para a API do Gemini que retorna um rótulo de sentimento classificado para cada um.

Cálculo de Métricas: O Backend processa as classificações, calcula a distribuição percentual dos sentimentos e determina o Coeficiente Kappa (métrica de validação).

Persistência: Os resultados finais (resumo e métricas) são salvos de forma persistente no Banco de Dados.

Visualização: Os dados consolidados são retornados ao Frontend, que renderiza o dashboard de resultados para o usuário.