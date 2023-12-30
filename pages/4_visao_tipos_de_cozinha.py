# Importando Bibliotecas Necessarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import inflection
import plotly.express as px
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

import folium 
from folium.plugins import MarkerCluster
from PIL import Image
import emoji
from streamlit_folium import folium_static
import streamlit as st

st.set_page_config(page_title='Visao Cozinha', page_icon='🍽️', layout='wide')

###------------------------------------###
###  Limpeza de Dados e Import DataSet ###
###------------------------------------###

# Limpeza de Dados e Import Dataset
df = pd.read_csv("data_set/zomato.csv")

# Removendo Dados duplicados
df.duplicated().sum()
df.drop_duplicates(inplace=True)

# Removendo os NaN values no Dataset
df.isnull().sum()
df.dropna(how="any", inplace=True)



###------------------------------------###
###               FUNCOES              ###
###------------------------------------###

def sort_restaurants_by_rattings(df1, x):
    # Calcular a média por tipo de culinária
    media_cuisines = df1.groupby('cuisines')['aggregate_rating'].mean().reset_index()

    # Ordenar por nota média em ordem decrescente
    top_cuisines = media_cuisines.sort_values(by='aggregate_rating', ascending= x)

    # Selecionar os top tipos de culinárias
    #num_restaurants1 = st.sidebar.slider('Selecione a quantidade de restaurantes desejada', 1, 20, 10, key='unique_slider_key1')
    top_cuisines_subset = top_cuisines.head(num_restaurants).reset_index(drop=True)

    if x == False:
        # Criar o gráfico de barras verticais usando plotly express
        fig = px.bar(
            top_cuisines_subset,
            x='cuisines',
            y='aggregate_rating',
            color='aggregate_rating',
            orientation='v',  # Alterado para vertical
            title=f'Top {num_restaurants} Melhores Tipos de Culinárias',
            labels={'aggregate_rating': 'Média de Avaliação Média', 'cuisines': 'Tipo de Culinária'},)
    else:
        # Criar o gráfico de barras verticais usando plotly express
        fig = px.bar(
            top_cuisines_subset,
            x='cuisines',
            y='aggregate_rating',
            color='aggregate_rating',
            orientation='v',  # Alterado para vertical
            title=f'Top {num_restaurants} Piores Tipos de Culinárias',
            labels={'aggregate_rating': 'Média de Avaliação Média', 'cuisines': 'Tipo de Culinária'},)

    # Atualizar o texto formatado com duas casas decimais
    fig.update_traces(texttemplate='%{y:.2f}', textposition='inside')
    
    return fig

def most_restaurant_by_ratting(df1):
    # Supondo que você tenha uma coluna 'country' e 'cuisines' em seu DataFrame df1
    # Classificar o DataFrame pela coluna 'aggregate_rating' em ordem decrescente
    df_sorted = df1.sort_values(by='aggregate_rating', ascending=False)

    # Criar um DataFrame contendo os top 10 restaurantes mais bem avaliados por país e tipo de culinária
    top_restaurants_by_country_cuisine = (df_sorted.groupby(['country', 'cuisines'])
                                                   .head(num_restaurants)[['restaurant_id','restaurant_name', 
                                                                        'country','city', 'aggregate_rating', 
                                                                        'cuisines', 'average_cost_for_two', 'currency']])

    # Ordenar o DataFrame resultante pelos valores médios do prato para 2 pessoas em ordem decrescente
    top_restaurants_by_country_cuisine = top_restaurants_by_country_cuisine.sort_values(by='average_cost_for_two', ascending=False)

    # Exibir apenas os top 10 restaurantes mais bem avaliados e com maior valor médio do prato para 2 pessoas
    fig = top_restaurants_by_country_cuisine.head(num_restaurants)
        
    return fig


import streamlit as st

def display_best_restaurants(df1, num_colunas=5):
    # Agrupe os dados por tipo culinário e obtenha os melhores restaurantes para cada tipo
    melhores_restaurantes_por_tipo = df1.groupby('cuisines').apply(
        lambda x: x.nlargest(1, 'aggregate_rating')).reset_index(drop=True)

    # Divida o DataFrame em partes iguais para cada coluna
    partes = [melhores_restaurantes_por_tipo.iloc[i:i+num_colunas]
              for i in range(0, len(melhores_restaurantes_por_tipo), num_colunas)]

    # Para cada parte, criar uma coluna na grade
    for parte in partes:
        colunas = st.columns(num_colunas)
        for idx, (_, row) in enumerate(parte.iterrows()):
            with colunas[idx]:
                label = f"{row['cuisines']}: {row['restaurant_name']}"
                value = f"{row['aggregate_rating']}/5.0"
                info_adicional = f"**País:** {row['country']}  \n**Cidade:** {row['city']}  \n**Preço para duas pessoas:** {row['currency']}{row['average_cost_for_two']}"
                st.metric(label=label, value=value, help=info_adicional)



