# 1. Problema de negócio:
   A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
  business é facilitar o encontro e negociações de clientes e restaurantes. Os
  restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
  informações como endereço, tipo de culinária servida, se possui reservas, se faz
  entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
  dentre outras informações.
  
   Enquanto a empresa vê um aumento nas entregas, o CEO enfrenta desafios para visualizar 
   completamente os KPIs de crescimento. A Fome Zero gera dados valiosos sobre localizações, 
   avaliações de restaurantes e preços dos pratos, indicando a necessidade de uma análise de 
   dados eficaz para melhor compreender estes indicadores chave.
  
   Você foi contratado como Cientista de Dados da empresa
  Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO da empresa
  a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
  utilizando dados!


   Dentro da estrutura do seu modelo de negócio Marketplace, que conecta restaurantes, e clientes, a 
  Fome Zero busca expandir sua análise de dados para acompanhar de perto o crescimento e o 
  desempenho em diferentes áreas. Isto inclui uma visão geral das transações e interações 
  no marketplace, análises detalhadas por país e cidade para entender a expansão geográfica, 
  tendências e preferências nos tipos de culinária ofertados pelos restaurantes cadastrados, 
  bem como insights específicos sobre o desempenho e popularidade dos restaurantes individuais. 
  Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

# 2. Premissas assumidas para a análise:
   1. A análise foi realizada com dados entre 05/10/2023 e 03/01/2024.
   2. Marketplace foi o modelo de negócio assumido.
   3. Os 3 principais visões do negócio foram: visão geral, Visao dos paises, visao das cidades,
    visão tipos culinarios e visão Restaurantes.


# 3. Estratégia da solução:

### Visao Geral:
  
  1. Quantos restaurantes únicos estão registrados?
  2. Quantos países únicos estão registrados?
  3. Quantas cidades únicas estão registradas?
  4. Qual o total de avaliações feitas?
  5. Qual o total de tipos de culinária registrados?


### Visao Paises:

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

### Visao Cidades:

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?


### Visao Tipos de Culinária:

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

### Visao Restaurantes:

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?


# 4.0 - Top 3 Insights de Dados:
   
   1.0 - Diversidade de Ofertas e Alcance Global:

   A Fome Zero tem uma presença global significativa, evidenciada pelo registro de 5914 
   restaurantes únicos espalhados por 15 países diferentes e 125 cidades. Isso demonstra 
   a ampla gama de escolhas disponíveis para os clientes e o potencial de crescimento em novos mercados.
   A plataforma oferece uma grande variedade de opções culinárias, com 2832 tipos 
   de culinária únicos registrados. Isso sugere que a Fome Zero pode atender a uma vasta gama 
   de preferências alimentares e culturais, tornando-a atrativa para um público diversificado.
   
   2.0 - Foco em Qualidade e Serviço ao Cliente:

   Com um total impressionante de 4.639.654 avaliações, fica claro que a Fome Zero tem uma base 
   de usuários ativa e engajada. Isso não só indica um alto nível de interação dos clientes com 
   a plataforma, mas também fornece uma rica fonte de dados para análises e melhorias contínuas no serviço.
   
   
  3.0 - Tendências Regionais e Oportunidades de Crescimento:

   Observa-se uma concentração significativa de atividades em certos países. Por exemplo, A India domina 
   em várias categorias, incluindo o maior número de cidades registradas, a maioria dos restaurantes registrados, 
   a maior variedade de culinárias e a maioria das avaliações. Este país pode representar um mercado chave para a 
   Fome Zero, tanto em termos de volume de negócios quanto de diversidade de ofertas. Por outro lado, os EUA se 
   destaca por ter o maior número de restaurantes de alto preço, indicando uma possível tendência de mercado 
   de luxo ou de alta gastronomia.


  # 5.0 - O produto final do projeto:

   Painel online, hospedado em um Cloud e disponível para acesso em
   qualquer dispositivo conectado à internet.
   O painel pode ser acessado através desse link: https://fomezerocompany-glauberds.streamlit.app/


   # 6.0 - Conclusao:

   A Fome Zero demonstra um potencial significativo para crescimento e expansão, com oportunidades 
   para aprimorar ainda mais a experiência do cliente e expandir sua base de usuários em mercados 
   existentes e novos. A análise detalhada dos dados pode continuar a fornecer insights valiosos 
   para a tomada de decisões estratégicas e operacionais da empresa.

# 7.0 - Proximos Passos:
   
   1. Integração de Feedback dos Usuários.
   2. Parcerias Estratégicas com Restaurantes e Fornecedores.
   3. Simplificação e Otimização da Interface do Usuário. 
