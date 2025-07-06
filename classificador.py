from inicializacao_IA import *
import json

def get_contexto(exemplificar_polaridades = True):
    contexto = [
        ("system", "Você é um assistente especializado em avaliar sentimentalmente trechos de texto"),
        ("system", "Você deve categorizar os textos em três polaridades: NEGATIVA, POSITIVA e NEUTRA"),
        ("system", "Você também deve determinar qual o tipo de emoção do texto"),
        ("system", "Limite-se a avaliar a emoção nas seguintes categorias: {emocoes}"),
        ("system", "A sua classificacao deve ser um estrutura JSON contendo: a polaridade associado ao atributo 'polaridade' e a emoção associada ao atributo 'emocao"),
        ("system", "A sua classificacao deve ser conter somente o conteúdo do JSON e nada mais"),
        ("system", "Ou seja, a sua classificacao não pode conter caracteres ou informações que exijam limpeza ou modificação do JSON"),

        ("human", "{texto}")
    ]

    if exemplificar_polaridades:
        contexto.append(("system", "Textos como {positivos} deve ser categorizado como POSITIVA"))
        contexto.append(("system", "Textos como {negativos} deve ser categorizado como NEGATIVA"))
        contexto.append(("system", "Textos como {neutros} deve ser categorizado como NEUTRA"))

    return contexto

def classificar(IA, texto, exemplos_positivos = [], exemplos_negativos = [], exemplos_neutros = [], emocoes = ['alegria', 'tristeza', 'raiva', 'medo', 'nojo', 'desprezo', 'surpresa']):
    sucesso, classificacao = obter_resposta(IA, {"positivos": exemplos_positivos, "negativos": exemplos_negativos, "neutros": exemplos_neutros, "emocoes": emocoes, "texto": texto})
    
    if sucesso:
        classificacao = classificacao.text()
        classificacao = classificacao.replace("```json", "")
        classificacao = classificacao.replace("```", "")

        classificacao = json.loads(classificacao)

    return sucesso, classificacao

if __name__ == "__main__":
    sucesso, IA = iniciar_IA(get_contexto())
    if sucesso:
        print("acesso à IA iniciado, classificando um texto...")

        texto = 'hoje o dia vai ser bom'
        sucesso, classificacao = classificar(IA, texto, ['você está bonita hoje'], ['hoje é um péssimo dia'], ['hoje é 21 de Outubro'], ['alegria', 'tristeza', 'raiva', 'medo', 'nojo', 'desprezo', 'surpresa'])

        if sucesso:
            print(f"classificação do texto '{texto}': {classificacao}")