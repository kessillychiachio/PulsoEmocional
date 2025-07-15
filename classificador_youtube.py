from classificador import *
import requests

CHAVE_KEY = "keys/youtube.key"

MAXIMO_RESULTADOS = 30
URL_COMENTARIOS = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&order=relevance"

def iniciar(id_video, maximo_resultados = MAXIMO_RESULTADOS):
    sucesso, url = False, None

    try:
        with open(CHAVE_KEY, "r") as arquivo_chave:
            chave = arquivo_chave.read()
            url = f"{URL_COMENTARIOS}&videoId={id_video}&maxResults={maximo_resultados}&key={chave}"

            arquivo_chave.close()

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro iniciando acesso ao comentários do youtube: {str(e)}")

    return sucesso, url

def get_comentarios(url):
    sucesso, comentarios = False, []

    try:
        resposta = requests.get(url)
        resposta = resposta.json()

        for item in resposta["items"]:
            conteudo = item["snippet"]["topLevelComment"]["snippet"]
            comentarios.append({
                "autor": conteudo["authorDisplayName"],
                "texto": conteudo["textOriginal"], 
                "curtidas": conteudo["likeCount"],
                "data": conteudo["publishedAt"]
            })

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro acessando os comentários: {str(e)}")

    return sucesso, comentarios

def classificar_comentarios(comentarios):
    for comentario in comentarios:
        texto = comentario["texto"]
        texto = texto.replace("\n", "")

        sucesso, classificacao = classificar(IA, texto)        
        if sucesso:
            comentario.update(classificacao)

            print(f"o texto: '{texto}' tem polaridade {classificacao['polaridade']}")
        else:
            comentario.update({"polaridade": "erro", "emocao": "erro"})

            print(f"não foi possível classificar o texto '{texto}' sentimentalmente")

    return comentarios

def resumir_classificacoes(comentarios):
    positivas, negativas, neutras = 0, 0, 0

    for comentario in comentarios:
        positivas += 1 if comentario["polaridade"] == "POSITIVA" else 0
        negativas += 1 if comentario["polaridade"] == "NEGATIVA" else 0
        neutras += 1 if comentario["polaridade"] == "NEUTRA" else 0

    print(f"total de polaridades: positivas = {positivas}, negativas = {negativas}, neutras = {neutras}")

if __name__ == "__main__":
    sucesso, IA = iniciar_IA()

    if sucesso:
        id_video = "uYuxLi-FfSw"
        sucesso, url = iniciar(id_video)

        if sucesso:
            sucesso, comentarios = get_comentarios(url)
            if sucesso:
                resumir_classificacoes(classificar_comentarios(comentarios))