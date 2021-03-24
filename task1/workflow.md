## Workflow - Task 1

Foi criado um arquivo chamado 'task1.py' que contém todo o código utilizado para fazer a curadoria do banco de dados. 

Primeiro criei uma função que processa o arquivo fasta de forma econômica e retorna tuplas com as sequências e as headers com os códigos.

Depois uso a biblioteca com a API do NCBI chamada Entrez contida no BioPython para procurar os códigos de nucleotídeos. Com a resposta da API eu consigo acessar os nomes associados a essa sequência e ver se esses nomes contem '16S'. Como eucariotos também possuem o gene pro RNA 16S, removo os que possuem algum conteúdo organelar, como 'mitochondrial' ou 'chloroplast'.

Mesmo que eles possuam 16S no nome e não tenham algum indício organelar, pode ser que a anotação fornecida pelo usuário que submeteu a sequência tenha sido feita de forma incorreta. Eu posso verificar isso acessando novamente a API com o TaxID associado ao código, só que isso acaba atrasando muuuuuito o processamento, porque a maneira como eu programei faz chamadas individuais. Para acelerar o processo eu poderia reunir todas as taxids que se adequam nessa categoria e faz uma chamada conjunta, assim como com os IDs das sequências. Entretanto, isso exigiria um tempo de dedicação maior a essa atividade que eu não possua, mas certamente é factível. 

Eu fiz um parâmetro para desativar/ativar essa verificação de TaxID e os resultados abaixo trazem a curação do banco de dados verificando se os nomes associados ao códigos possuem '16s' e não contem indícios de serem organelares.

Ao final da execução da limpeza, são exibidos resultados que resumem o processamento da informação e as sequências que passaram no filtro são escritas em um novo arquivo chamado 'filtered.fasta'.

![enter image description here](https://github.com/igrorp/desafio_neo/blob/main/task1/out.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbODkzMzkzODhdfQ==
-->