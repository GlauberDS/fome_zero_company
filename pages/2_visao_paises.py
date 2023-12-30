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

st.set_page_config(page_title='Visao Paises', page_icon='🌍', layout='wide')


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

def plot_avg_price_for_two_by_country(dataframe):
    """
    Plota a média de preço para dois por país usando um gráfico de barras.

    Parameters:
        - dataframe: O DataFrame contendo os dados.

    Returns:
        None
    """
    # Fazendo a média de preço para dois por países usando a função ("groupby()") e ("mean()")
    average_price_for_two_by_country = dataframe.groupby('country')['average_cost_for_two'].mean().reset_index()

    # Ordenando o DataFrame pela média de preço em ordem decrescente usando a função sort_values() para ordenar a quantidade.
    average_price_for_two_by_country = average_price_for_two_by_country.sort_values(by='average_cost_for_two', ascending=False)

    # Desenhando o gráfico de barras
    fig = px.bar(average_price_for_two_by_country, 
                 x='country', 
                 y='average_cost_for_two',
                 color='average_cost_for_two',
                 text=average_price_for_two_by_country['average_cost_for_two'].apply(lambda x: f"{x:.2f}"),
                 title='Média de Preço para Dois por País',
                 labels={"country": "Países", 'average_cost_for_two': 'Preço do prato para duas pessoas'} )

    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Média de Preço de um prato para 2 pessoas por País',  # Título
        title_x=0.2,  # Centralizando o título
        font=dict(size=12))  # Ajustando o tamanho da fonte do título)

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_avg_votes_by_country(dataframe):
    """
    Plota a média de avaliações (votes) por país usando um gráfico de barras.

    Parameters:
        - dataframe: O DataFrame contendo os dados.

    Returns:
        None
    """
    # Fazendo a média de avaliações (votes) por países usando a função ("groupby()") e ("mean()")
    avg_mean_country = dataframe.groupby('country')['votes'].mean().reset_index()

    # Ordenando o DataFrame pela média de avaliações em ordem decrescente usando a função sort_values() para ordenar a quantidade.
    mean_avg_by_country = avg_mean_country.sort_values(by='votes', ascending=False).round(2)

    # Desenhando o gráfico de barras
    fig = px.bar(mean_avg_by_country, 
                 x='country', 
                 y='votes',
                 color='votes',
                 text=mean_avg_by_country['votes'],
                 title='Média de Avaliações Feitas por País',
                 labels={"country": "Países", 'votes': 'Quantidade de Avaliações'})

    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Média de Avaliações Feitas por País',  # Título
        title_x=0.2,  # Centralizando o título
        font=dict(size=12))  # Ajustando o tamanho da fonte do título)

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_quantity_of_cities_by_country(dataframe):
    """
    Plota a quantidade de cidades por país usando um gráfico de barras.

    Parameters:
        - dataframe: O DataFrame contendo os dados.

    Returns:
        None
    """
    # Fazendo uma contagem da quantidade de cidades por países usando a função ("groupby()") e ("nunique()")
    city_counts = dataframe['city'].groupby(dataframe['country']).nunique().reset_index()

    # Ordenando o DataFrame pela quantidade de cidades em ordem decrescente usando a função sort_values() para ordenar a quantidade.
    count_city_by_country = city_counts.sort_values(by='city', ascending=False)

    # Desenhando o gráfico de barras
    fig = px.bar(count_city_by_country, 
                 x='country', 
                 y='city',
                 color='city',
                 text=count_city_by_country['city'],
                 title='Quantidade de Cidades Registradas por País',
                 labels={"country": "Países", 'city': 'Quantidade de Cidades'})

    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Quantidade de Cidades Registradas por País',  # Título
        title_x=0.3,  # Centralizando o título
        font=dict(size=14))  # Ajustando o tamanho da fonte do título)

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


def plot_quantity_by_category(dataframe, category_column, quantity_column, plot_title):
    """
    Plota a quantidade por categoria usando um gráfico de barras.

    Parameters:
        - dataframe: O DataFrame contendo os dados.
        - category_column: A coluna usada para categorizar os dados.
        - quantity_column: A coluna contendo a quantidade para contar.
        - plot_title: O título do gráfico.

    Returns:
        None
    """
    # Contando a quantidade por categoria
    category_counts = dataframe[quantity_column].groupby(dataframe[category_column]).count().reset_index()

    # Ordenando o DataFrame pela quantidade em ordem decrescente
    count_by_category = category_counts.sort_values(by=quantity_column, ascending=False)

    # Desenhando o gráfico de barras
    fig = px.bar(count_by_category, 
                 x=category_column, 
                 y=quantity_column,
                 text=count_by_category[quantity_column],
                 color=quantity_column,
                 labels={category_column: 'Paises', quantity_column: f'Quantidade de Restaurantes'})
    
    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text=plot_title,  # Título
        title_x=0.3,  # Centralizando o título
        font=dict(size=14))  # Ajustando o tamanho da fonte do título)

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

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

    df1["cuisines"] = (df1["cuisines"].fillna("")
                                      .astype(str)
                                      .apply(lambda x: 
                                     x.split(",")[0]))

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
st.sidebar.markdown('# Fome Zero !')
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

st.title(emoji.emojize('🌍 Visao Paises'))

#Quantidade de Restaurante por Pais

with st.container():
    # Plota a quantidade por categoria usando um gráfico de barras.
    plot_quantity_by_category(df1, 'country', 'restaurant_id', 'Quantidade de Restaurantes Registrados por País')
    
# Quantidade de Cidades por pais

with st.container():
    # Plota a quantidade de cidades por país usando um gráfico de barras.
    plot_quantity_of_cities_by_country(df1)
    


with st.container():
    col1,col2 = st.columns(2)
    
    # Media de Avaliacoes feitas por Pais
    with col1:
        # Plota a média de avaliações (votes) por país usando um gráfico de barras.
        plot_avg_votes_by_country(df1)
        
    # Media de Preco de um prato para 2 pessoas por Pais
    with col2:
        #Plota a média de preço para dois por país usando um gráfico de barras.
        plot_avg_price_for_two_by_country(df1)