from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.utils.inicializacao_IA import iniciar_IA
from backend.utils.youtube_api import construir_url_comentarios, buscar_comentarios, obter_titulo_youtube 
from backend.utils.classificador import classificar as classificar_polaridade
from backend.utils.emocoes import analisar_emocoes
from backend.utils.sumarizacao import gerar_resumo
from backend.services import crud
from backend.models.video_models import Video
import asyncio


def analisar_video_sincrono(db: Session, video_id_youtube: str, n_comentarios: int):
    video_existente = crud.obter_video_por_id_youtube(db, video_id_youtube)
    if video_existente:
        raise HTTPException(status_code=400, detail="Vídeo já analisado.")

    sucesso_ia, modelo_ia = iniciar_IA()
    if not sucesso_ia:
        raise HTTPException(status_code=500, detail="Falha ao iniciar a IA.")

    try:
        titulo = obter_titulo_youtube(video_id_youtube)
        
        novo_video_db = crud.criar_video(db, video_id_youtube, titulo=titulo)

        sucesso_url, url_comentarios = construir_url_comentarios(video_id_youtube, n_comentarios)
        if not sucesso_url:
            raise HTTPException(status_code=500, detail="Falha ao montar a URL de comentários do YouTube.")
        
        sucesso_com, comentarios = buscar_comentarios(url_comentarios)
        if not sucesso_com or not comentarios:
            raise HTTPException(status_code=404, detail="Nenhum comentário encontrado.")

        textos_para_sumarizar = []
        for comentario in comentarios:
            texto = comentario.get("Texto", "").replace("\n", " ").strip()
            if not texto:
                continue
            
            sucesso_pol, resultado_pol = classificar_polaridade(modelo_ia, texto)
            polaridade = resultado_pol.get("polaridade") if sucesso_pol and resultado_pol else "DESCONHECIDO"
            
            emocao_obj = analisar_emocoes(textos=[texto], ia=modelo_ia)
            emocao = emocao_obj[0].get("Emocao", "indefinida") if emocao_obj else "indefinida"
            
            crud.salvar_comentario(db=db, video_id=novo_video_db.id, texto=texto, polaridade=polaridade, emocao=emocao)
            textos_para_sumarizar.append(texto)

        if textos_para_sumarizar:
            resumo_gerado = gerar_resumo(textos_para_sumarizar)
            if resumo_gerado:
                crud.salvar_resumo(db, novo_video_db.id, resumo_gerado)
        
        db.commit() 
        
        return obter_video_analisado(db, video_id_youtube)

    except HTTPException:
        db.rollback() 
        raise

    except Exception as e:
        db.rollback() 
        print(f"Erro interno: Transação desfeita devido a falha no processamento. Erro: {e}")
        raise HTTPException(status_code=500, detail="Erro interno durante o processamento da análise do vídeo.")


def obter_video_analisado(db: Session, video_id_youtube: str):
    video_db = crud.obter_video_por_id_youtube(db, video_id_youtube)
    if not video_db:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado ou ainda não analisado.")
    return {
        "id": video_db.id,
        "video_id_youtube": video_db.video_id_youtube,
        "titulo": video_db.titulo,
        "resumo": video_db.resumo,
        "criado_em": video_db.criado_em,
        "comentarios": [
            {
                "id": c.id,
                "texto": c.texto,
                "polaridade": c.polaridade,
                "emocao": c.emocao
            }
            for c in video_db.comentarios
        ],
    }

    
def deletar_video_por_id(db: Session, video_id_youtube: str):
    video = crud.obter_video_por_id_youtube(db, video_id_youtube)
    if not video:
        return False
    
    sucesso = crud.deletar_video_por_id(db, video.id)
    return sucesso

def listar_videos(db: Session, limit: int, offset: int):
    return (
        db.query(Video)
        .order_by(Video.criado_em.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )