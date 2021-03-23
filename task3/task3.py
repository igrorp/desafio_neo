import pandas as pd

N_BAC = 50  # Definindo o número de bactérias mais abundantes a ser visualizado

table = pd.read_csv('arquivos-de-apoio/tables/otu_table_tax_amostras.tsv', delimiter='\t')

# Fazendo uns reajustes pra diminuir o nome das espécies e ocupar menos espaço no gráfico

temp = table['OTU'].str.split(' ', expand=True) # Separando o nome todo 

table['OTU'] = temp[0] + ' ' + temp[1].str.get(0) + '. ' + temp[2]  # Usando a abreviação de espécie pra S. cerevisiae por ex

# Essa solução não funcionaria se o arquivo contivesse espécies que não estão no formato dual gênero + espécie
# Teria que bolar outra solução se fosse o caso

del temp

table.set_index('OTU', inplace=True)    # Usando o nome das espécies como índices por enquanto

# No arquivos com os dados os indivíduos estão com "group_Sxxx" e como eu assumi que essa última part do "Sxxx" não é relevante, eu removi pra poder fazer
# o join entre os dataframes, já que os nomes tem que ser iguais

table.columns = table.columns.str.split('_').str.get(0)

# Transpondo a tabela para que eu possa acessar os indivíduos como linhas e cada espécie como coluna, permitindo a junção com a informação do metadado

table = table.transpose()

table.index.name = 'group'

soma = table.sum(axis=0) # Criei um objeto Series que contém a soma do número total de bactérias em todas as condições/indivíduos

# Agora que eu sei quantas bactérias de cada espécie existem, vou selecionar as 50 mais abundantes

fifty = soma.sort_values(ascending=False).head(N_BAC)

# Sabendo o nome das 50 espécies mais abundantes, vou selecionar os dados dessas espécies em cada condição/indivíduo da tabela original

table = table[[a for a in fifty.index]]

# Agora vou ler a informação do metadado pra saber qual a condição de tempo de cada indivíduo

info = pd.read_csv('arquivos-de-apoio/tables/metadata.csv', delimiter='\t')

info.set_index('group', inplace=True)

# Agora juntando as informações das duas tabelas usando a operação de join do pandas com base na chave de grupo

table = table.join(info, on='group')    # Agora essa tabela contém apenas os dados das 50 espécies mais abundantes e o metadado de cada ind associado

########################### Plotando as informações

import seaborn as sns   # Biblioteca que produz gráficos mais bonitinhos

import matplotlib.pyplot as plt

sns.set()

# Plotando o número absoluto de bactérias em cada indivíduo, mantendo as diferentes espécies de bactérias

table.drop('dpw', axis=1).plot(kind='bar', stacked=True, linewidth=0)

# Outra forma de plotar a mesma coisa
# sns.histplot(table.groupby('time').sum().reset_index(), x='time', multiple='stack')

plt.legend(bbox_to_anchor=(1,1), loc="upper left", fontsize=4)

plt.tight_layout()

plt.savefig('task3/stacked_absolute_ind.png', dpi=800)


# Criando um gráfico stacked mas dessa vez reunindo a informação do número absoluto de bactérias de acordo com o grupo de tempo late/early

# Agrupandos os indivíduos de acordo com a categoria a que pertencem (late/early)
# E logo depois somando a quantidade de bactérias de todos os indivíduos na mesma condição para analisar grupalmente

timegroup = table.groupby('time').sum()

timegroup.drop('dpw', axis=1, inplace=True)   # Removendo colunas indesejadas

timegroup.plot(kind='bar', stacked=True, linewidth=0)   # Plotando os dados

plt.legend(bbox_to_anchor=(1,1), loc="upper left", fontsize=4)  # Customizando as legendas

plt.tight_layout()

plt.savefig('task3/stacked_absolute_time.png', dpi=800)


# Criando o gráfico stacked mas agora de forma percentual e não absoluta

# Criando primeiro por indivíduo

indpercent = table.copy().drop(['dpw', 'time'], axis=1) # Copiando a tabela pra poder recalcular os valores e removendo colunas indesejadas

somaind = indpercent.sum(axis=1)    # Somando o número de bactérias de cada indivíduo pra poder fazer o percentual

for ind in somaind.index:   # Dividindo o número de bactérias de cada ind pelo total pra poder saber o percentual
    
    indpercent.loc[ind] = indpercent.loc[ind].divide(somaind[ind])

indpercent.plot(kind='bar', stacked=True, linewidth=0) # Plotando os dados em stacked barplot

plt.legend(bbox_to_anchor=(1,1), loc="upper left", fontsize=4)

plt.tight_layout()

plt.savefig('task3/stacked_percent_ind.png', dpi=800)


# Criando o gráfico stacked percentual mas por categoria de tempo e não por indivíduo

# Começo agrupando os dados com base na categoria de tempo e somando o número de bactérias de cada espécie em todos os indivíduos dessa categoria

somatempo = table.groupby('time').sum()

somatempo.drop('dpw', axis=1, inplace=True) # Removendo colunas indesejadas

somatotal = somatempo.sum(axis=1) # Calculando o total de bactérias em cada condição de tempo para poder calcular o percentual

# Essa parte abaixo poderia ser automatizada para receber valores arbitrários caso houvessem mais de duas categorias

somatempo.loc['Early'] = somatempo.loc['Early'].divide(somatotal['Early']) # Dividindo o número de bactérias em cada tempo pelo total para obter a porcentagem

somatempo.loc['Late'] = somatempo.loc['Late'].divide(somatotal['Late'])


somatempo.plot(kind='bar', stacked=True, linewidth=0) # Plotando os dados em stacked barplot

plt.legend(bbox_to_anchor=(1,1), loc="upper left", fontsize=4)

plt.tight_layout()

plt.savefig('task3/stacked_percent_time.png', dpi=800)