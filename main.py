from numpy import int64
import pandas as pd
import matplotlib.pyplot as plt

wc_champions = pd.read_csv('wc_champions.csv')

# wc_champions.head()
# wc_champions.tail()
# wc_champions.shape
# wc_champions.info()
# wc_champions.describe()
# wc_champions.columns
# wc_champions.dtypes
# print(wc_champions.isna().any())

# ATENÇÃO: meu database não tem nenhum campo que seja NaN/null. Por conta disso, vou substituir onde há hifens por NaN.


#Substitua os hífens existentes no database por NaN.
wc_champions.replace('-', 'NaN', inplace=True)
print(wc_champions['winrate_blue_side'])
print("###########################")

# Apagando as linhas de champions que não possuem vitórias (DROPNA - não funcionou aqui no Replit, somente no Notebook - ipynb)
wc_champions['win_total'].dropna(axis=0)
print(wc_champions['winrate_blue_side'])
print(wc_champions['win_total'])
print("###########################")

# Dropando as linhas de campeões que foram escolhidos menos que 5 vezes (DROP)
wc_champions.drop(wc_champions[wc_champions['win_total'] < 5].index, inplace=True)
print(wc_champions['winrate_blue_side'])
print(wc_champions['win_total'])
print("###########################")

# Traduza para português o nome das colunas (RENAME)

novo_nome_colunas = {
    'champion': 'campeão',
    'sum_total': 'total_soma',
    'win_total': 'total_vitórias',
    'lose_total': 'total_derrotas',
    'winrate_total': 'taxa_vitórias_total',
    'pick_rate': 'taxa_escolha',
    'sum_blue_side': 'total_lado_azul',
    'win_blue_side': 'vitórias_lado_azul',
    'lose_blue_side': 'derrotas_lado_azul',
    'winrate_blue_side': 'taxa_vitórias_lado_azul',
    'sum_red_side': 'total_lado_vermelho',
    'win_red_side': 'vitórias_lado_vermelho',
    'lose_red_side': 'derrotas_lado_vermelho',
    'winrate_red_side': 'taxa_vitórias_lado_vermelho',
    'sum_bans': 'total_bans',
    'ban_rate': 'taxa_banimento',
    'sum_pick_ban': 'total_escolha_banimento',
    'pick_ban_rate': 'taxa_escolha_banimento'
}

wc_champions = wc_champions.rename(columns=novo_nome_colunas)
print(wc_champions)
print("###########################")

# Criando nova coluna que conta quantas letras tem o nome de cada campeão (APPLY)
wc_champions['quantidade_letras'] = wc_champions['campeão'].apply(lambda x: len(x))
print(wc_champions)
print("###########################")

# MANIPULAÇÕES ARITMÉTICAS

# Quantos jogos tiveram no total?
total_de_partidas = wc_champions['total_soma'].sum()
print(f'O total de partidas que consta na database é de: {total_de_partidas}')
print("###########################")

# Calcular a proporção de vitórias para derrotas por campeão

wc_champions['vitórias_vs_derrotas'] = wc_champions['total_vitórias'] / wc_champions['total_derrotas']
print(wc_champions[['campeão', 'total_vitórias', 'total_derrotas', 'vitórias_vs_derrotas']])
print("###########################")

#Qual a média de vitória e desvio padrão para cada lado?

wc_champions['taxa_vitórias_lado_azul'] = wc_champions['taxa_vitórias_lado_azul'].str.rstrip('%').str.replace(',', '.').astype(float)
wc_champions['taxa_vitórias_lado_vermelho'] = wc_champions['taxa_vitórias_lado_vermelho'].str.rstrip('%').str.replace(',', '.').astype(float)

media_vitoria_azul = wc_champions['taxa_vitórias_lado_azul'].mean()
media_vitoria_vermelho = wc_champions['taxa_vitórias_lado_vermelho'].mean()
desvio_padrao_azul = wc_champions['taxa_vitórias_lado_azul'].std()
desvio_padrao_vermelho = wc_champions['taxa_vitórias_lado_vermelho'].std()

print("Qual a média de vitória e desvio padrão para cada lado?")
print(f"Média de vitória do lado azul: {media_vitoria_azul:.2f}%")
print(f"Média de vitória do lado vermelho: {media_vitoria_vermelho:.2f}%")
print(f"Desvio padrão do lado azul: {desvio_padrao_azul:.2f}")
print(f"Desvio padrão do lado vermelho: {desvio_padrao_vermelho:.2f}")
print("###########################")

# Qual a popularidade de cada campeão?
wc_champions['popularidade'] = wc_champions['total_bans'] / wc_champions['total_soma']
print(wc_champions[['campeão', 'popularidade']])
print("###########################")

#Calcule a média das estatísticas de cada campeão
wc_champions['média_estatísticas'] = wc_champions[['total_soma', 'total_vitórias', 'total_derrotas', 'taxa_vitórias_total']].mean(axis=1)
print(wc_champions[['campeão', 'média_estatísticas']])
print("###########################")

# Quais os campeões mais banidos por ordem decrescente? (GROUPBY)
wc_champions['taxa_banimento'] = wc_champions['taxa_banimento'].str.rstrip('%').astype(float)

campeoes_mais_banidos = wc_champions.groupby('campeão')['taxa_banimento'].max()

campeoes_mais_banidos = campeoes_mais_banidos.sort_values(ascending=False)

print(campeoes_mais_banidos)
print("###########################")

# Exporte a lista de campeões mais banidos para um novo CSV
campeoes_mais_banidos.to_csv('campeoes_mais_banidos.csv')

### GRÁFICO

## USANDO MPL

# df = wc_champions[['campeão', 'vitórias_lado_azul', 'vitórias_lado_vermelho']]
# df = df.copy()

# df['total_vitórias'] = df['vitórias_lado_azul'] + df['vitórias_lado_vermelho']
# df = df.sort_values(by='total_vitórias', ascending=False)
# fig, ax = plt.subplots(figsize=(12, 6))
# ax.bar(df['campeão'], df['vitórias_lado_azul'], label='Vitórias Lado Azul', color='tab:blue')
# ax.bar(df['campeão'], df['vitórias_lado_vermelho'], bottom=df['vitórias_lado_azul'], label='Vitórias Lado Vermelho', color='tab:red')
# ax.set_xlabel('Campeão')
# ax.set_ylabel('Total de Vitórias')
# ax.set_title('Total de Vitórias por Campeão (Lado Azul vs. Lado Vermelho)')
# plt.xticks(rotation=90)
# plt.legend()
# plt.tight_layout()
# plt.show()


### USANDO PD.QCUT

df = wc_champions[['campeão', 'vitórias_lado_azul', 'vitórias_lado_vermelho']].copy()
df['total_vitórias'] = df['vitórias_lado_azul'] + df['vitórias_lado_vermelho']

num_bins = 5  # Número de intervalos desejados
df['total_vitórias_interval'] = pd.qcut(df['total_vitórias'], num_bins)

df = df.sort_values(by='total_vitórias_interval')

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df['campeão'], df['vitórias_lado_azul'], label='Vitórias Lado Azul', color='tab:blue')
ax.bar(df['campeão'], df['vitórias_lado_vermelho'], bottom=df['vitórias_lado_azul'], label='Vitórias Lado Vermelho', color='tab:red')

ax.set_xlabel('Campeão')
ax.set_ylabel('Total de Vitórias')
ax.set_title('Total de Vitórias por Campeão (Lado Azul vs. Lado Vermelho)')
plt.xticks(rotation=90)
plt.legend()

plt.tight_layout()
plt.show()


####










