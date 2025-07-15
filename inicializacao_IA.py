from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

import os

CHAVE_KEY = "keys/gemini.key"
MODELO = "gemini-2.0-flash"

def iniciar_IA(contexto = None):
    sucesso, IA = False, None
    
    try:
        with open(CHAVE_KEY, "r") as arquivo_chave:
            chave = arquivo_chave.read().strip()
            os.environ["GOOGLE_API_KEY"] = chave

        llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0, max_output_tokens=None, timeout=None, max_retries=2)
        
        if contexto is not None:
            IA = ChatPromptTemplate.from_messages(contexto) | llm
        else:
            IA = llm

        sucesso = True
    except FileNotFoundError:
        print(f"ocorreu um erro iniciando acesso à IA: o arquivo de chave '{CHAVE_KEY}' não foi encontrado.")
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
            SystemMessage(content="Responda SIM se você consegue realizar análise de sentimentos sobre trechos de texto. Caso contrário, responda NÃO"),
            HumanMessage(content="Você é capaz de realizar análise de sentimentos?")
        ])
        if sucesso:
            print(f"Resposta (Análise de Sentimentos): {resposta.content}")
        else:
            print("Não foi possível obter resposta para a pergunta de análise de sentimentos.")