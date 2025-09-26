import argparse
from backend.utils.inicializacao_IA import iniciar_IA, obter_resposta
from langchain_core.messages import HumanMessage, SystemMessage
from backend.database.db import SessionLocal
from backend.services.crud import obter_video_por_id_youtube, obter_comentarios_de_video, salvar_resumo

def criar_prompt(textos: list[str]) -> tuple[SystemMessage, HumanMessage]:
    s = (
        "Você analisa comentários de usuários em vídeos do YouTube. "
        "Escreva um único parágrafo objetivo, sem gírias e sem suposições externas. "
        "Identifique o(s) assunto(s) principal(is) e o tom geral das opiniões. "
        "Retorne somente o parágrafo."
    )
    amostra = " ".join(textos)
    h = f"Amostra de comentários:\n{amostra}"
    return SystemMessage(content=s), HumanMessage(content=h)

def gerar_resumo(textos: list[str]) -> str:
    ok, ia = iniciar_IA()
    if not ok:
        print("Falha ao iniciar IA para sumarização.")
        return ""
    sysm, hum = criar_prompt(textos)
    sucesso, resp = obter_resposta(ia, [sysm, hum])
    return str(resp.content).strip() if sucesso else ""

def main():
    parser = argparse.ArgumentParser(description="Gera e salva a sumarização dos comentários de um vídeo do YouTube.")
    parser.add_argument("--video-id", required=True, help="ID do vídeo do YouTube para sumarizar.")
    args = parser.parse_args()
    
    db = SessionLocal()
    
    try:
        # 1. Obter o vídeo pelo ID do YouTube
        video_db = obter_video_por_id_youtube(db, args.video_id)
        if not video_db:
            print(f"Erro: O vídeo '{args.video_id}' não foi encontrado no banco de dados.")
            return

        # 2. Obter os comentários do vídeo a partir do banco
        textos = obter_comentarios_de_video(db, video_db.id)
        if not textos:
            print("Nenhum comentário encontrado para sumarizar.")
            return

        # 3. Gerar o resumo usando a IA
        resumo = gerar_resumo(textos)
        if not resumo:
            print("Falha ao gerar o resumo.")
            return

        # 4. Salvar o resumo no banco de dados
        salvar_resumo(db, video_db.id, resumo)
        
        print("\n--- Resumo gerado e salvo no banco de dados ---")
        print(resumo)
        print("-------------------------------------------------")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()