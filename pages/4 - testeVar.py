import streamlit as st
from conexao import variavelYAML
import os

connect = variavelYAML()

st.write(connect)

st.write("Conteúdo de os.environ:")
st.write(os.environ)

# Itera sobre as variáveis de ambiente e imprime seus valores
for key, value in os.environ.items():
    st.write(f'{key}: {value}')
