# Texto de análise

## Descrição do Simulador

A simulação aqui proposta busca representar as colaborações entre pesquisadores distribuídos entre vários locais distintos.

A cada step, são atualizados a idade (o cientista se torna mais velho com a passagem do tempo) e a saúde (podendo melhorar ou piorar); e avaliado, através de um cálculo probabilistico, se ele colaborará ou não com seus vizinhos.

O código, este texto, os resultados da simulação e os gráficos gerados a partir dos dados se encontram disponíveis [no nosso repositório](https://github.com/luthierycosta/CE-trab-mesa).

## Descrição da simulação e dos dados gerados

A lista de universidades foi obtida pelo rank das melhores universidades em 2019 pela [Folha de São Paulo](https://ruf.folha.uol.com.br/2019/ranking-de-universidades/principal/); e, a lista de interesses de pesquisa dos cientistas foi obtida através da seleção de um pequeno subconjunto de todas áreas de pesquisa existentes hoje e listadas pela [CAPES](http://fisio.icb.usp.br:4882/posgraduacao/bolsas/capesproex_bolsas/tabela_areas.html).

Os estados do cientista podem ser:
- Em busca de colaboração
- Colaborando
- Coordenando (isto é, quando está com 3 ou mais colaborações simultâneas)
- Indisponível (quando sua saúde é menor que 50)

Verificamos a Universidade (peso 1), Cidade (peso 1), Área de conhecimento (peso 2), Área de Interesse Específico (peso 2), Necessidade financeira (peso 2) e Estado do cientista (peso 2) para indicar se ele irá ou não colaborar com outro.

Utilizando dados reais como entrada para nossa simulação, era esperado conseguir uma simulação mais próxima de um ambiente real. No final da simulação foi gerado um arquivo .txt, com uma lista de todas as relações de colaboração no último instante de tempo da simulação. Nesse arquivo, cada linha representa uma aresta (colaboração) no grafo, tendo dois números por linha, o nó origem e o nó destino.

## Análise dos dados gerados

O arquivo gerado, *results.txt*, contém a lista de todas as colaborações entre cientistas no último instante de tempo simulado. Como o grafo da simulação é não-direcionado, a lista contém repetições, isto é, se o nó *i* tem aresta para o nó *j* então a aresta de *j* para *i* também consta na lista.

É possível notar com os dados do arquivo - e do gráfico gerado com **R** posteriormente a partir dele - que a maioria dos cientistas possuem um número alto de colaborações com muitos outros cientistas, o que não condiz com a tendência observada com os dados da tarefa 3.5. Na nossa simulação, reconhecemos que o fenômeno da criação de redes de colaboração, centralizadas em torno dos chamados "coordenadores" não foi bem representado, tendo os cientistas da simulação fazendo muitas vezes colaborações aleatórias com outros cientistas da mesma área de conhecimento e/ou da mesma universidade.

## Discussão de problemas da simulação

- Falta de recursos computacionais para executar a simulação na mesma escala que os dados supostos anteriormente (na base de dados da tarefa 3.5, existiam 18772 nós, enquanto a nossa simulação não conseguiu executar em velocidade viável com mais de 1000 nós).
- Dificuldade na construção da abstração para o Python Mesa.
- Difícil curva de aprendizagem na utilização do framework.
- Dificuldade na evaluação dos parâmetros do cientista para a definição da colaboração entre os cientistas.

## Reflexões pessoais

### Luthiery Costa (17/0040631)
Nesse semestre entramos em contato com uma ferramenta totalmente nova, ao menos pra mim, para fazer uma simulação multi-agente que também foi algo inédito. Como era de se esperar, encontrei grande dificuldade em como usar o framework, e como adaptar os tutoriais encontrados e exemplo do professor à realidade da nossa simulação. Houve também problemas de motivação e de entendimento sobre a especificação das tarefas. Contudo, aprendemos bastante com a experiência, que pode ser útil no fim do curso.

### Henrique Mariano (17/0012280)
Neste semestre tivemos um grande aprendizado sobre a experimentação em computação, utilizando o framework python mesa para realizar uma simulação computacional, além do grande aprendizado em relação a análise de dados reais em comparação a uma simulação. Com isso, foi possível se aprofundar na matéria e torná-la mais interativa com o aluno.

### Thales Menezes (17/0045919)

Em comparação com semestres anteriores, esse semestre teve uma atenção particularmente grande a etapa de experimentação. No meu caso, que já havia feito parcialmente a disciplina, achei o conteúdo complementar ao conhecimento desenvolvido anteriormente. Entretanto, me questiono se esse foco não tirou atenção da etapa de classicação de referencial teórico.
