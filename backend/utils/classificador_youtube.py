import requests
import argparse
from langchain_core.messages import HumanMessage, SystemMessage

from backend.database.db import SessionLocal
from backend.services.crud import obter_video_por_id_youtube, criar_video, salvar_comentario
from backend.utils.inicializacao_IA import iniciar_IA, obter_resposta
from backend.utils.classificador import classificar
from backend.utils.emocoes import analisar_emocoes, EMOCOES_PADRAO

CHAVE_KEY = "keys/youtube.key"
LIMITE_COMENTARIOS = 60
URL_BASE = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&order=relevance"

def construir_url_comentarios(video_id: str, n: int) -> (bool, str | None):
    try:
        with open(CHAVE_KEY, "r") as f:
            chave = f.read().strip()
        n_ajustado = max(1, min(LIMITE_COMENTARIOS, int(n)))
        url = f"{URL_BASE}&videoId={video_id}&maxResults={n_ajustado}&key={chave}"
        return True, url
    except FileNotFoundError:
        print(f"ERRO: O arquivo de chave do YouTube '{CHAVE_KEY}' não foi encontrado.")
        return False, None
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao montar a URL: {str(e)}")
        return False, None

def buscar_comentarios(url: str) -> (bool, list):
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

def analisar_e_salvar_comentarios_do_video(video_id: str, n: int) -> None:
    db = SessionLocal()
    sucesso_ia, modelo_ia = iniciar_IA()
    
    if not sucesso_ia:
        print("Falha ao iniciar a IA. Encerrando.")
        db.close()
        return

    try:
        video_existente = obter_video_por_id_youtube(db, video_id)
        if video_existente:
            print(f"O vídeo {video_id} já existe no banco. Nenhum novo comentário será salvo.")
            return

        novo_video_db = criar_video(db, video_id)
        print(f"Vídeo {video_id} criado no banco com ID interno {novo_video_db.id}.")

        sucesso_url, url_comentarios = construir_url_comentarios(video_id, n)
        if not sucesso_url:
            return

        sucesso_comentarios, comentarios = buscar_comentarios(url_comentarios)
        if not sucesso_comentarios or not comentarios:
            print("Nenhum comentário válido para processar. Encerrando.")
            return

        comentarios_analisados = []
        for comentario in comentarios:
            texto = comentario.get("Texto", "").replace("\n", " ").strip()
            if not texto:
                continue

            sucesso_pol, resultado_pol = classificar(modelo_ia, texto)
            polaridade = resultado_pol.get("polaridade") if sucesso_pol and resultado_pol else "DESCONHECIDO"

            emocao_analisada = "indefinida"
            emocao_obj = analisar_emocoes(textos=[texto], ia=modelo_ia, categorias=EMOCOES_PADRAO)
            if emocao_obj and len(emocao_obj) > 0:
                emocao_analisada = emocao_obj[0].get("Emocao", "indefinida")

            salvar_comentario(
                db=db,
                video_id=novo_video_db.id,
                texto=texto,
                polaridade=polaridade,
                emocao=emocao_analisada
            )
        
        print(f"Análise e salvamento de {len(comentarios)} comentários concluídos com sucesso!")

    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Busca, analisa e salva comentários de um vídeo do YouTube no banco de dados.")
    parser.add_argument("--video-id", required=True, help="ID do vídeo do YouTube.")
    parser.add_argument("--n", type=int, default=LIMITE_COMENTARIOS, help="Número de comentários a buscar (máx. 60).")
    args = parser.parse_args()
    
    analisar_e_salvar_comentarios_do_video(args.video_id, args.n)