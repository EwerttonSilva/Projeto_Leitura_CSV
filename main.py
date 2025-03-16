import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import locale

# Definindo a formatação de Moeda
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

st.title('Leitura de CSV')

arquivo_csv = st.file_uploader('Escolha o seu arquivo CSV', type='csv')
if arquivo_csv is not None:
    
    df = pd.read_csv(arquivo_csv)

## Avaliação dos produtos
    categorias_agrupadas_por_avalaicoes = df.groupby('Category').agg({'Rating': 'mean'}).reset_index()
    top10rating = categorias_agrupadas_por_avalaicoes.sort_values('Rating', ascending=False).head(10)
    top10rating.reset_index(drop=True, inplace=True)
    top10rating.index = top10rating.index + 1

    fig = px.line(categorias_agrupadas_por_avalaicoes, x='Category', y='Rating')

    st.subheader("Top 10 Categorias Melhor Avaliadas")
    st.dataframe(top10rating)

    st.plotly_chart(fig, use_container_width=True)

## Categorias Mais Vendidas
    categoriaMaisVendida = df.groupby('Category').agg({ 'Sales': np.sum }).sort_values('Sales', ascending=False).reset_index()
    fig2 = px.bar(categoriaMaisVendida, x='Category', y='Sales')

    st.subheader("Top 10 Categorias Mais Vendidas")
    top10Vendidas = categoriaMaisVendida.sort_values('Sales', ascending=False).head(10)
    top10Vendidas.index = top10Vendidas.index + 1
    st.dataframe(top10Vendidas)
    st.plotly_chart(fig2)

# Categorias De Maior Faturamento
    df['Revenue'] = df['Price'] * df['Sales']
    CategoriasDeMaiorFaturamento = df.groupby('Category').agg({'Revenue': np.sum}).sort_values('Revenue', ascending=False).reset_index()
    st.subheader("Top 10 Categorias de Maior Faturamento")
    fig3 = px.bar(CategoriasDeMaiorFaturamento, x='Category', y='Revenue')

    top10fat = CategoriasDeMaiorFaturamento.sort_values('Revenue', ascending=False).head(10)
    top10fat.index = top10fat.index + 1
    # Formatar Revenue para Real
    top10fat['Revenue'] = top10fat['Revenue'].apply(lambda x: locale.currency(x, grouping=True))
    st.dataframe(top10fat)

    st.plotly_chart(fig3)

    # Total de Receita
    receita = df['Revenue'].sum()
    # Formatar Receita para Real
    st.title(f'Total Receita: {locale.currency(receita, grouping=True)}')

else:
    st.info("Por favor, faça o upload de um arquivo CSV para começar a análise.")
