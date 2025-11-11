import requests
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") 
LIMITE_COMENTARIOS = 60
URL_BASE = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&order=relevance"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

def construir_url_comentarios(video_id: str, n: int) -> tuple[bool, str | None]:
    chave = YOUTUBE_API_KEY
    if not chave:
        print("ERRO: A chave YOUTUBE_API_KEY não está configurada no ambiente.")
        return False, None
    
    try:
        n_ajustado = max(1, min(LIMITE_COMENTARIOS, int(n)))
        url = f"{URL_BASE}&videoId={video_id}&maxResults={n_ajustado}&key={chave}"
        return True, url
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao montar a URL: {str(e)}")
        return False, None

def buscar_comentarios(url: str) -> tuple[bool, list]:
    try:
        resp = requests.get(url, timeout=20)
        if not resp.ok:
            print(f"ERRO: Falha na requisição HTTP: {resp.status_code} - {resp.text[:200]}")
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
        return True, comentarios
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao buscar os comentários: {str(e)}")
        return False, []

def obter_titulo_youtube(video_id: str) -> str | None:
    chave = YOUTUBE_API_KEY
    if not chave:
        print("AVISO: Chave YOUTUBE_API_KEY não configurada no ambiente.")
        return None

    try:
        params = {
            "id": video_id,
            "key": chave,
            "part": "snippet",
            "fields": "items(snippet(title))",
        }
        resp = requests.get(YOUTUBE_VIDEOS_URL, params=params, timeout=10)
        
        if not resp.ok:
            print(f"ERRO: Falha HTTP ao buscar título: {resp.status_code}")
            return None
            
        dados = resp.json()
        items = dados.get("items", [])
        
        if items:
            return items[0]["snippet"]["title"]
            
        return None
        
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao buscar o título: {str(e)}")
        return None