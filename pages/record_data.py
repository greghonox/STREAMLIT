import streamlit as st
from main import load_data, clear_cache


with st.form(key="my_form"):
    st.title("Cadastro de vendas")
    inx = load_data().shape[0] + 1
    lat, lon = -13.29, -41.71
    sales = st.selectbox("Vendedor", load_data()["Vendedor"].unique())
    local = st.selectbox("Local da compra", load_data()["Local da compra"].unique())
    product = st.selectbox("Produto", load_data()["Produto"].unique())
    category = st.selectbox(
        "Categoria do Produto", load_data()["Categoria do Produto"].unique()
    )
    date = st.date_input("Data da Compra")
    type_pay = st.selectbox(
        "Tipo de pagamento", load_data()["Tipo de pagamento"].unique()
    )
    tax = st.number_input("Frete", min_value=1.0)
    price = st.number_input("Preço", min_value=1.0)
    quantity = st.number_input("Quantidade", min_value=1)
    score = st.number_input("Nota de atendimento", min_value=1, max_value=5)

    def record_sales():
        with open("resources/2024-07-27T23-35_export.csv", "a") as file:
            text = [
                inx,
                product,
                category,
                price,
                tax,
                date.strftime("%Y-%m-%dT00:00:00.000"),
                sales,
                local,
                type_pay,
                quantity,
                score,
                lat,
                lon,
            ]
            txt = ",".join([str(t) for t in text])
            file.write(txt + "\n")
            clear_cache()
            load_data()
            st.success("Venda registrada com sucesso!")

    st.form_submit_button(
        label="Registrar vendas",
        help="Depois de preenchido clique aqui para cadastrar no banco",
        on_click=record_sales,
    )
