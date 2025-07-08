import os
from googleapiclient.discovery import build

YOUTUBE_API_KEY_FILE = "keys/youtube_api.key"

def carregar_chave_api(caminho_arquivo: str) -> str:
  try:
    with open(caminho_arquivo, "r") as arquivo:
      chave = arquivo.read().strip()
      if not chave:
        raise ValueError("O arquivo da chave {caminho_arquivo} está vazio.")
      return chave
  except FileNotFoundError:
    raise FileNotFoundError(f"Arquivo de chave não encontrado: {caminho_arquivo}")
  except Exception as e:
    raise Exception(f"Erro ao carregar a chave da API: {str(e)}")
  
def obter_servico_youtube(api_key: str):
  try:
    api_key = carregar_chave_api(YOUTUBE_API_KEY_FILE)
    youtube_service = build('youtube', 'v3', developerKey=api_key)
    
    print("Serviço do YouTube Data API carregado com sucesso.")
    return True, youtube_service
  except Exception as e:
    print(f"Erro ao carregar o serviço do YouTube inicializado com sucesso.")
      