import streamlit as st
import os
import yaml

def ler_configuracoes(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        configuracoes = yaml.safe_load(arquivo)
    return configuracoes

# Caminho do arquivo YAML
caminho_arquivo_yaml = '.github/workflows/main.yaml'

# Lê as variáveis do arquivo YAML
config = ler_configuracoes(caminho_arquivo_yaml)

st.write(config)

# db_user = os.environ.get('$DB_USER')
# db_password = os.environ.get('$DB_PASSWORD')
# db_host = os.environ.get('$DB_HOST')
# db_port = os.environ.get('$DB_PORT')
# db_database = os.environ.get('$DB_DATABASE')

# st.write("teste - 3.0")
# st.info(db_user)
# st.info(db_password)
# st.info(db_host)
# st.info(db_port)
# st.info(db_database)
