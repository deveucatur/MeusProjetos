import streamlit as st
from conexao import variavelYAML
import os

connect = variavelYAML()

st.write(connect)

print("Conteúdo de os.environ:")
print(os.environ)

# Itera sobre as variáveis de ambiente e imprime seus valores
for key, value in os.environ.items():
    print(f'{key}: {value}')
