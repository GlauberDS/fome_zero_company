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

from streamlit_folium import folium_static
import streamlit as st

st.set_page_config(page_title='Visao Geral', page_icon='map', layout='wide')


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

def exibir_mapa_restaurantes(dataframe):
    """
    Função para exibir um mapa de restaurantes com informações de localização.

    Parameters:
    - dataframe: DataFrame contendo os dados dos restaurantes.

    Returns:
    - None
    """
    st.markdown('### Mapa dos Restaurantes')

    # Transformando coluna "average_cost_for_two" em tipo numérico.
    dataframe['average_cost_for_two'] = pd.to_numeric(dataframe['average_cost_for_two'], errors='coerce')

    # Corrige o DataFrame
    df_aux = (dataframe.loc[:, ['restaurant_id', 'restaurant_name', 'rating_color', 'average_cost_for_two', 'currency', 'cuisines', 'aggregate_rating', 'latitude', 'longitude']]
        .groupby(['restaurant_id', 'restaurant_name', 'rating_color', 'average_cost_for_two', 'currency', 'cuisines', 'aggregate_rating'])
        .value_counts()
        .reset_index())

    # Criar um mapa
    mapa = folium.Map(tiles="OpenStreetMap", zoom_start=8)
    marker_cluster = MarkerCluster().add_to(mapa)

    # Iterar sobre o DataFrame df_aux com informações de localização
    for index, location_info in df_aux.iterrows():
        # Construir o conteúdo do popup com HTML e CSS
        popup_content = f"""
            <div style="font-weight: bold;">{location_info['restaurant_name']}</div><br>
            <div>Price: {location_info['average_cost_for_two']},00 ({location_info['currency']}) para dois</div>
            <div>Type: {location_info['cuisines']}</div>
            <div>Aggregate Rating: {location_info['aggregate_rating']}/5.0</div>
        """

        # Adicionar marcadores ao cluster
        folium.Marker(
            [location_info['latitude'], location_info['longitude']],
            popup=folium.Popup(popup_content, max_width=300, max_height=600),  # Ajuste a largura conforme necessário
            icon=folium.Icon(color=color_name(location_info['rating_color']), icon_color='white', icon='house', angle=0, prefix='fa')
        ).add_to(marker_cluster)

    # Exibir o mapa
    folium_static(mapa, width=1024, height=600)

def exibir_metrica_sum(dataframe, coluna, titulo, coluna_streamlit):
    """
    Função para exibir uma métrica contendo a soma dos valores de uma coluna.

    Parameters:
    - dataframe: DataFrame contendo os dados.
    - coluna: Nome da coluna para calcular a soma.
    - titulo: Título da métrica.
    - coluna_streamlit: Coluna do Streamlit (st.col1, st.col2, etc.) para exibição.

    Returns:
    - None
    """
    with coluna_streamlit:
        total_soma = dataframe[coluna].sum()

        # Usando a função format para adicionar pontos decimais
        numero_formatado = '{:,}'.format(total_soma)

        # Substituindo as vírgulas por pontos
        numero_formatado = numero_formatado.replace(',', '.')

        st.markdown(f'<p style="font-size:14px">{titulo}</p>', unsafe_allow_html=True)
        st.metric('', numero_formatado)

# Defina a função exibir_metrica_nunique antes de usá-la
def exibir_metrica_nunique(dataframe, coluna, titulo, coluna_streamlit):
    """
    Função para exibir uma métrica contendo a contagem de valores únicos de uma coluna.

    Parameters:
    - dataframe: DataFrame contendo os dados.
    - coluna: Nome da coluna para calcular os valores únicos.
    - titulo: Título da métrica.
    - coluna_streamlit: Coluna do Streamlit (st.col1, st.col2, etc.) para exibição.

    Returns:
    - None
    """
    with coluna_streamlit:
        qtd_valores_unicos = dataframe[coluna].nunique()
        st.markdown(f'<p style="font-size:14px">{titulo}</p>', unsafe_allow_html=True)
        st.metric('', qtd_valores_unicos)

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
        df1["cuisines"].fillna("").astype(str).apply(lambda x: x.split(",")[0]))

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

image_path = 'image_fome_zero.png'
image = Image.open('image_fome_zero.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('#### Nós cuidamos de sua comida, nós cuidamos de você !')

st.sidebar.markdown('### Filtros')
paises_select = st.sidebar.multiselect("Selecione os Paises que Deseja visualizar os Restaurantes",
                       df1['country'].unique(),
                       default=['Brazil', 'Canada','England','United States of America' ] )

# Filtro de Paises
linhas_selecionadas01 = df1["country"].isin(paises_select)
df1 = df1.loc[linhas_selecionadas01, :]

st.sidebar.markdown("""-------""")

# Criando Funcao para colocar botao para Download de arquivo CSV
st.sidebar.markdown('### Dados Tratados')

@st.cache
def convert_df(file_path):
    # Load the CSV file from the specified path
    df1 = pd.read_csv(file_path, on_bad_lines='skip')
    # Convert the DataFrame to CSV and encode it
    return df1.to_csv().encode('utf-8')

# Especifique o caminho do arquivo CSV no seu computador
file_path = 'data_set/zomato.csv'

# Chame a função para converter e obter o botão de download
csv = convert_df(file_path)

# Crie o botão de download na sidebar
st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv',
    mime='text/csv')

# =======================================
#         Layout no Streamlit
# =======================================

st.markdown('# Fome Zero!')
st.markdown('### Nós cuidamos de sua comida, nós cuidamos de você !')
st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # Exemplo de uso para 'restaurant_id' no col1
        exibir_metrica_nunique(df1, 'restaurant_id', 'Restaurantes Cadastrados', col1)
        
    with col2:
        # Exemplo de uso para 'country' no col2
        exibir_metrica_nunique(df1, 'country', 'Paises Cadastrados', col2)
        
    with col3:
        # Exemplo de uso para 'country' no col3
        exibir_metrica_nunique(df1, 'city', 'Paises Cadastrados', col3)
        
    with col4:
        # Exemplo de uso para 'votes' no col4
        exibir_metrica_sum(df1, 'votes', 'Avaliacoes Feitas na Plataforma', col4)
        
    with col5:
        # Exemplo de uso para 'country' no col5
        exibir_metrica_nunique(df1, 'city', 'Paises Cadastrados', col5)
        
    
with st.container():
        
    # Exemplo de uso do mapa no Streamlit
    exibir_mapa_restaurantes(df1)