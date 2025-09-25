from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from backend.utils.inicializacao_IA import iniciar_IA
from backend.utils.classificador_youtube import construir_url_comentarios, buscar_comentarios
from services.crud import (
    obter_video_por_id_youtube,
    criar_video,
    salvar_comentario,
    salvar_resumo
)
from backend.utils.classificador import classificar as classificar_polaridade
from backend.utils.emocoes import analisar_emocoes
from backend.utils.sumarizacao import gerar_resumo

def _processar_analise_completa(db: Session, video_id_youtube: str, n_comentarios: int):
    sucesso_ia, modelo_ia = iniciar_IA()
    if not sucesso_ia:
        print("Falha ao iniciar a IA. Análise abortada.")
        return

    novo_video_db = criar_video(db, video_id_youtube)

    sucesso_url, url_comentarios = construir_url_comentarios(video_id_youtube, n_comentarios)
    if not sucesso_url: return

    sucesso_com, comentarios = buscar_comentarios(url_comentarios)
    if not sucesso_com or not comentarios:
        print("Nenhum comentário encontrado.")
        return
    
    textos_para_sumarizar = []
    for comentario in comentarios:
        texto = comentario.get("Texto", "").replace("\n", " ").strip()
        if not texto: continue
        
        sucesso_pol, resultado_pol = classificar_polaridade(modelo_ia, texto)
        polaridade = resultado_pol.get("polaridade") if sucesso_pol and resultado_pol else "DESCONHECIDO"
        
        emocao_obj = analisar_emocoes(textos=[texto], ia=modelo_ia)
        emocao = emocao_obj[0].get("Emocao", "indefinida") if emocao_obj else "indefinida"

        salvar_comentario(
            db=db,
            video_id=novo_video_db.id,
            texto=texto,
            polaridade=polaridade,
            emocao=emocao
        )
        textos_para_sumarizar.append(texto)

    # 2. Gerar e salvar o resumo
    if textos_para_sumarizar:
        resumo_gerado = gerar_resumo(textos_para_sumarizar)
        if resumo_gerado:
            salvar_resumo(db, novo_video_db.id, resumo_gerado)
            print(f"Resumo salvo para o vídeo {video_id_youtube}")

    print(f"Análise completa para o vídeo {video_id_youtube}.")


def iniciar_analise_completa(
    db: Session,
    video_id: str,
    n_comentarios: int,
    background_tasks: BackgroundTasks
):
    video_existente = obter_video_por_id_youtube(db, video_id)
    if video_existente:
        raise HTTPException(status_code=400, detail="Vídeo já analisado.")

    background_tasks.add_task(_processar_analise_completa, db, video_id, n_comentarios)
    return {"message": "Análise iniciada", "video_id": video_id}

def obter_video_analisado(db: Session, video_id_youtube: str):
    video_db = obter_video_por_id_youtube(db, video_id_youtube)
    if not video_db:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado ou ainda não analisado.")
    
    return {
        "id": video_db.id,
        "video_id_youtube": video_db.video_id_youtube,
        "resumo": video_db.resumo,
        "criado_em": video_db.criado_em,
        "comentarios": [
            {
                "texto": c.texto,
                "polaridade": c.polaridade,
                "emocao": c.emocao
            } for c in video_db.comentarios
        ]
    }