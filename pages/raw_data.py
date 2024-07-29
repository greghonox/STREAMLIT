import streamlit as st
from main import load_data

data_frame = load_data()
columns = data_frame.columns.unique()

with st.expander("Selecione as colunas"):
    columns_selected = st.multiselect("", list(columns), list(columns))
    if len(columns_selected) == 0:
        columns_selected = ["Produto"]
        st.toast(":red[Não é possivel ficar sem colunas!!!]", icon="🔥")

data_frame_column_selected = data_frame[columns_selected]
st.dataframe(data_frame_column_selected)
st.markdown(
    f"### Quantidade de colunas selecionadas: :blue[{len(columns_selected)}] e linhas :red[{data_frame.shape[0]}]"
)
