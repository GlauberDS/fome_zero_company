import streamlit as st
from PIL import Image


st.set_page_config(page_title="Home", page_icon="")

#image_path = "/Users/user/Documents/repos/glauber/ftc_programacao_python/dataset/project_fome_zero/image_fome_zero.png"
image = Image.open('image_fome_zero.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Fome Zero!")
st.sidebar.markdown("#### Nós cuidamos de sua comida, nós cuidamos de você !")
st.sidebar.markdown("""_____""")

st.write("# Fome zero Company!")
st.markdown("#### Nós cuidamos de sua comida, nós cuidamos de você !")
st.markdown("""_____""")

st.markdown(
    """
##### O Dashboard interativo foi projetado para fornecer respostas claras e abrangentes aos questionamentos propostos pelo CEO da empresa.
### Como Utilizar esse Growth Dashboard?


- ##### Resumo Geral: 
    - A Visao destaca o crescimento da empresa, evidenciando sua expansão para mais países, cidades e restaurantes.


- ##### Análise por País:
    - Descreve a análise de dados quantitativos dos restaurantes, incluindo o número de avaliações e o custo médio para duas pessoas em vários países.


- ##### Análise por Cidade:
    
    - Esta análise examina como os restaurantes estão espalhados pelas cidades, considerando suas avaliações e os tipos de comida que servem.

- ##### Análise de Restaurantes:
    - Avalia os restaurantes com base em critérios como melhores avaliações e maior número de votos, além de comparar os preços conforme o tipo de culinária e os serviços oferecidos.

- ##### Análise de Cozinhas:
    - Examina o preço médio de uma refeição para duas pessoas em diferentes tipos de cozinhas, identificando aquelas com melhores avaliações e a quantidade de restaurantes que oferecem serviços adicionais.

### Duvidas
- Time de Data Science no Discord
    - @glauber1171
"""
)
