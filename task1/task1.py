

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

db = 'arquivos-de-apoio/fas/banco.fasta'

from Bio import Entrez

Entrez.email = 'fake@fake.com'

Entrez.max_tries = 5

Entrez.api_key = '9bc8c1d04425ea6757d6b8c7c46d7a904608'

counter, tem16, positive, error, mito, taxx, nottax = 0, 0, 0, 0, 0, 0, 0

EPOST_BATCH = 1000

info = {header:seq for header, seq in read_fasta(db)}

id_list = list(info.keys())

verifiyTaxID = False

print(f'Foram lidas {len(id_list)} sequências no arquivo {db}')


data = []

for start in range(0, len(id_list), EPOST_BATCH):

    end = start + EPOST_BATCH if start + EPOST_BATCH < len(id_list) else len(id_list)

    postreq = Entrez.epost(db="nucleotide", id=",".join(id_list[start:end]))

    search_res = Entrez.read(postreq)

    web_env = search_res["WebEnv"]

    query_key = search_res["QueryKey"]

    nuc_handle = Entrez.esummary(db='nucleotide', webenv=web_env, query_key=query_key)

    nuc_data = Entrez.read(nuc_handle)

    data += nuc_data


print(f'Foram extraídos {len(data)} resultados associados aos códigos informados')

with open('task1/filtered.fasta', 'w') as out:

    for record in data: # Iterando por cada entrada pra processar os dados de cada uma
        
        try:

            title = record['Title']  # Pegando o nome associado a essa entrada, pra ver se contem 16S nele

            code = record['AccessionVersion']

        except:

            print(f'''Found an error while processing code {code}''')

            error += 1

        counter += 1

        if '16S' in title.upper():  # Primeiro fazendo uma verificação muito básica se a string contem 16S, assumindo que todas as corretas possuem isso
            
            if 'mito' not in title.lower() and 'plast' not in title.lower():    # Pra que eu não verifique a taxonomia a toa, gastando tempo acessando a API, vou logo vendo se tem mitochondrial no nome pra eliminar 16S de eucariotos

                out.write(f'>{code}\n{info[code]}\n')

                positive += 1

                # Mesmo tendo 16S no nome e não ter mitocondrial no nome, pode ser que tenha sido mal anotado, portanto
                # Vou usar o taxid desse código pra verificar se é um procarioto mesmo, essa parte acaba sendo demorada porque novamente tô acessando a API, mas como não sei quão heterogêneas são essas entradas acabei optando por fazer isso
                # Caso o time achasse essa alternativa muito custosa em questão de tempo, poderíamos discutir outras opções

                if verifiyTaxID:

                    try:    # Criando uma cláusula de erro pra caso a informação que eu obtive com o código de acesso do NT não possuir taxid associado a ele
                                    
                        taxid = record['TaxId'].real

                    except KeyError:

                        error += 1

                        print(f'O dado retornado de {header} não contém TaxID associado portanto não foi possível discernir o domínio da espécie')

                    try:    # Novamente criando uma cláusula simples de captura de erro caso eu não consiga obter informação associada com o taxid ou comunicação com a API
                                    
                        taxhandle = Entrez.esummary(db='taxonomy', id=taxid, retmode="txt")

                        # handle = Entrez.efetch(db='taxonomy', id=str(a.real)) # Também poderia usar essa entrada aqui que é beeem mais detalhada e legal, só que leva um pouquinho mais de tempo e a outra parece cumprir o trabalho

                        record = Entrez.read(taxhandle)

                        div = record[0]['Division']

                        if 'bac' in div.lower():

                            positive += 1

                        else:

                            nottax += 1

                        taxx += 1

                    except:

                        taxhandle.close()

                        error += 1

                        print(f'Não foi possível obter informações sobre o taxid de {header}')

            else:   # Se não passsou no teste anterior quer dizer que é 16S organelar
                
                mito += 1

            tem16 += 1 




print(f'{positive} ({round(positive/counter*100, 2)}%) foram identificadas como sendo do gene 16s de procariotos')

print(f'Dessas:')

print(f'\t{tem16} ({round(tem16/counter*100, 2)}%) possum a palavra 16S no nome')

print(f'\t{mito} ({round(mito/counter*100, 2)}%) foram dos 16S foram removidos por determinar que são organelares')

print(f'{taxx} ({round(taxx/counter*100, 2)}%) chamadas foram feitas para determinar taxonomia')

print(f'\t{nottax} ({round(nottax/counter*100, 2)}%) entradas foram removidas por não ter taxonomia de bacteria')

print(f'{error} ({round(error/counter*100, 2)}%) erros foram encontrados na consulta dos bancos de dados')
