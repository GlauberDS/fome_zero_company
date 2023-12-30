
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

st.set_page_config(page_title='Visao Cidades', page_icon='🏙️', layout='wide')


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

def top_10_cities_with_distinct_cuisines(df1):
    # Calcular a contagem de tipos culinários distintos por cidade e país
    cuisine_counts_by_city_country = df1.groupby(['city', 'country'])['cuisines'].nunique().reset_index(name='unique_cuisine_count')

    # Selecionar as top 10 Restaurantes com tipos de cozinha unicas
    top_cuisines_rated_uniq = cuisine_counts_by_city_country.nlargest(10, 'unique_cuisine_count')


    # Desenhar o gráfico de barras
    fig = px.bar(
        top_cuisines_rated_uniq,
        x='city',
        y='unique_cuisine_count',
        text=top_cuisines_rated_uniq['unique_cuisine_count'],
        title='Top 10 Cidades com mais restaurantes com tipos culinarios distintos',
        color='country',
        labels={'unique_cuisine_count': 'Quantidade de Tipos Culinarios Unicos', 'city': 'Cidades', 'country': 'País'})
        
    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Top 10 Cidades com Mais Restaurantes com tipos Culinarios Distintos',  # Título
        title_x=0.3,  # Centralizando o título
        font=dict(size=12))  # Ajustando o tamanho da fonte do título)
        
    return fig 
    

def top_7_with_lowest_ratting(df1):
    # Filtrar os restaurantes com nota média menor ou igual a 2.5
    low_rated_restaurants = df1[df1['aggregate_rating'] <= 2.5]

    # Calcular a contagem de restaurantes por cidade e país
    city_stats_low_rated = low_rated_restaurants.groupby(['city', 'country']).size().reset_index(name='restaurant_count')

    # Selecionar as top 7 cidades com as maiores contagens de restaurantes
    top_cities_low_rated = city_stats_low_rated.nlargest(7, 'restaurant_count')

    # Desenhando gráfico de barras
    fig = px.bar(
        top_cities_low_rated,
        x=top_cities_low_rated['city'],
        y='restaurant_count',
        title='Top 7 Cidades com Restaurantes e Média de Avaliação Abaixo de 2.5',
        color='country',
        labels={"country": "País", 'restaurant_count': 'Quantidade de Restaurantes', 'city': 'Cidades'})
            
    # Adicionando labels diretamente nas barras
    fig.update_traces(
        texttemplate='%{y:.2f}',  # Formatando o texto com duas casas decimais
        textposition='inside',)  # Posicionando o texto dentro da barra

    return fig


def top_7_with_highest_ratting(df1):
    # Filtrar os restaurantes com nota média acima de 4
    high_rated_restaurants = df1[df1['aggregate_rating'] >= 4]

    # Calcular a contagem de restaurantes e a média de avaliação por cidade
    city_stats = high_rated_restaurants.groupby(['city', 'country']).agg({'restaurant_id': 'count', 'aggregate_rating': 'mean'}).reset_index()

    # Adicionar uma coluna 'city_country' concatenando cidade e país
    city_stats['city_country'] = city_stats['city'] + ', ' + city_stats['country']

    # Selecionar as top 7 cidades com as maiores contagens de restaurantes
    top_cities_high_rated = city_stats.nlargest(7, 'restaurant_id')

    # Desenhando gráfico de barras
    fig = px.bar(
        top_cities_high_rated,
        x=top_cities_high_rated['city'],
        y='restaurant_id',
        title='Top 7 Cidades com Restaurantes e Média de Avaliação Acima de 4',
        color='country',  # Adicionando cor por cidade
        labels={"country": "País", 'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidades'})

    # Adicionando labels diretamente nas barras
    fig.update_traces(
        texttemplate='%{y:.2f}',  # Formatando o texto com duas casas decimais
        textposition='inside',)  # Posicionando o texto dentro da barra
    
    return fig 

