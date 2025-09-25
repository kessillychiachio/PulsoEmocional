import pandas as pd
from backend.database.db import SessionLocal
from backend.services.crud import criar_video, salvar_comentario

PLANILHA = "classificacoes/imdb-reviews-pt-br.xlsx"

def importar_dados_da_planilha():
    df = pd.read_excel(PLANILHA, header=0)
    db = SessionLocal()
    
    try:
        id_do_video_yt = "D2KIu_yDeJk"
        video_db = criar_video(db=db, video_id_youtube=id_do_video_yt)
        
        for index, row in df.iterrows():
            texto = row['text_pt']
            polaridade = 'NEGATIVO' if row['sentiment'] == "neg" else "POSITIVO"
            
            emocao = "" 
            
            salvar_comentario(
                db=db,
                video_id=video_db.id,
                texto=texto,
                polaridade=polaridade,
                emocao=emocao
            )
        
        print(f"Foram gravadas {len(df)} classificações para o vídeo {id_do_video_yt}.")

    finally:
        db.close()

if __name__ == "__main__":
    importar_dados_da_planilha()