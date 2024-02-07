import streamlit as st
from conexao import variavelYAML
import os

st.info("Essa página está sendo utilizada para a realização de testes no sistema. \n Ignore toda informação presente aqui!")

connect = variavelYAML()

st.write(connect)

env_variables = os.environ

# Itera sobre as variáveis de ambiente e imprime seus valores
for key, value in env_variables.items():
    st.write(f'{key}: {value}')