def top_10_cities_with_most_restaurants(df1):
    
    # Calcular a contagem de restaurantes por cidade e país
    restaurant_counts_by_city_country = df1.groupby(['city', 'country']).size().reset_index(name='restaurant_count')

    # Selecionar as top 10 cidades com as maiores contagens de restaurantes
    top_10_cities = restaurant_counts_by_city_country.nlargest(10, 'restaurant_count').round(2)

    # Desenhando gráfico de barras
    fig = px.bar(
        top_10_cities,
        x='city',
        y='restaurant_count',
        text=top_10_cities['restaurant_count'],
        title='Top 10 Cidades com Mais Restaurantes na Base de Dados',
        labels={'restaurant_count': 'Quantidade de Restaurantes', 'city': 'Cidades', 'country': 'País'},
        color='country')  # Adicionando cor por país

    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Top 10 Cidades com Mais Restaurantes na Base de Dados',  # Título
        title_x=0.3,  # Centralizando o título
        font=dict(size=12))  # Ajustando o tamanho da fonte do título)

    # Adicionando labels diretamente nas barras
    fig.update_traces(
        texttemplate='%{y:.2f}',  # Formatando o texto com duas casas decimais
        textposition='inside',)  # Posicionando o texto dentro da barra
        
    return fig

# Criando uma funcao chamada (rename_columns) com finalidade de Renomear as colunas do DataFrame.
def rename_columns(dataframe):
    """
    Função para renomear as colunas do DataFrame.

    Parameters:
    - dataframe: DataFrame a ser renomeado.

    Returns:
    - DataFrame com as colunas renomeadas.
    """
    
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
def country_codes(country_id):
    """
    Função para obter o nome do país a partir do código do país.

    Parameters:
    - country_id: Código do país.

    Returns:
    - Nome do país correspondente ao código.
    """
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
        216: "United States of America",}


    return COUNTRIES[country_id]


# 1.1 -  Em seguida criando a coluna "country_name" no DataFrame
df1["country"] = df1["country_code"].map(country_codes)


# 2 -Criacao do Tipo de Categoria de Comida pelo Price_range:


def price_type(price_range):
    """
    Função para obter o tipo de preço com base na faixa de preço.

    Parameters:
    - price_range: Faixa de preço.

    Returns:
    - Tipo de preço correspondente à faixa.
    """
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
def color_name(color_code):
    """
    Função para obter o nome da cor com base no código de cor.

    Parameters:
    - color_code: Código de cor.

    Returns:
    - Nome da cor correspondente ao código.
    """
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",}



    return COLORS[color_code]

def clean_code(df1):
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
    
    return df1

df1 = clean_code(df1)

# =======================================
#         Barra Lateral
# =======================================


image = Image.open('image_fome_zero.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('#### Nós cuidamos de sua comida, nós cuidamos de você !')

st.sidebar.markdown('### Filtros')
paises_select = st.sidebar.multiselect("Selecione os Paises que Deseja visualizar as Informacoes",
                       df1['country'].unique(),
                       default=['Brazil', 'Canada','England','United States of America' ] )

# Filtro de Paises
linhas_selecionadas01 = df1["country"].isin(paises_select)
df1 = df1.loc[linhas_selecionadas01, :]

st.sidebar.markdown("""-------""")
st.sidebar.markdown('#### Powered by Comunidade DS')

# =======================================
#         Layout no Streamlit
# =======================================

st.markdown('## 🏙️ Visao Cidades')

# Top 10 cidades com mais restaurantes
with st.container():
    fig = top_10_cities_with_most_restaurants(df1)
   # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Top 7 cidades com Media de Avaliacao Acima de 4.0
with st.container():
    col1, col2 = st.columns(2) 
    
    #Top 7 cidades 4.0
    with col1:
        fig = top_7_with_highest_ratting(df1)
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        
    # Top 7 cidades com notas abaixo 2.5
    with col2:
        fig = top_7_with_lowest_ratting(df1)
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        
        
# Top 10 Cidades com mais restaurantes com tipos culinarios distintos
with st.container():
    fig = top_10_cities_with_distinct_cuisines(df1)
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    