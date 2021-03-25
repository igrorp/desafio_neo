# Workflow - Task 2

Para realizar essa tarefa me baseei bastante na biblioteca **Pandas** para lidar com a manipulação das tabelas e com a biblioteca **Seaborn** para produção dos gráfico e customização.

O arquivo fasta do banco de dados curado automaticamente foi lido pela mesma função criada na tarefa anterior e logo em seguida foi criado um **DataFrame** que contivesse as informações presentes na header, a própria sequência e seu tamanho. O histograma pode ser observado abaixo, com intervalos de 50 nt entre cada barra:

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task2/hist.png)

E agora com intervalos de 10 nt entre cada barra podemos notar melhor que a maioria das sequências apresenta em torno de 800 nucleotídeos, além de termos sequências bem pequenas que provavelmente deveriam ser filtradas do banco de dados também.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task2/hist_10.png)

Para produzir uma visulização das **taxonomias** presentes no banco de dados, eu me baseei no arquivo CSV fornecido, embora pudesse também obter os TaxIDs associados com as sequências do fasta por meio do Entrez. A informação é lida e transformada para um CSV, onde posso agrupar as ocorrência de cada taxonomia em grupo e calcular a frequência com que ocorrem, determinando se são mais abundantes de 1%. Selecionando apenas essa informação, posso representá-la na forma de gráficos de barras.

O script foi programada de modo que pudesse aceitar qualquer categoria de taxonomia presenta na tabela, como classe, família, gênero, espécie, etc. Abaixo podemos ver o histograma das espécies mais representadas no banco de dados.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task2/Species_hist.png)

Podemos analisar também os gêneros mais frequentes no nosso banco de dados.
<img src="https://github.com/igrorp/desafio_neo/blob/main/task2/Genus_hist.png", height=50% />
![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task2/Genus_hist.png)

Ou também analisar as famílias de bactérias mais abundantes no dataset. Por algum motivo tem dados que parecem estar errados e associados com 'mitochondria' como família, certamente o banco teria quer ser revisado.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task2/Family_hist.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE3OTM5NDk2NjhdfQ==
-->