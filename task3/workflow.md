---


---

<h1 id="workflow---task-4">Workflow - Task 4</h1>
<p>Para reprentar adequadamente o que foi solicitado, utilizei a biblioteca Pandas para criar uma estrutura de contivesse as informações das frequências das bactérias em cada indivíduo e em cada condição, além de fazer as operações de junções entre as tabelas. Também utilizei as bibliotecas Matplotlib e Seaborn para produzir gráficos mais esteticamente agradáveis.</p>
<p>Todo o código utilizado para representar as imagens está comentado e se localiza no repositório junto a este arquivo, com o nome de ‘<a href="http://task3.py">task3.py</a>’.</p>
<p>O gráfico solicitado contendo a contagem absoluta das 50 bactérias mais abudantes de acordo com o tempo segue abaixo:</p>
<p><img src="https://github.com/igrorp/desafio_neo/blob/main/task3/stacked_absolute_time.png" alt="enter image description here"></p>
<p>A legenda da imagem está ordenada para representar a espécie mais frequente em cima e desce a medida que vai ficando menos abundante.</p>
<p>Também poderíamos representar a informação absoluta das contagem, mas em função de cada indivíduo, para compreendermos a diversidade dentro do grupo:</p>
<p><img src="https://github.com/igrorp/desafio_neo/blob/main/task3/stacked_absolute_ind.png" alt="enter image description here"></p>
<p>Caso estivéssemos interessando em estudar de forma percentual a representação de cada espécie, poderíamos usar um stacked barplot com a informação recalculada para porcentagem de representação.</p>
<p><img src="https://github.com/igrorp/desafio_neo/blob/main/task3/stacked_percent_time.png" alt="enter image description here"></p>
<p>E, da mesma forma que anteriormente, poderíamos representar de forma percentual a composição bacteriana associada a cada indivíduo.</p>
<p><img src="https://github.com/igrorp/desafio_neo/blob/main/task3/stacked_percent_ind.png" alt="enter image description here"></p>
<p>Podemos deduzir que os tratamentos influenciam a composição bacteriana dos indivíduos e que a diversidade de espécies entre os indivíduos do mesmo grupo é grande, o que denota uma necessidade de tratamento estatístico para verificar se as diferenças observadas são de fato significativas. Uma espécie que parece chamar atenção é <em>C. aerofaciens</em>, cuja abundância é bem maior em indivíduos do grupo “Late”. Essa espécie comensal habita o intestino de mamíferos e sua abundância já esteve associada com a ingestão de leite por camundongos, além de outros aspectos salutares tanto positivos quanto negativos.                          (<a href="https://doi.org/10.3389/fmicb.2019.00458">https://doi.org/10.3389/fmicb.2019.00458</a>)</p>

