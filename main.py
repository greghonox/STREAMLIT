import streamlit as st
from requests import get
import pandas as pd
import plotly.express as px


st.title("DashBoard de Vendas :shop_troley:")
st.write("Este é um DashBoard interativo para análise de vendas")

url = "https://labdados.com/produtos"
response = get(url)


if response.status_code == 200:
    data = response.json()
    data_frame = pd.DataFrame.from_dict(data)
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Receitas", "R$ {:.2f}".format(data_frame["Preço"].sum()))
    with col2:
        st.metric("Quantidade de Produtos", data_frame.shape[0])
    st.dataframe(data_frame)
else:
    st.write("Erro ao carregar os dados")
