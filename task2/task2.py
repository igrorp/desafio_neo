
def read_fasta(filename):

    ''' Função bem simples que recebe o nome de um arquivo fasta e retorna um iterador que gera tuplas contendo a sequência e a header'''

    # Decidi usar um iterador ao invés de um .readlines() porque o iterador não carrega o arquivo inteiro na memória e seria mais econômico se trabalhássemos com um banco maior

    with open(filename) as file:

        begin = True

        for line in file:

            if line.startswith('>'):

                if not begin:

                    yield (header, sequence)

                header = line[1:-1]
                sequence = ''

            else:

                sequence += line[:-1]

            begin = False

db = 'task1/filtered.fasta' # O banco de dados curado na tarefa anterior

# Criando um dicionário cuja chave é a header e o valor é uma lista com a sequência e o tamanho dela

data = {
    header:[seq, len(seq)] for header, seq in read_fasta(db)
}

# Criando uma DF que possui os dados da header, da sequência, e de seu comprimento

import pandas as pd

data = pd.DataFrame.from_dict(data, orient='index', columns=['sequence', 'length'])

# Primeiro fazendo o histograma das frequências dos tamanhos das sequências em intervalos de 50 nt

import matplotlib.pyplot as plt 

import seaborn as sns

from matplotlib.cm import viridis

import numpy as np

sns.set()

plt.clf()

sns.histplot(data=data, x='length', stat='count', binwidth=50)  # Criando um histograma da frequência dos tamanhos das sequências, os intervalos de 50 nt

plt.tight_layout()

plt.savefig('task2/hist.png', dpi=800)  

# Agora fazendo o plot das taxonomias mais frequentes

# Estou assumindo que o arquivo a ser usado é 'tax_table_amostras.tsv', mas poderia extrair as TaxIDs a partir dos códigos do FASTA

taxs = 'arquivos-de-apoio/tables/tax_table_amostras.tsv'

taxs = pd.read_csv(taxs, delimiter='\t')


# Fazendo a seleção da informação a ser representada

group_by = 'Species' # Taxonomia a ser representada, pode ser qualquer uma presenta na tabela

grouped = taxs.groupby(group_by).count()    # Agrupando os dados da tabela que apresentam a mesma taxonomia selecionada e contando suas ocorrências

total = grouped['OTU'].sum()    # Vendo o total de ocorrências entre os possíveis valores pra poder calcular o percentual

keep = []   # Vai armazar as taxonomias mais frequentes que 1%

for gen in grouped.index:

    if grouped.loc[gen,'OTU'] / total >= 0.01:  # Verificando se a frequência dessa taxonomia é maior que 1%

        keep.append(gen)


plotdata = grouped.loc[keep,]   # Selecionando só os dados mais abundantes pra poder plotar

plt.clf()

plotdata = plotdata.sort_values(by='OTU', ascending=False)['OTU']   # Ordenando e selecionando os dados

colors = viridis(np.linspace(0,1,len(plotdata)))    # Criando uma paleta de cores pra usar em cada barra

plotdata.plot(kind='barh', linewidth=0, color=colors)   # Plotando os dados

plt.tick_params(axis='both', which='major',labelsize=5)

plt.tight_layout()

plt.savefig(f'task2/{group_by}_hist.png', dpi=800)
