import pandas as pd
import sqlite3
import os

PLANILHA = "classificacoes/imdb-reviews-pt-br.xlsx"
BANCO_DE_DADOS = "sentimentos.sqlite"

def iniciar_planilha():
    sucesso, planilha = False, None

    try:
        planilha = pd.read_excel(PLANILHA, header=0)

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro ao ler a planilha: {str(e)}")

    return sucesso, planilha

def iniciar_banco():
    sucesso, banco = False, None

    try:
        if os.path.exists(BANCO_DE_DADOS):
            os.remove(BANCO_DE_DADOS)

        conexao = sqlite3.connect(BANCO_DE_DADOS)
        cursor = conexao.cursor()

        cursor.execute("DROP TABLE IF EXISTS classificacao")
        cursor.execute("CREATE TABLE classificacao(texto TEXT, polaridade TEXT, emocao TEXT)")

        conexao.close()

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro ao criar o banco de dados: {str(e)}")

    return sucesso, banco

def gravar_classificacao(texto, polaridade, emocao):
    sucesso = False

    try:
        conexao = sqlite3.connect(BANCO_DE_DADOS)
        cursor = conexao.cursor()

        cursor.execute(f"INSERT INTO classificacao(texto, polaridade, emocao) VALUES ('{texto}', '{polaridade}', '{emocao}')")

        conexao.commit()
        conexao.close()

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro gravando classificação no banco de dados: {str(e)}")

    return sucesso

if __name__ == "__main__":
    sucesso, planilha = iniciar_planilha()
    if sucesso:
        sucesso, banco = iniciar_banco()
        if sucesso:
            contador = 0

            for contador, row in planilha.iterrows():
                texto = row['text_pt'].strip().lower().replace("'", "")
                polaridade = 'NEGATIVA' if row['sentiment'] == "neg" else "POSITIVA"

                gravar_classificacao(texto, polaridade, "")

            print(f"foram gravadas {contador} classificações")
