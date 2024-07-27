import streamlit as st
import pandas as pd

import plotly.express as px

# set config widmode
st.set_page_config(
    page_title="DashBoard de Vendas",
    page_icon="🔸",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("DashBoard de Vendas 🔸")
st.write("Este é um DashBoard interativo para análise de vendas")

data = pd.read_csv("2024-07-27T23-35_export.csv")
data_frame = pd.DataFrame.from_dict(data)
data_frame["Data da Compra"] = pd.to_datetime(data_frame["Data da Compra"])

col_index1, col_index2 = st.columns(2)
with col_index1:
    st.metric("Receitas", "R$ {:.2f}".format(data_frame["Preço"].sum()))

with col_index2:
    st.metric("Quantidade de Produtos", data_frame.shape[0])

tab1, tab2, tab3 = st.tabs(["Charts", "Table", "Sales"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        incomes = data_frame.groupby("Local da compra")["Preço"].sum()
        income_states = (
            data_frame.drop_duplicates(subset=["Local da compra"])[
                ["Local da compra", "lat", "lon"]
            ]
            .merge(incomes, left_on="Local da compra", right_index=True)
            .sort_values("Preço", ascending=False)
        )

        fig_income = px.scatter_geo(
            income_states,
            lat="lat",
            lon="lon",
            scope="south america",
            size="Preço",
            color="Preço",
            hover_name="Local da compra",
            hover_data={"lat": False, "lon": False},
            title="Receita por Local de Compra",
            size_max=50,
            template="seaborn",
        )
        st.plotly_chart(fig_income, use_container_width=True)

    with col2:
        income_month = (
            data_frame.set_index("Data da Compra")
            .groupby(pd.Grouper(freq="ME"))["Preço"]
            .sum()
            .reset_index()
        )
        income_month["Ano"] = income_month["Data da Compra"].dt.year
        income_month["Mês"] = income_month["Data da Compra"].dt.month_name()

        fig_income_month = px.line(
            income_month,
            x="Mês",
            y="Preço",
            color="Ano",
            markers=True,
            range_y=(0, income_month.max()),
            line_dash="Ano",
            template="seaborn",
            title="Receita por Mês",
        )
        fig_income_month.update_layout(yaxis_title="Receita (R$)")
        st.plotly_chart(fig_income_month, use_container_width=True)

    with col3:
        fig_income_states = px.bar(
            income_states.head(),
            x="Local da compra",
            y="Preço",
            text_auto="auto",
            title="Receita por Estados",
        )
        fig_income_states.update_layout(yaxis_title="Estados (R$)")
        st.plotly_chart(fig_income_states, use_container_width=True)

    with col4:
        income_category = (
            data_frame.groupby("Categoria do Produto")[["Preço"]]
            .sum()
            .sort_values("Preço", ascending=False)
        )

        fig_income_category = px.bar(
            income_category,
            text_auto="auto",
            title="Receita por Categoria",
        )

        fig_income_category.update_layout(yaxis_title="Categorias (R$)")
        st.plotly_chart(fig_income_category, use_container_width=True)

with tab2:
    st.dataframe(data_frame)

with tab3:
    st.write("Vendas")
    qt_seller = st.number_input("Quantidade de Vendedores", 2, 10, 5)
    col1, col2, col3 = st.columns(3)

    seller_incomes = data_frame.groupby("Vendedor")["Preço"].agg(["sum", "count"])
    seller_incomes_stage = data_frame.groupby("Local da compra")["Preço"].agg(
        ["sum", "count"]
    )
    with col1:
        pd_seller_incomes = pd.DataFrame(seller_incomes)
        st.metric("Receita", "R$ {:.2f}".format(pd_seller_incomes["sum"].sum()))
        fig_seller_incomes = px.bar(
            pd_seller_incomes[["sum"]]
            .sort_values("sum", ascending=True)
            .head(qt_seller),
            x="sum",
            y=pd_seller_incomes[["sum"]]
            .sort_values("sum", ascending=True)
            .head(qt_seller)
            .index,
            text_auto=True,
            title=f"Top {qt_seller} Vendedores por Receita",
        )
        st.plotly_chart(fig_seller_incomes, use_container_width=True)

    with col2:
        st.metric("Quantidade de Vendas", seller_incomes["count"].sum())
        fig_count_incomes = px.bar(
            seller_incomes[["count"]]
            .sort_values("count", ascending=True)
            .head(qt_seller),
            x="count",
            y=seller_incomes[["count"]]
            .sort_values("count", ascending=True)
            .head(qt_seller)
            .index,
            text_auto=True,
            title=f"Top {qt_seller} Vendedores por Quantidade de Vendas",
        )
        st.plotly_chart(fig_count_incomes, use_container_width=True)

    with col3:
        st.metric("Local de Vendas", seller_incomes_stage["count"].sum())
        fig_seller_incomes_stage = px.bar(
            seller_incomes_stage[["count"]]
            .sort_values("count", ascending=True)
            .head(qt_seller),
            x="count",
            y=seller_incomes_stage[["count"]]
            .sort_values("count", ascending=True)
            .head(qt_seller)
            .index,
            text_auto=True,
            title=f"Top {qt_seller} Local de Vendas",
        )
        st.plotly_chart(fig_seller_incomes_stage, use_container_width=True)
