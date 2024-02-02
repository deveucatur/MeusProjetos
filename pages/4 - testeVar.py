import streamlit as st
from conexao import variavelYAML
import os

connect = variavelYAML()

st.write(connect)

env_variables = os.environ

# Itera sobre as variáveis de ambiente e imprime seus valores
for key, value in env_variables.items():
    print(f'{key}: {value}')