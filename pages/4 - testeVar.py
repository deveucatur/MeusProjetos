import streamlit as st
import os
import yaml
import re
import sys

yaml_code = """
coloque o seu YAML aqui
"""

secrets = {
    'DB_USER': 'valor_secreto_user',
    'DB_PASSWORD': 'valor_secreto_password',
    'DB_HOST': 'valor_secreto_host',
    'DB_PORT': 'valor_secreto_port',
    'DB_DATABASE': 'valor_secreto_database',
}

for key, value in secrets.items():
    yaml_code = re.sub(fr'\${{{{\s+secrets.{key}\s+}}}}', value, yaml_code)

st.write(yaml_code)

#===========================================================================

# def ler_configuracoes(nome_arquivo):
#     with open(nome_arquivo, 'r') as arquivo:
#         configuracoes = yaml.safe_load(arquivo)
#     return configuracoes

# # Caminho do arquivo YAML
# caminho_arquivo_yaml = '.github/workflows/main.yaml'

# # Lê as variáveis do arquivo YAML
# config = ler_configuracoes(caminho_arquivo_yaml)

# st.write(config)

#==========================================================================

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
