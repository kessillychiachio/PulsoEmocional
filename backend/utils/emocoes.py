
from backend.utils.inicializacao_IA import iniciar_IA, obter_resposta
from langchain_core.messages import HumanMessage, SystemMessage
import json
from typing import List, Union

EMOCOES_PADRAO = ["alegria","tristeza","raiva","medo","nojo","desprezo","surpresa","expectativa"]

def montar_prompt_emocao(texto: str, emocoes: list) -> tuple[SystemMessage, HumanMessage]:
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

def analisar_emocoes(textos: List[str], ia, categorias: List[str] | None = None) -> List[dict]:
    cats = categorias if categorias else EMOCOES_PADRAO
    resultado = []
    for t in textos:
        rotulo = classificar_emocao(ia, t, cats)
        resultado.append({"Texto": t, "Emocao": rotulo})
    return resultado