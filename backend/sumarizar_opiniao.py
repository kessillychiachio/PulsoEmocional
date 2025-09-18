import pandas as pd
from inicializacao_IA import iniciar_IA, obter_resposta
from langchain_core.messages import HumanMessage, SystemMessage

def preparar_dados_para_sumarizacao(df: pd.DataFrame) -> (int, int, int):
    contagem_polaridade = df['Polaridade'].value_counts().to_dict()
    positivos = contagem_polaridade.get('POSITIVO', 0)
    negativos = contagem_polaridade.get('NEGATIVO', 0)
    neutros = contagem_polaridade.get('NEUTRO', 0)
    
    return positivos, negativos, neutros

def criar_prompt_sumarizacao(
    positivos: int, 
    negativos: int, 
    neutros: int,
    comentarios_amostra: str
) -> (SystemMessage, HumanMessage):
    prompt_sistema_conteudo = f"""
    Você é um assistente especializado em analisar e resumir grandes volumes de feedback de usuários, como os comentários de um vídeo do YouTube.
    Sua tarefa é criar um resumo, em português, que pareça um comentário escrito por um membro da equipe de marketing da empresa do criador do vídeo, ponderando preocupaçōes, que seja baseado nos dados de análise de sentimento que eu fornecer.
    O resumo deve focar em identificar o assunto principal abordado nos comentários e relacionar o sentimento geral do vídeo a esse assunto.
    Apresente o resumo de forma fluida e em um único parágrafo, sem adicionar informações extras ou suposições, sem adicionar gírias.
    """

    prompt_humano_conteudo = f"""
    Dados da Análise de Sentimento:
    - Comentários Positivos: {positivos}
    - Comentários Negativos: {negativos}
    - Comentários Neutros: {neutros}
    
    Amostra dos comentários para contexto:
    {comentarios_amostra}

    Por favor, crie um resumo narrativo a partir desses dados e da amostra de comentários, focando no principal assunto discutido.
    """
    
    system_message = SystemMessage(content=prompt_sistema_conteudo.strip())
    human_message = HumanMessage(content=prompt_humano_conteudo.strip())

    return system_message, human_message

def gerar_sumario(df: pd.DataFrame) -> str | None:
    sucesso_ia, modelo_ia = iniciar_IA()

    if not sucesso_ia:
        print("Falha ao iniciar a IA. Não foi possível gerar o resumo.")
        return None

    positivos, negativos, neutros = preparar_dados_para_sumarizacao(df)
    comentarios_amostra = " ".join(df['Texto'].head(60).tolist())

    system_message, human_message = criar_prompt_sumarizacao(
        positivos, negativos, neutros, comentarios_amostra
    )

    sucesso, resposta_ia = obter_resposta(modelo_ia, [system_message, human_message])

    if sucesso:
        return resposta_ia.content
    else:
        print("Falha ao obter resposta da IA para sumarização.")
        return None

def main():
    try:
        df = pd.read_excel('resultados_da_ia.xlsx')
    except FileNotFoundError:
        print("Erro: O arquivo 'resultados_da_ia.xlsx' não foi encontrado.")
        print("Certifique-se de executar 'classificador_youtube.py' primeiro.")
        return

    if df.empty:
        print("A planilha de resultados está vazia. Não há nada para resumir.")
        return

    positivos, negativos, neutros = preparar_dados_para_sumarizacao(df)
    resumo = gerar_sumario(df)
    
    if resumo:
        print("\nResumo da Análise de Sentimentos")
        print(resumo)
        print ("\nForam analisados:")
        print(f"{positivos} comentários positivos, {negativos} negativos e {neutros} neutros.\n")

if __name__ == "__main__":
    main()