# Criando uma funcao chamada (rename_columns) com finalidade de Renomear as colunas do DataFrame.
def rename_columns(dataframe):
    # Faz uma cópia do DataFrame de entrada para evitar modificações inesperadas.
    df = dataframe.copy()
    # Define três funções lambda para a transformação de nomes de coluna.

    # Converte para formato de título (capitaliza palavras).
    title = lambda x: inflection.titleize(x)
    # Converte para snake_case (substitui espaços por sublinhados e torna tudo minúsculo).
    snakecase = lambda x: inflection.underscore(x)
    # Remove espaços em branco.
    spaces = lambda x: x.replace(" ", "")

    # Obtém a lista de nomes de coluna originais.
    cols_old = list(df.columns)

    # Aplica as transformações em cascata nas colunas.

    # Aplica titleize.
    cols_old = list(map(title, cols_old))
    # Remove espaços em branco.
    cols_old = list(map(spaces, cols_old))
    # Aplica underscore para obter os novos nomes de coluna em formato snake_case.
    cols_new = list(map(snakecase, cols_old))

    # Define os novos nomes de coluna no DataFrame.
    df.columns = cols_new
    # Retorna o DataFrame com as colunas renomeadas.
    return df


# Criando Uma copia da Funcao (rename_columns):
df1 = rename_columns(df)

## 1. Preenchimento do nome dos países:
# Criando uma funcao com o nome country_name com fins de subistituir alguns "Country Code" pelo nome dos paises.

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}


def country_codes(country_id):
    return COUNTRIES[country_id]


# 1.1 -  Em seguida criando a coluna "country_name" no DataFrame
df1["country"] = df1["country_code"].map(country_codes)


# 2 -Criacao do Tipo de Categoria de Comida pelo Price_range:


def price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


# 2.1 - Criando a coluna price_type a partir da funcao price_type

df1["price_type"] = df1["price_range"].map(price_type)


# 3 -Criando funcao: (color_name) pela coluna ("Rating color")

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}


def color_name(color_code):
    return COLORS[color_code]


# 3.1 -Criando coluna com nome(color_name) no DataFrame(df1).
df1["color_name"] = df1["rating_color"].map(color_name)

# Categorizando todos os restaurantes por tipo de culinaria (Cuisines):
# Foi primeiramente tratado os valores nulos(NaN), depois foi convertido os valores nulos em STR(string)
# Assim foi possivel usar a funcao split para substituir os valores nulos (NaN) .

df1["cuisines"] = (
    df1["cuisines"].fillna("").astype(str).apply(lambda x: x.split(",")[0])
)

# Removendo Linhas da coluna "cuisines" que nao fazem parte de tipos de Cuisines("Mineira", "Drinks Only")
# Para tratar valores nulos e substituir valores em uma coluna, você pode usar o método replace:

df1["cuisines"].replace({"Mineira": np.nan, "Drinks Only": np.nan}, inplace=True)
df1.dropna(subset=["cuisines"], inplace=True)

# Eliminando Colunas que nao serao utilizadas
colunas_deletadas = ["country_code", "switch_to_order_menu", "price_range"]
df1.drop(columns=colunas_deletadas, inplace=True)

# =======================================
#         Barra Lateral
# =======================================

#Imagem da logo

image = Image.open('image_fome_zero.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('#### Nós cuidamos de sua comida, nós cuidamos de você !')
st.sidebar.markdown("""-------""")

st.sidebar.markdown('### Filtros')
paises_select = st.sidebar.multiselect("Selecione os Paises que Deseja visualizar as Informacoes",
                       df1['country'].unique(),
                       default=['Brazil', 'Canada','England','United States of America' ] )

# Filtro de Paises
linhas_selecionadas01 = df1["country"].isin(paises_select)
df1 = df1.loc[linhas_selecionadas01, :]

st.sidebar.markdown("""-------""")

# Criar um slider para selecionar a quantidade de restaurantes
num_restaurants = st.sidebar.slider('Selecione a quantidade de restaurantes desejada', 1, 20, 10)
st.sidebar.markdown("""-------""")


cuisines_select = st.sidebar.multiselect("Selecione os Tipos Culinarios",
                       df1['cuisines'].unique(),
                       default=['Italian', 'European', 'American', 'Fast Food', 'Brazilian'] )

# Filtro de Paises
linhas_selecionadas02 = df1["cuisines"].isin(cuisines_select)
df1 = df1.loc[linhas_selecionadas02, :]

st.sidebar.markdown('#### Powered by Comunidade DS')

# =======================================
#         Layout no Streamlit
# =======================================

st.title('🍽️ Visao dos Tipos Culinarios!')
# Layout do Streamlit
st.markdown("### Melhores Restaurantes dos Principais Tipos Culinários")

# Melhores Restaurantes por Tipo de Culinaria
with st.container():
    # Uso da função no Streamlit
    display_best_restaurants(df1, 5)
    
with st.container():
    # Exibir o título com base no valor selecionado no slider
    st.write(f'#### Top {num_restaurants} - Restaurantes Mais Bem Avaliados e com Maior Valor Médio do Prato para 2 Pessoas!')
    fig = most_restaurant_by_ratting(df1)
    # Exibindo no Streamlit usando a função st.dataframe
    st.dataframe(fig, use_container_width=True)


#Top 10 Melhores Restaurantes Tipos de Culinarias
with st.container():
    fig = sort_restaurants_by_rattings(df1, False)
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


#Top 10 Piores Restaurantes Tipos de Culinarias
with st.container():
    fig = sort_restaurants_by_rattings(df1, True)
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    



    

   




















