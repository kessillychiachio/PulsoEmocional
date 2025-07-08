from inicializacao_IA import iniciar_IA, obter_resposta
import json

def get_prompt_para_classificacao(
    texto: str,
    exemplos_positivos: list = None,
    exemplos_negativos: list = None,
    exemplos_neutros: list = None,
    emocoes: list = None
) -> str:
    if exemplos_positivos is None:
        exemplos_positivos = []
    if exemplos_negativos is None:
        exemplos_negativos = []
    if exemplos_neutros is None:
        exemplos_neutros = []
    if emocoes is None:
        emocoes = ['alegria', 'tristeza', 'raiva', 'medo', 'nojo', 'desprezo', 'surpresa']

    prompt_base = f"""
    Você é um assistente especializado em avaliar sentimentalmente trechos de texto.
    Você deve categorizar os textos em três polaridades: NEGATIVA, POSITIVA e NEUTRA.
    Você também deve determinar qual o tipo de emoção do texto.
    Limite-se a avaliar a emoção nas seguintes categorias: {', '.join(emocoes)}.
    A sua classificação deve ser uma estrutura JSON contendo: a polaridade associada ao atributo 'polaridade' e a emoção associada ao atributo 'emocao'.
    A sua classificação deve conter SOMENTE o conteúdo do JSON e NADA mais.
    Ou seja, a sua classificação não pode conter caracteres ou informações que exijam limpeza ou modificação do JSON.
    """

    if exemplos_positivos:
        prompt_base += f"\nTextos como '{'; '.join(exemplos_positivos)}' devem ser categorizados como POSITIVA."
    if exemplos_negativos:
        prompt_base += f"\nTextos como '{'; '.join(exemplos_negativos)}' devem ser categorizados como NEGATIVA."
    if exemplos_neutros:
        prompt_base += f"\nTextos como '{'; '.join(exemplos_neutros)}' devem ser categorizados como NEUTRA."

    prompt_final = f"{prompt_base}\n\nTexto para classificar: \"{texto}\"\n\nClassificação:"
    
    return prompt_final

def classificar(
    modelo_ia,
    texto: str,
    exemplos_positivos: list = None,
    exemplos_negativos: list = None,
    exemplos_neutros: list = None,
    emocoes: list = None
) -> (bool, dict | None):
    prompt_completo = get_prompt_para_classificacao(
        texto, exemplos_positivos, exemplos_negativos, exemplos_neutros, emocoes
    )

    sucesso, resposta_texto_ia = obter_resposta(modelo_ia, prompt_completo)
    
    classificacao = None
    if sucesso:
        try:
            resposta_limpa = resposta_texto_ia.replace("```json", "").replace("```", "").strip()
            classificacao = json.loads(resposta_limpa)
            sucesso = True
        except json.JSONDecodeError as e:
            print(f"ERRO: Resposta da IA não é um JSON válido: {e}")
            print(f"Resposta bruta da IA: {resposta_texto_ia}")
            sucesso = False
        except Exception as e:
            print(f"ERRO: Ocorreu um erro inesperado no processamento do JSON: {e}")
            sucesso = False

    return sucesso, classificacao

if __name__ == "__main__":
    print("Iniciando teste de classificação de sentimentos com Gemini...")

    sucesso_ia, modelo_ia_pronto = iniciar_IA() 

    if sucesso_ia:
        print("Acesso à IA iniciado, classificando um texto...")

        texto_exemplo = 'Hoje o dia vai ser bom! Estou muito animada com as novidades.'
        exemplos_pos = ['Você está bonita hoje', 'Que alegria te ver!', 'Amei o presente']
        exemplos_neg = ['Hoje é um péssimo dia', 'Detestei o filme', 'Que tristeza essa notícia']
        exemplos_neu = ['Hoje é 21 de Outubro', 'A parede é azul', 'O carro estacionou']
        emocoes_permitidas = ['alegria', 'tristeza', 'raiva', 'medo', 'nojo', 'desprezo', 'surpresa', 'expectativa']

        sucesso_classificacao, resultado_classificacao = classificar(
            modelo_ia_pronto,
            texto_exemplo,
            exemplos_positivos=exemplos_pos,
            exemplos_negativos=exemplos_neg,
            exemplos_neutros=exemplos_neu,
            emocoes=emocoes_permitidas
        )

        if sucesso_classificacao:
            print(f"\n--- Classificação do Texto: '{texto_exemplo}' ---")
            print(f"Polaridade: {resultado_classificacao.get('polaridade', 'Não encontrada')}")
            print(f"Emoção: {resultado_classificacao.get('emocao', 'Não encontrada')}")
            print("-------------------------------------------------")
        else:
            print("\nNão foi possível classificar o texto. Verifique as mensagens de erro.")
    else:
        print("\nFalha ao iniciar acesso à IA. Não foi possível realizar a classificação.")