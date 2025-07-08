import os
import google.generativeai as genai

CHAVE_KEY="keys/google_ai_studio.key"
MODELO="gemini-1.5-flash"

def iniciar_IA():
    sucesso, modelo_ia = False, None
    try:
        with open(CHAVE_KEY, "r") as arquivo_chave:
            chave = arquivo_chave.read().strip()
            genai.configure(api_key=chave) 
            arquivo_chave.close()
            
            modelo_ia = genai.GenerativeModel(MODELO)
            
            sucesso = True
    except Exception as e:
        print(f"Ocorreu um erro iniciando acesso a IA: {str(e)}")

    return sucesso, modelo_ia

def obter_resposta(modelo_ia, prompt_texto):
    sucesso, resposta = False, None
    try:
        response_obj = modelo_ia.generate_content(prompt_texto)
        resposta = response_obj.text
        sucesso = True
    except Exception as e:
        print(f"Ocorreu um erro testando o prompt: {str(e)}")
        
    return sucesso, resposta

if __name__ == "__main__":
    sucesso, ia_pronta = iniciar_IA()

    if sucesso:
        print("Acesso à IA iniciado, iniciando o chat de teste...")
        
        prompt_de_teste = "Responda SIM se você consegue realizar análise de sentimentos sobre trechos de texto. Caso contrário, responda NÃO."
        
        sucesso, resposta = obter_resposta(ia_pronta, prompt_de_teste)
        
        if sucesso:
            print(f"Resposta: {resposta}")
        else:
            print("Não foi possível obter uma resposta para o teste de prompt.")
    else:
        print("Falha ao iniciar acesso à IA. Verifique as mensagens de erro acima.")