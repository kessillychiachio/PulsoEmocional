import argparse
from backend.database.db import SessionLocal
from backend.services.crud import obter_video_por_id_youtube, criar_video, salvar_comentario
from backend.utils.inicializacao_IA import iniciar_IA, obter_resposta
from backend.utils.classificador import classificar
from backend.utils.emocoes import analisar_emocoes, EMOCOES_PADRAO
from backend.utils.youtube_api import construir_url_comentarios, buscar_comentarios, obter_titulo_youtube
from backend.utils.youtube_api import LIMITE_COMENTARIOS

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

        titulo_video = obter_titulo_youtube(video_id)
        if titulo_video:
            print(f"Título do vídeo encontrado: {titulo_video}")
        else:
            print(f"Aviso: Não foi possível obter o título para o vídeo {video_id}.")

        novo_video_db = criar_video(db, video_id, titulo=titulo_video)
        print(f"Vídeo {video_id} criado no banco com ID interno {novo_video_db.id}.")

        sucesso_url, url_comentarios = construir_url_comentarios(video_id, n)
        if not sucesso_url:
            db.rollback()
            return

        sucesso_comentarios, comentarios = buscar_comentarios(url_comentarios)
        if not sucesso_comentarios or not comentarios:
            print("Nenhum comentário válido para processar. Encerrando.")
            db.rollback()
            return

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

    except Exception as e:
        print(f"ERRO FATAL: Falha na transação. Fazendo rollback: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Busca, analisa e salva comentários de um vídeo do YouTube no banco de dados.")
    parser.add_argument("--video-id", required=True, help="ID do vídeo do YouTube.")
    parser.add_argument("--n", type=int, default=LIMITE_COMENTARIOS, help="Número de comentários a buscar (máx. 60).")
    args = parser.parse_args()
    
    analisar_e_salvar_comentarios_do_video(args.video_id, args.n)