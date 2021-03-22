# Workflow - Tarefa 4

Utilizei os arquivos FQ fornecidos para demonstrar o fluxo de trabalho que geralmente utilizo para lidar com limpeza de qualidade de NGS.

Explicando as pastas criadas nessa tarefa:

 1. **raw/** contém os arquivos gerados pelo FASTQ com os dados originais fornecidos
 2. **multiqc_raw/** contém os arquivos gerados pelo MultiQC com os dados originais fornecidos
 3. **cleaning/** contém os arquivos gerados pelo FASTQ com os dados após o controle de qualidade e remoção dos adaptadores
 4. **multiqc_cleaning/** contém os arquivos gerados pelo MultiQC comparando as informações

## Cálculo de métricas de qualidade

Começando de maneira bem simples e prática, utilizo as ferramentas de análise do [FASTQC](bioinformatics.babraham.ac.uk/projects/fastqc/). Ele me permite ter acesso a uma boa variedade de estatísticas dos arquivos de sequenciamento e é bem padrão dentro da bioinformática, portanto sigo utilizando-o inicialmente. Rodei usando:

    fastqc -t 8 arquivos-de-apoio/fqs/*.fastq -o task4/raw/

Uma informação relevante, estou assumindo que os dados são single-end. Por causa de:

 - As headers de reads em arquivos FASTQ sequenciados em paired-end geralmente apresentam **"1:xxxx..."** e **"2:xxxx..."**, mas não encontrei esse padrão
 - O nome dos arquivos FASTQ informados não apresenta **"R2"** ou alguma
    compatibilidade que indique ligação.

Não que a informação da tecnologia de sequenciamento seja essencial nessa etapa, mas programas de controle de qualidade muitas vezes precisam dessa informação para remover os reads que falhem no controle de qualidade de ambos os arquivos paired-end, por exemplo, para que não tenhamos reads sem par.

Logo em seguida rodei o software [MultiQC](https://multiqc.info/), que basicamente reúne as estatísticas calculadas pelo FASTQC sobre vários arquivos FASTQ e coloca todas essas informações em conjunto para facilitar a análise e visualização múltipla. Uma das melhores e mais completas ferramentas que eu já utilizei na bioinformática, que vai bem além do que só essa função.

    multiqc task4/raw/ -o task4/multiqc_raw/

O programa gera um relatório dentro de uma página HTML que contém vários gráficos facilmente customizáveis e bem informativos, facilitando a comparação entre as diferentes amostras.

O arquivo pode ser acessado em "task4/multiqc_raw/multiqc_report.html".

## Análise interpretativa das bibliotecas

Em suma, as bibliotecas apresentam uma boa qualidade em termos de **PHRED score médio** (em torno de 35), com o gráfico do score ao longo da posição do read indicando qualidades superiores a 30, exceto nos últimos nucleotídeos, ou seja, temos grande confiança (maior que 99,9%) na atribuição das sequências desses erros.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task4/multiqc_raw/fastqc_per_base_sequence_quality_plot.png)

Os **níveis de duplicação** são altos, mas acho que isso não apresenta um problema porque provavelmente são consequência dos primers utilizados e da condução do PCR
anterior ao sequenciamento. Desde não seja uma contaminação (o que o FASTQC não está indicando) e a cobertura seja suficiente para representar o gene/genoma/transcritos desejados, a remoção dessas duplicações é tranquila e realizada durante os passos de alinhamento ou montagem. 

A distribuição das **porcentagens de nucleotídeos** nas sequências dos reads foi bem irregular (na verdade nunca vi uma distribuição tão estranha), mas acredito que isso se deve a presença de adaptadores ou deve ser um artefato vindo do corte que foi feito nos FASTQ para diminuir seu tamanho.
![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task4/multiqc_raw/chart.png)

A **distribuição GC** dos reads também destoa da esperada distribuição normal, apesar de que se a amostra sequenciada for de uma comunidade de microorganismos, é esperado que se tenha uma diversidade bem grande de conteúdos GC, já que essa característica é bem espécie-específica. Também já encontrei padrões bem estranhos de conteúdos GC em amostras que analisei em outros projetos, mesmo sendo da mesma espécie e não apresenta sinais de contaminação.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task4/multiqc_raw/fastqc_per_sequence_gc_content_plot.png)

A **distribuição de tamanho** dos reads gira em torno de 248-252 e aparentemente não foram identificados adaptadores.

Algumas das estatísticas também podem ter sido influenciadas porque os FASTQ são apenas porções do que seriam de fato, para vias de facilitar a nossa análise e processamento dos dados

## Limpeza das bibliotecas

Após a verificação da qualidade inicial dos arquivos, vou partir para a limpeza deles, eliminando reads com qualidades ruins e cortando possíveis sequências de adaptadores presentes.

Para realizar essa tarefa eu gosto de usar o programa [Trim Galore!](https://github.com/FelixKrueger/TrimGalore/blob/master/Docs/Trim_Galore_User_Guide.md) .  Essencialmente ele é um "wrapper" de um outro software chamado CutAdapt, que faz a eliminação de sequências de adaptadores. As vantagens dele são, principalmente, que possui um algoritmo que **automaticamente** identifica qual o tipo de adaptador (illumina, sanger, de pequenos RNAs, etc) presente nos reads e passa a eliminá-lo, além de integrar o FASTQC na análise e rodá-lo após a limpeza dos dados ter sido realizada. Também tem uma boa coleção de parâmetros costumizáveis e aceita multithreading, assim como a maioria dos outros software da categoria.

Para rodá-lo, usei:

    trim_galore -max_n 10 -q 30 --cores 8 --trim-n --fastqc --gzip --length 50

 - **max_n** remove reads que tenham mais que 10 letras N (bases não determinadas)
 - **q** especifica o score Phred de corte usado para controle de qualidade, o valor de 30 é bem utilizado e evidencia uma confiança de 99,9% nos nucelotídeos do read que foi sequenciado
 - **--trim-n** faz com que as letras N nas extremidades dos reads sejam removidas
 - **--length** faz com que reads com menos de 50 nucleotídos de tamanho sejam removidos, já que provavelmente não seriam tão informativos assim
 - **gzip** comprime os arquivos de saída para que ocupem menos espaço no disco
 - **fastqc** já roda o cálculo das métricas  geração das imagens 

## Análise interpretativa da limpeza

 Novamente rodei o MultiQC nos arquivos de saída do FASTQC das bibliotecas agora limpas e podemos notar que ouve uma leve melhora nos parâmetros gerais, com uma diminuição significativa dos desvio dos valores de PHRED em algumas posiçõe mais finais do read, o que é bem comum.

![End read quality improvement](https://github.com/igrorp/desafio_neo/blob/main/task4/multiqc_cleaning/Screenshot%202021-03-22%20153746.png)

De maneira geral as bibliotecas agora estão numa qualidade melhor e poucos reads (em torno de 5% nas bibliotecas) de fato foram removidos por não se adequarem os critérios, como consta nos relatórios fornecidos pelo FASTQC, o que indica que aparentemente esse sequenciamento foi bem sucedido. 

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task4/multiqc_cleaning/fastqc_per_base_sequence_quality_plot%20%281%29.png)

Outra coisa que eu teria realizado na limpeza seria a remoção dos primeiros oito nucleotídeos dos reads, que, como demonstrado na imagem abaixo, são sequências quase que consenso e poderiam atrapalhar futuras análises. Como não tenho certeza da procedência das bilbiotecas e isso talvez seja algum artefato ou mesmo uma sequência adaptadora, decidi omitir essa parte da análise e provavelmente buscaria consulta com colegas em um situação real de trabalho.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task4/multiqc_cleaning/Screenshot%202021-03-22%20144550.png)

Com esse filtros de qualidade, agora as biblioteca podem ser utilizadas com mais confiança e reprodutibilidade, garantindo um desempenho melhor e agregando valor ao trabalho da empresa.

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTczMzI4Nzk3NV19
-->