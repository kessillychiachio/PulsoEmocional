from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

import os

load_dotenv()
MODELO = "gemini-2.5-flash"

def iniciar_IA(contexto = None):
    sucesso, IA = False, None
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("ocorreu um erro iniciando acesso à IA: Chave 'GEMINI_API_KEY' não encontrada no ambiente.")
        return False, None
        
    try:
        os.environ["GOOGLE_API_KEY"] = api_key

        llm = ChatGoogleGenerativeAI(
            model=MODELO, 
            temperature=0, 
            max_output_tokens=None, 
            timeout=None, 
            max_retries=2
        )
        
        if contexto is not None:
            IA = ChatPromptTemplate.from_messages(contexto) | llm
        else:
            IA = llm

        sucesso = True
    except Exception as e:
        # 4. Captura qualquer erro de inicialização ou módulo
        print(f"ocorreu um erro iniciando acesso à IA: Falha ao carregar o modelo Langchain. Detalhe: {str(e)}")
    
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