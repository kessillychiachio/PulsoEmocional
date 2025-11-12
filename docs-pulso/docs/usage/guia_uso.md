O projeto Pulso Emocional é aberto a contribuições. Seja para reportar um bug, sugerir um novo recurso ou enviar código, sua ajuda é muito bem-vinda!

1. Relatório de Bugs e Sugestões

Antes de abrir uma Pull Request (PR), siga estas diretrizes:

- Bugs (Erros):

Verifique se o erro já foi reportado na seção Issues do repositório.

Ao criar um novo Issue, inclua o máximo de detalhes possível, como: passos para reproduzir o erro, sua versão do Python e Node.js e o stack trace completo (se houver).

- Sugestões de Recursos:

Use a seção Issues para propor novas funcionalidades. Descreva claramente o problema que o recurso resolve e qual seria o benefício para o projeto.

2. Configuração do Ambiente Local

- Para começar a codificar, siga os passos de configuração que você encontra em:

Pré-requisitos: config/prerequisitos.md

Instalação: config/instalacao.md

Execução: execution/execucao.md

Lembre-se de que é essencial rodar o Backend (uvicorn) e o Frontend (npm run dev) em paralelo.

3. Diretrizes de Codificação

- Para manter a consistência do código, solicitamos que os contribuidores sigam estas práticas:

Python (Backend): Adote a formatação PEP 8. Use type hinting (dicas de tipo) sempre que possível, especialmente nas funções do FastAPI.

JavaScript (Frontend): Siga as convenções modernas do React. Evite o uso de variáveis globais e garanta que os componentes sejam acessíveis (Accessibility/A11y).

Commits: Use mensagens de commit claras e descritivas (ex: feat: Adiciona campo para novo cálculo de Kappa ou fix: Corrige erro de porta no uvicorn).

4. Processo de Pull Request (PR)

Crie um fork do repositório.

- Crie uma branch nova com um nome descritivo (ex: feature/novo-dashboard ou fix/bug-instalacao).

git checkout -b nome-da-sua-branch

Implemente seu código ou correção.

- Execute os Testes: Certifique-se de que todos os testes existentes (tests/guia_testes.md) continuam passando.

- Envie sua PR: Certifique-se de que sua branch está atualizada com a main antes de enviar. Descreva suas alterações no corpo da PR.

Seu código será revisado pela equipe principal e, se aprovado, será integrado ao projeto!