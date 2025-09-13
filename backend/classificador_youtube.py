from classificador import *
import requests
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from pathlib import Path
import argparse

CHAVE_KEY = "keys/youtube.key"
MAXIMO_RESULTADOS = 60
URL_COMENTARIOS = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&order=relevance"

def iniciar(id_video, maximo_resultados = MAXIMO_RESULTADOS):
    sucesso, url = False, None

    try:
        with open(CHAVE_KEY, "r") as arquivo_chave:
            chave = arquivo_chave.read().strip()
            n = max(1, min(100, int(maximo_resultados)))
            url = f"{URL_COMENTARIOS}&videoId={id_video}&maxResults={n}&key={chave}"

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro iniciando acesso ao comentários do youtube: {str(e)}")

    return sucesso, url

def get_comentarios(url):
    sucesso, comentarios = False, []
    try:
        resp = requests.get(url, timeout=20)
        if not resp.ok:
            print(f"erro HTTP ao acessar comentários: {resp.status_code} - {resp.text[:200]}")
            return False, []
        resposta = resp.json()
        items = resposta.get("items", [])
        for item in items:
            try:
                conteudo = item["snippet"]["topLevelComment"]["snippet"]
                comentarios.append({
                    "autor": conteudo.get("authorDisplayName"),
                    "texto": (conteudo.get("textOriginal") or "").strip(),
                    "curtidas": conteudo.get("likeCount"),
                    "data": conteudo.get("publishedAt")
                })
            except Exception:
                continue
        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro acessando os comentários: {str(e)}")
    return sucesso, comentarios

def classificar_comentarios(comentarios):
    for comentario in comentarios:
        texto = comentario.get("texto","").replace("\n", "")
        sucesso, classificacao = classificar(IA, texto)        
        if sucesso:
            comentario.update(classificacao)
        else:
            comentario.update({"polaridade": "erro", "emocao": "erro"})
    return comentarios

def gerar_planilha(video_id: str, n: int = 61, saida: str = "resultados_da_ia.xlsx"):
    sucesso_url, url = iniciar(video_id, maximo_resultados=n)
    if not sucesso_url:
        print("não foi possível montar a URL de coleta")
        return
    sucesso_comentarios, comentarios = get_comentarios(url)
    if not sucesso_comentarios or not comentarios:
        print("não foi possível obter comentários do YouTube")
        return
    sucesso_ia, ia = iniciar_IA()
    if not sucesso_ia:
        print("não foi possível iniciar a IA")
        return
    globals()["IA"] = ia
    comentarios = classificar_comentarios(comentarios)
    registros = []
    for c in comentarios:
        texto = str(c.get("texto", "")).replace("\n", " ").strip()
        pol = c.get("polaridade") or c.get("sentimento") or c.get("label") or "DESCONHECIDO"
        if texto:
            registros.append({"Texto": texto, "Polaridade": pol})
    if not registros:
        print("nenhum registro válido para salvar")
        return
    df = pd.DataFrame(registros)
    destino = Path(saida)
    try:
        if destino.suffix.lower() == ".xlsx":
            df.to_excel(destino, index=False, engine="openpyxl")
        else:
            df.to_csv(destino, index=False, encoding="utf-8")
        print(f"arquivo '{destino.name}' criado com sucesso com {len(df)} linhas")
    except ImportError:
        alt = destino.with_suffix('.csv')
        df.to_csv(alt, index=False, encoding='utf-8')
        print(f"biblioteca 'openpyxl' não encontrada. salvei como CSV: '{alt.name}'")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coleta, classifica e gera planilha (Texto, Polaridade) de comentários do YouTube.")
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--n", type=int, default=61)
    parser.add_argument("--saida", default="resultados_da_ia.xlsx")
    args = parser.parse_args()
    gerar_planilha(args.video_id, max(1, min(61, args.n)), args.saida)
