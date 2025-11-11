from backend.utils.classificador import classificar
from backend.utils.inicializacao_IA import iniciar_IA
import requests
import pandas as pd
from pathlib import Path
import argparse
import os 
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") 

LIMITE_COMENTARIOS = 60
URL_BASE = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&order=relevance"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos" 

def construir_url_comentarios(video_id: str, n: int) -> tuple[bool, str | None]:
    try:
        chave = YOUTUBE_API_KEY 
        
        if not chave:
            print(f"erro iniciando acesso aos comentários do youtube: Chave YOUTUBE_API_KEY não configurada.")
            return False, None
            
        n_ajustado = max(1, min(LIMITE_COMENTARIOS, int(n)))
        url = f"{URL_BASE}&videoId={video_id}&maxResults={n_ajustado}&key={chave}" 
        return True, url
    except Exception as e:
        print(f"erro iniciando acesso aos comentários do youtube: {str(e)}")
        return False, None

def buscar_comentarios(url: str) -> tuple[bool, list]:
    try:
        resp = requests.get(url, timeout=20)
        if not resp.ok:
            print(f"erro HTTP ao acessar comentários: {resp.status_code} - {resp.text[:200]}")
            return False, []
        dados = resp.json()
        items = dados.get("items", [])
        comentarios = []
        for item in items[:LIMITE_COMENTARIOS]:
            try:
                s = item["snippet"]["topLevelComment"]["snippet"]
                comentarios.append({"Texto": (s.get("textOriginal") or "").strip()})
            except Exception:
                continue
        return True, comentarios[:LIMITE_COMENTARIOS]
    except Exception as e:
        print(f"erro acessando os comentários: {str(e)}")
        return False, []

def buscar_titulo(video_id: str) -> str | None:
    chave = YOUTUBE_API_KEY
    if not chave:
        return f"Vídeo ID: {video_id} (Chave não configurada)"

    try:
        params = {
            "id": video_id,
            "key": chave,
            "part": "snippet",
            "fields": "items(snippet(title))",
        }
        resp = requests.get(YOUTUBE_VIDEOS_URL, params=params, timeout=10)
        resp.raise_for_status()
            
        dados = resp.json()
        items = dados.get("items", [])
        
        if items:
            return items[0]["snippet"]["title"]
            
        return f"Vídeo ID: {video_id} (Título não encontrado)"
        
    except Exception as e:
        return f"Vídeo ID: {video_id} (Erro de API: {str(e)})"


def classificar_comentarios(comentarios: list, ia) -> list:
    classificados = []
    for c in comentarios[:LIMITE_COMENTARIOS]:
        texto = (c.get("Texto") or "").replace("\n", " ").strip()
        if not texto:
            classificados.append({"Texto": ""})
            continue
        sucesso, rotulo = classificar(ia, texto)
        if sucesso and isinstance(rotulo, dict):
            pol = rotulo.get("polaridade") or "DESCONHECIDO"
        else:
            pol = "erro"
        classificados.append({"Texto": texto, "Polaridade": pol})
    return classificados

def salvar_tabela(registros: list, destino: Path) -> None:
    if not registros:
        print("nenhum registro válido para salvar")
        return
    df = pd.DataFrame(registros)
    try:
        if destino.suffix.lower() == ".xlsx":
            df.to_excel(destino, index=False, engine="openpyxl")
        else:
            df.to_csv(destino, index=False, encoding="utf-8")
        print(f"arquivo '{destino.name}' criado com {len(df)} linhas")
    except ImportError:
        alt = destino.with_suffix(".csv")
        df.to_csv(alt, index=False, encoding="utf-8")
        print(f"'openpyxl' não encontrado. salvei como CSV: '{alt.name}'")

def gerar_planilhas(video_id: str, n: int, saida_comentarios: str, saida_classificados: str) -> None:
    titulo = buscar_titulo(video_id)
    titulo_seguro = "".join(c for c in titulo if c.isalnum() or c.isspace()).strip()[:30].replace(' ', '_') if titulo else "Sem_Titulo"
    
    ok_url, url = construir_url_comentarios(video_id, n)
    if not ok_url:
        print("não foi possível montar a URL de coleta")
        return
    ok_com, comentarios = buscar_comentarios(url)
    if not ok_com or not comentarios:
        print("não foi possível obter comentários do YouTube")
        return
    comentarios = comentarios[:LIMITE_COMENTARIOS]
    
    for c in comentarios:
        c['Título'] = titulo
        c['VideoID'] = video_id
        
    base_comentarios = Path(saida_comentarios)
    base_classificados = Path(saida_classificados)
    
    novo_nome_com = base_comentarios.parent / f"{titulo_seguro}_{base_comentarios.name}"
    novo_nome_class = base_classificados.parent / f"{titulo_seguro}_{base_classificados.name}"
    
    salvar_tabela(comentarios, novo_nome_com)
    
    ok_ia, ia = iniciar_IA()
    if not ok_ia:
        print("não foi possível iniciar a IA")
        return
        
    classificados = classificar_comentarios(comentarios, ia)
    
    for c in classificados:
        c['Título'] = titulo
        c['VideoID'] = video_id
        
    salvar_tabela(classificados, novo_nome_class)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera duas planilhas: (1) comentários e (2) comentários + polaridade, até 60 linhas.")
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--n", type=int, default=LIMITE_COMENTARIOS)
    parser.add_argument("--saida-comentarios", default="comentarios.xlsx")
    parser.add_argument("--saida-classificados", default="resultados_da_ia.xlsx")
    args = parser.parse_args()
    gerar_planilhas(
        args.video_id,
        max(1, min(LIMITE_COMENTARIOS, args.n)),
        args.saida_comentarios,
        args.saida_classificados
    )