import argparse
from pathlib import Path
import pandas as pd
from inicializacao_IA import iniciar_IA, obter_resposta
from langchain_core.messages import HumanMessage, SystemMessage

ENTRADA_PADRAO = "resultados_da_ia.xlsx"
SAIDA_PADRAO = "sumarizacao.xlsx"
LIMITE = 60

def carregar_comentarios(caminho: str, limite: int) -> list[str]:
    p = Path(caminho)
    df = pd.read_excel(p) if p.suffix.lower() == ".xlsx" else pd.read_csv(p)
    df = df.fillna("")
    col_texto = next((c for c in df.columns if str(c).strip().casefold() in {"texto","comentario","comment"}), None)
    if not col_texto:
        raise ValueError("Coluna equivalente a 'Texto' não encontrada.")
    textos = df[col_texto].astype(str).str.strip().tolist()
    return [t for t in textos if t][:limite]

def criar_prompt(textos: list[str]) -> tuple[SystemMessage, HumanMessage]:
    s = (
        "Você analisa comentários de usuários em português. "
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
        return ""
    sysm, hum = criar_prompt(textos)
    sucesso, resp = obter_resposta(ia, [sysm, hum])
    return str(resp.content).strip() if sucesso else ""

def salvar_resumo(resumo: str, caminho: str) -> None:
    df = pd.DataFrame([{"Resumo": resumo}])
    p = Path(caminho)
    if p.suffix.lower() == ".xlsx":
        df.to_excel(p, index=False)
    else:
        df.to_csv(p, index=False, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(description="Gera um parágrafo de sumarização a partir de resultados_da_ia.")
    ap.add_argument("--entrada", default=ENTRADA_PADRAO)
    ap.add_argument("--saida", default=SAIDA_PADRAO)
    ap.add_argument("--n", type=int, default=LIMITE)
    args = ap.parse_args()
    try:
        textos = carregar_comentarios(args.entrada, args.n)
    except Exception as e:
        print(f"Erro ao ler '{args.entrada}': {e}")
        return
    if not textos:
        print("Nenhum comentário encontrado para sumarizar.")
        return
    resumo = gerar_resumo(textos)
    if not resumo:
        print("Falha ao gerar o resumo.")
        return
    salvar_resumo(resumo, args.saida)
    print(resumo)
    print(f"\nResumo salvo em '{args.saida}'.")

if __name__ == "__main__":
    main()