import json

# Função para ler o arquivo JSON e contar gains e losses
def contar_gains_losses(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        
        gains = dados.get('gains', [])
        losses = dados.get('losses', [])
        
        total_gains = len(gains)
        total_losses = len(losses)
        
        print(f"Total de Gains: {total_gains}")
        print(f"Total de Losses: {total_losses}")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")

# Caminho do arquivo JSON
caminho_arquivo = "C:\Projetos\operacoes.json"

# Chamada da função
contar_gains_losses(caminho_arquivo)