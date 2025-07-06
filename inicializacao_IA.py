from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import os

CHAVE_KEY = "keys/openai.key"
MODELO = "gpt-4o"

def iniciar_IA(contexto = None):
    sucesso, IA = False, None
    
    try:
        with open(CHAVE_KEY, "r") as arquivo_chave:
            chave = arquivo_chave.read()
            os.environ["OPENAI_API_KEY"] = chave

            arquivo_chave.close()

        llm = ChatOpenAI(model=MODELO, temperature=0, max_tokens=None, timeout=None, max_retries=2)
        IA = ChatPromptTemplate.from_messages(contexto) | llm if contexto is not None else llm

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro iniciando acesso à IA: {str(e)}")
    
    return sucesso, IA

def obter_resposta(IA, parametros):
    sucesso, resposta = False, None
    
    try:
        resposta = IA.invoke(parametros)
        
        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro testando o prompt: {str(e)}")

    return sucesso, resposta

if __name__ == "__main__":
    sucesso, IA = iniciar_IA()
    if sucesso:
        print("acesso à IA iniciado, iniciando o chat...")

        sucesso, resposta = obter_resposta(IA, [
            (
                "system", "Responda SIM se você consegue realizar análise de sentimentos sobre trechos de texto. Caso contrário, responda NÃO",
            )
        ])
        if sucesso:
            print(f"Resposta: {resposta.content}") 
