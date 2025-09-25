from utils.inicializacao_IA import iniciar_IA, obter_resposta
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import argparse
import json
from collections import Counter

EMOCOES_PADRAO = ["alegria","tristeza","raiva","medo","nojo","desprezo","surpresa","expectativa"]

def carregar_comentarios(caminho: str) -> list:
    df = pd.read_excel(caminho) if caminho.lower().endswith(".xlsx") else pd.read_csv(caminho)
    df = df.fillna("")
    if "Texto" not in df.columns:
        return []
    textos = [str(t).strip() for t in df["Texto"].tolist()]
    textos = [t for t in textos if t]
    return textos

def montar_prompt_emocao(texto: str, emocoes: list) -> (SystemMessage, HumanMessage):
    conteudo = f"""
Você é um assistente que classifica a emoção predominante de um texto curto.
Escolha exatamente uma emoção dentre: {', '.join(emocoes)}.
Retorne apenas JSON no formato: {{"emocao": "<uma_emocao_da_lista>"}}.
Não retorne explicações, apenas o JSON válido.
    """.strip()
    return SystemMessage(content=conteudo), HumanMessage(content=f'Texto: "{texto}"\nClassificação:')

def classificar_emocao(ia, texto: str, emocoes: list) -> str:
    sys_msg, hum_msg = montar_prompt_emocao(texto, emocoes)
    sucesso, resposta = obter_resposta(ia, [sys_msg, hum_msg])
    if not sucesso:
        return "indefinida"
    bruto = str(resposta.content).replace("```json","").replace("```","").strip()
    try:
        obj = json.loads(bruto)
        rotulo = str(obj.get("emocao","")).strip().lower()
        return rotulo if rotulo in [e.lower() for e in emocoes] else "indefinida"
    except Exception:
        return "indefinida"

def gerar_emocoes(textos: list, ia, emocoes: list) -> list:
    resultado = []
    for t in textos:
        rotulo = classificar_emocao(ia, t, emocoes)
        resultado.append({"Texto": t, "Emocao": rotulo})
    return resultado

def salvar_planilha(registros: list, destino: str) -> None:
    df = pd.DataFrame(registros)
    caminho = Path(destino)
    if caminho.suffix.lower() == ".xlsx":
        df.to_excel(caminho, index=False)
    else:
        df.to_csv(caminho, index=False, encoding="utf-8")

def gerar_nuvem_emocoes(registros: list, destino_imagem: str) -> None:
    contagem = Counter([r["Emocao"] for r in registros if r.get("Emocao")])
    if not contagem:
        return
    wc = WordCloud(width=1600, height=900, background_color="white")
    wc.generate_from_frequencies(contagem)
    plt.figure(figsize=(10,6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    Path(destino_imagem).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(destino_imagem, dpi=200)
    plt.close()

def executar(entrada: str, saida_planilha: str, saida_imagem: str, categorias: list) -> None:
    textos = carregar_comentarios(entrada)
    if not textos:
        print("nenhum texto encontrado em 'Texto'.")
        return
    ok, ia = iniciar_IA()
    if not ok:
        print("não foi possível iniciar a IA.")
        return
    registros = gerar_emocoes(textos, ia, categorias)
    salvar_planilha(registros, saida_planilha)
    gerar_nuvem_emocoes(registros, saida_imagem)
    print(f"planilha criada: {saida_planilha}")
    print(f"nuvem de palavras criada: {saida_imagem}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classifica emoções e gera nuvem de palavras a partir de comentarios.xlsx.")
    parser.add_argument("--entrada", default="comentarios.xlsx")
    parser.add_argument("--saida-planilha", default="emocoes.xlsx")
    parser.add_argument("--saida-imagem", default="nuvem_emocoes.png")
    parser.add_argument("--categorias", nargs="*", default=EMOCOES_PADRAO)
    args = parser.parse_args()
    executar(args.entrada, args.saida_planilha, args.saida_imagem, args.categorias)
    

def analisar_emocoes(textos: list, ia, categorias: list | None = None) -> list:
    cats = categorias if categorias else EMOCOES_PADRAO
    return gerar_emocoes(textos, ia, cats)