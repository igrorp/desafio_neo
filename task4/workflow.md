Descrição dos passos tomados para a limpeza dos dados contidos nos arquivos FASTQ

Começando de maneira bem simples e prática, aplicando as ferramentas de análise do FASTQC.

fastqc -t 8 arquivos-de-apoio/fqs/*.fastq -o task4/raw/

Outra informação importante, estou assumindo que os dados são single-end. Por causa de:
1) A header de arquivos FASTQ sequenciados em paired-end geralmente apresenta "1:xxxx..." e "2:xxxx...", mas não encontrei esse padrão
2) O nome dos arquivos FASTQ informados não apresenta "R2" ou alguma compatibilidade que indique ligação

Não que a informação da tecnologia de sequenciamento seja essencial nessa etapa, mas programas de controle de qualidade muitas vezes precisam dessa informação para remover os reads que falhem no controle de qualidade de ambos os arquivos paire-end, por exemplo, para que não tenhamos reads sem par.

Logo em seguida rodei o software MultiQC, que basicamente reune as estatísticas calculadas pelo FASTQC sobre vários arquivos
FASTQ e coloca todas essas informações em conjunto para facilitar a análise e visualização múltipla.

multiqc task4/raw/ -o task4/multiqc_raw/

O programa gera um relatório dentro de uma página HTML que contém vários gráficos facilmente customizáveis e bem informativos,
facilitando a comparação entre as diferentes amostras.

O arquivo pode ser acessado em "task4/multiqc_raw/multiqc_report.html".

Em suma, as bibliotecas apresentam uma boa qualidade em termos de PHRED score médio (em torno de 35), com o gráfico do score ao longo da posição do read indicando
qualidades superiores a 30, exceto nos últimos nucleotídeos, ou seja, temos grande confiança na atribuição dos nucleotídeos dessas sequências.

Os níveis de duplicação são altos, mas acho que isso não apresenta um problema porque provavelmente são consequência dos primers utilizados e da condução do PCR
anterior ao sequenciamento, e desde não seja uma contaminação e a cobertura seja suficiente para representar o gene/genoma/transcritos desejados, a remoção dessas duplicações é tranquila.

A distribuição GC dos reads também destoa da esperada distribuição normal, apesar de que se a amostra sequenciada for de uma comunidade de microorganismos, é esperado que se tenha uma diversidade bem grande
de conteúdos GC, já que essa característica é bem espécie-específica. Também já encontrei padrões bem estranhos de conteúdos GC em amostras que analisei em outros projetos.

A distribuição de tamanho dos reads gira em torno de 248-252 e aparentemente não foram identificados adaptadores.

Algumas das estatísticas também podem ter sido influenciadas porque os FASTQ são apenas porções do que seriam de fato, para vias de facilitar a nossa análise e processamento dos dados

### 

Após a verificação da qualidade inicial dos arquivos, vou partir para a limpeza deles, eliminando reads com qualidades ruins
e eliminando possíveis sequências de adaptadores presentes.

Para realizar essa tarefa eu gosto de usar o programa Trim Galore! (https://github.com/FelixKrueger/TrimGalore/blob/master/Docs/Trim_Galore_User_Guide.md). 
Essencialmente ele é um programa que é um "wrapper" de um outro software chamado CutAdapt, que faz a eliminação de sequências de adaptadores. As vantagens 
dele são, principalmente, que possui um algoritmo que automaticamente identifica qual o tipo de adaptador presentes nos reads e passa a eliminá-lo, além
de integrar o FASTQC na análise e rodá-lo após a limpeza dos dados ter sido realizada. Também tem uma boa coleção de parâmetros costumizáveis e aceita multithreading,
assim como a maioria dos outros software da categoria.

Para rodá-lo, usei:

