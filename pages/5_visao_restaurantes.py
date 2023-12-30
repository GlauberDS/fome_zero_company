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

st.set_page_config(page_title='Visao Restaurantes', page_icon='🍝', layout='wide')

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

def mean_cost_for_two_jap_bbq(df1):
    # Filtrar apenas restaurantes de culinária japonesa nos Estados Unidos
    japanese_restaurants_usa = df1[(df1['cuisines'] == 'Japanese') & (df1['country'] == 'United States of America')]

    # Filtrar apenas churrascarias americanas (BBQ) nos Estados Unidos
    bbq_restaurants_usa = df1[(df1['cuisines'] == 'BBQ') & (df1['country'] == 'United States of America')]

    # Calcular os valores médios para duas pessoas
    average_cost_japanese = japanese_restaurants_usa['average_cost_for_two'].mean()
    average_cost_bbq = bbq_restaurants_usa['average_cost_for_two'].mean()

    # Criar o gráfico de pizza com Plotly Express
    fig = px.pie(
        names=['Culinária Japonesa', 'Churrascaria Americana (BBQ)'],
        values=[average_cost_japanese, average_cost_bbq],
        title='Comparação de Valor Médio para Duas Pessoas entre Culinária Japonesa e Churrascaria Americana (BBQ) nos EUA',
        labels={'Culinária Japonesa': 'Valor Médio para Duas Pessoas', 'Churrascaria Americana (BBQ)': 'Valor Médio para Duas Pessoas'},)

    return fig

def mean_avg_cost_for_two(df1):
    # Mapeamento dos valores 0 e 1 para rótulos desejados
    table_booking_mapping = {0: 'Não', 1: 'Sim'}

    # Substituir os valores na coluna 'has_online_delivery'
    df1['has_table_booking'] = df1['has_table_booking'].map(table_booking_mapping)

    # Calcular a média de avaliações por tipo de restaurante
    average_booking_table_cost = df1.groupby('has_table_booking')['average_cost_for_two'].mean().reset_index()


    # Criar o gráfico de pizza com Plotly Express
    fig = px.pie(average_booking_table_cost,
                names='has_table_booking', 
                values='average_cost_for_two',
                title='Distribuição da Média de Restaurantes que Fazem Reserva ou Não por País',
                color='has_table_booking',)  # Adicionando cores diferentes para 'Sim' e 'Não'
                # Exibir informações do país ao pairar sobre o gráfico
            
    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Comparativo do Valor do Prato para 2 Pessoas',  # Título
        title_x=0.2,  # Centralizando o título
        font=dict(size=12))  # Ajustando o tamanho da fonte do título)
    
    return fig
        

def mean_avg_online_orders(df1):
    # Mapeamento dos valores 0 e 1 para rótulos desejados
    online_delivery_mapping = {0: 'Não', 1: 'Sim'}

    # Substituir os valores na coluna 'has_online_delivery'
    df1['has_online_delivery'] = df1['has_online_delivery'].map(online_delivery_mapping)

    # Calcular a média de avaliações por tipo de restaurante
    average_votes_by_online_order = df1.groupby('has_online_delivery')['votes'].mean().reset_index()

    # Criar o gráfico de pizza com Plotly Express
    fig = px.pie(average_votes_by_online_order,
        names='has_online_delivery', values='votes',
        title='Distribuição da Média de Avaliações por Aceitação de Pedido Online')
        
    # Atualizando o layout para ajustar o título
    fig.update_layout(
        title_text='Comparativo de Quantidade de Avaliacoes Media',  # Título
        title_x=0.2,  # Centralizando o título
        font=dict(size=12))  # Ajustando o tamanho da fonte do título)
    
    return fig


def top_restaurants_with_mots_votes(df1):
    # Exibir o título com base no valor selecionado no slider
    st.write(f'#### Top {num_restaurants} - Restaurantes Mais Votados!')
    # Top 10 Restaurantes Mais Votados
    # Supondo que você tenha uma coluna 'country' em seu DataFrame df1
    # Classificar o DataFrame pela coluna 'votes' em ordem decrescente
    df_sorted = df1.sort_values(by='votes', ascending=False)

    # Selecionar os top 10 restaurantes mais bem votados
    top_restaurants = df_sorted.head(num_restaurants)
        
    # Remover duplicatas com base no nome do restaurante
    unique_restaurants = top_restaurants.drop_duplicates(subset='restaurant_name')


    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(
        unique_restaurants,
            x='restaurant_name',
            y='votes',
            labels={'votes': 'Quantidade de Votos', 'restaurant_name': 'Restaurante', 'country': 'Paises'},
            color='country')

    # Adicionar a quantidade total de votos em cada barra
    fig.update_traces(text=unique_restaurants['votes'], textposition='inside')

    # Adicionar o nome do país nas labels
    fig.update_layout(
            xaxis_title='Restaurantes',
            yaxis_title='Quantidade de Avaliacoes',
            bargap=0.3)  # Espaçamento entre as barras
        
    return fig

def top_10_restaurants_with_most_analysis(df1):
    # Exibir o título com base no valor selecionado no slider
    st.write(f'#### Top {num_restaurants} - Restaurantes Mais Bem Avaliados!')
    # Supondo que você tenha uma coluna 'country' e 'cuisines' em seu DataFrame df1
    # Classificar o DataFrame pela coluna 'aggregate_rating' em ordem decrescente
    df_sorted = df1.sort_values(by='aggregate_rating', ascending=False)

    # Criar um DataFrame contendo os top 10 restaurantes mais bem avaliados por país e tipo de culinária
    top_restaurants_by_country_cuisine = (df_sorted.groupby(['country', 'cuisines'])
                                                .head(num_restaurants)[['restaurant_name','country', 'aggregate_rating','cuisines',  ]])

    # Exibir apenas os top 10 restaurantes mais bem avaliados
    fig = top_restaurants_by_country_cuisine.head(num_restaurants)
        
    return fig


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
st.sidebar.image('image_fome_zero.png', width=120)

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
num_restaurants = st.sidebar.slider('Selecione a quantidade de restaurantes', 1, 20, 10)

st.sidebar.markdown("""-------""")
st.sidebar.markdown('#### Powered by Comunidade DS')

# =======================================
#         Layout no Streamlit
# =======================================

st.markdown('## 🍝 Visao Restaurantes')

# Top 10 Restaurantes Mais bem avaliados 
with st.container():
    fig = top_10_restaurants_with_most_analysis(df1)
    # Exibindo no Streamlit usando a funcao st.dataframe
    st.dataframe(fig, use_container_width=True)
    
           
with st.container():
    fig = top_restaurants_with_mots_votes(df1)
     # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
     

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        fig = mean_avg_online_orders(df1) 
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
             
        
    with col2:
        fig = mean_avg_cost_for_two(df1)
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
                    
with st.container():
    fig = mean_cost_for_two_jap_bbq(df1)
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)  
    
    
    
  



   
        