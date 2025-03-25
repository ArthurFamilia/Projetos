
import pandas as pd
import talib
import json

# Substitua 'caminho_do_arquivo.csv' pelo caminho do seu arquivo CSV
caminho_do_arquivo = "C:/Projetos/USDJPYDaily.csv"

# Configurações do mercado futuro
contract_size = 1000  # Tamanho do contrato (exemplo: 1000 unidades)
tick_value = 0.01     # Valor de cada ponto (exemplo: 0.01 por ponto)

# Lê o arquivo CSV
df = pd.read_csv(caminho_do_arquivo)

# Converte a coluna de data para datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filtra os anos de 2015 a 2025
df_filtered = df[(df['Date'].dt.year >= 2015) & (df['Date'].dt.year <= 2025)]

# Calcula o índice direcional médio de 14 períodos (ADX)
df_filtered['ADX'] = talib.ADX(df_filtered['High'], df_filtered['Low'], df_filtered['Close'], timeperiod=14)

# Calcula DI+ e DI-
df_filtered['DI+'] = talib.PLUS_DI(df_filtered['High'], df_filtered['Low'], df_filtered['Close'], timeperiod=14)
df_filtered['DI-'] = talib.MINUS_DI(df_filtered['High'], df_filtered['Low'], df_filtered['Close'], timeperiod=14)

# Determina o tipo de operação (compra ou venda)
df_filtered['Operation'] = df_filtered.apply(lambda row: 'Compra' if row['DI+'] > row['DI-'] else 'Venda', axis=1)

# Calcula o True Range (TR) de 10 períodos
df_filtered['TR'] = talib.ATR(df_filtered['High'], df_filtered['Low'], df_filtered['Close'], timeperiod=10)

# Inicializa uma lista para armazenar os resultados das operações
operations = []

# Itera sobre as linhas do DataFrame para verificar condições de operação
for index, row in df_filtered.iterrows():
    if row['ADX'] > 30:  # Verifica se o ADX é maior que 30
        # Define os valores de Stop e Gain com base no tipo de operação
        if row['Operation'] == 'Compra':
            stop = row['Close'] - 1.5 * row['TR']
            gain = row['Close'] + 4 * row['TR']
        elif row['Operation'] == 'Venda':
            stop = row['Close'] + 1.5 * row['TR']
            gain = row['Close'] - 4 * row['TR']

        # Cria a operação
        operation = {
            "Date": row['Date'],
            "Type": row['Operation'],
            "EntryPrice": row['Close'],
            "Stop": stop,
            "Gain": gain,
            "Result": None,  # Inicializa o resultado como None
            "Profit/Loss": None  # Inicializa o lucro/prejuízo como None
        }

        # Simula o preço atingindo o Gain ou o Stop
        # Substitua esta parte com dados reais de preços em tempo real, se disponível
        simulated_prices = [row['Close'], gain, stop]  # Verifica o Gain antes do Stop
        for price in simulated_prices:
            if row['Operation'] == 'Compra' and price >= gain:
                operation['Result'] = 'Gain'
                operation['Profit/Loss'] = (gain - row['Close']) * contract_size * tick_value
                break
            elif row['Operation'] == 'Compra' and price <= stop:
                operation['Result'] = 'Stop'
                operation['Profit/Loss'] = (stop - row['Close']) * contract_size * tick_value
                break
            elif row['Operation'] == 'Venda' and price <= gain:
                operation['Result'] = 'Gain'
                operation['Profit/Loss'] = (row['Close'] - gain) * contract_size * tick_value
                break
            elif row['Operation'] == 'Venda' and price >= stop:
                operation['Result'] = 'Stop'
                operation['Profit/Loss'] = (row['Close'] - stop) * contract_size * tick_value
                break

        # Adiciona a operação à lista
        operations.append(operation)

# Salva os resultados das operações em um arquivo JSON
with open("operations_result.json", "w") as json_file:
    json.dump(operations, json_file, indent=4, default=str)

# Exibe o resultado das operações
print(operations)