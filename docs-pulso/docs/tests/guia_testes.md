Os testes são cruciais para validar a integração das APIs, a lógica de classificação e o cálculo de métricas (como o Coeficiente Kappa). Certifique-se de que o ambiente virtual esteja ativo antes de executar qualquer teste.

Execução dos Testes Unitários

- Navegue até a pasta que contém os scripts de teste:

cd backend/testes

- Execute cada script de teste sequencialmente, utilizando python:

Script	| Propósito
python inicializacao_IA.py	| Verifica se a conexão e a resposta básica da API do Gemini estão funcionando.

python inicializacao_banco.py	| Testa a inicialização e a conectividade com o Banco de Dados.

python classificador.py	| Testa a lógica interna do classificador de sentimentos (sem envolver a API do YouTube).

python validadores_humanos.py	| Executa testes na lógica de validação baseada em dados rotulados por humanos.

python coeficiente_kappa.py	| Valida o cálculo estatístico do Coeficiente Kappa usado para medir a concordância do classificador.

Teste de Classificação de Vídeo

- Este teste realiza a integração completa: coleta de dados do YouTube e classificação via IA. Você deve fornecer um ID de vídeo válido como argumento.

python classificador_youtube.py --video-id <videoid>

💡 Exemplo: Para testar com o vídeo usado na avaliação do projeto:

python classificador_youtube.py --video-id D2KIu_yDeJk