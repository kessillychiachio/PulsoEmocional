import pandas as pd
import os

def _carregar_base():
    try:
        return pd.read_excel('resultados_da_ia.xlsx')
    except FileNotFoundError:
        try:
            return pd.read_csv('resultados_da_ia.csv')
        except FileNotFoundError:
            print("Erro: Nenhum arquivo de resultados encontrado ('resultados_da_ia.xlsx' ou 'resultados_da_ia.csv').")
            print("Gere os resultados primeiro executando: python classificador_youtube.py --video-id SEU_ID")
            return None

def preparar_planilhas_para_avaliacao():
    df_base = _carregar_base()
    if df_base is None:
        return

    if 'Texto' not in df_base.columns:
        if 'Mensagem Coletada' in df_base.columns:
            df_base['Texto'] = df_base['Mensagem Coletada']
        else:
            print("Erro: A coluna 'Texto' não foi encontrada na base de resultados.")
            print("Verifique se a planilha contém a coluna 'Texto' ou 'Mensagem Coletada'.")
            return

    df_para_avaliadores = df_base[['Texto']].copy()
    df_para_avaliadores.drop_duplicates(inplace=True)
    df_para_avaliadores.reset_index(drop=True, inplace=True)

    df_danilo = df_para_avaliadores.copy()
    df_danilo['Avaliação Humana (Danilo)'] = ''
    nome_arquivo_danilo = 'avaliacoes_danilo.xlsx'
    try:
        df_danilo.to_excel(nome_arquivo_danilo, index=False, engine='openpyxl')
    except ImportError:
        nome_arquivo_danilo = 'avaliacoes_danilo.csv'
        df_danilo.to_csv(nome_arquivo_danilo, index=False, encoding='utf-8')
    print(f"Planilha '{nome_arquivo_danilo}' criada com sucesso para Danilo!")

    df_melkes = df_para_avaliadores.copy()
    df_melkes['Avaliação Humana (Melkes)'] = ''
    nome_arquivo_melkes = 'avaliacoes_melkes.xlsx'
    try:
        df_melkes.to_excel(nome_arquivo_melkes, index=False, engine='openpyxl')
    except ImportError:
        nome_arquivo_melkes = 'avaliacoes_melkes.csv'
        df_melkes.to_csv(nome_arquivo_melkes, index=False, encoding='utf-8')
    print(f"Planilha '{nome_arquivo_melkes}' criada com sucesso para Melkes!")

    print("\nInstruções: Envie as planilhas para cada avaliador. Após o preenchimento, use o script 'coeficiente_kappa.py'.")

if __name__ == "__main__":
    preparar_planilhas_para_avaliacao()
