import streamlit as st
import mysql.connector

# Abra o arquivo para leitura
with open('conexao.txt', 'r') as arquivo:
    # Leia todas as linhas do arquivo
    linhas = arquivo.readlines()

# Inicialize um dicionário para armazenar as variáveis
variaveis = {}

# Itere sobre as linhas
for linha in linhas:
    # Divida a linha em partes usando o sinal de igual como separador
    partes = linha.strip().split('=')
    # Atribua a variável ao dicionário
    variaveis[partes[0]] = partes[1]

# Agora você pode acessar as variáveis como desejado
# print("Nome:", variaveis['nome'])
# print("Idade:", variaveis['idade'])
# print("Cidade:", variaveis['cidade'])
    
conexao = mysql.connector.connect(
    passwd=variaveis['DB_PASSWORD'],
    port=variaveis['DB_PORT'],
    user=variaveis['DB_USER'],
    host=variaveis['DB_HOST'],
    database=variaveis['DB_DATABASE']
)

st.write(conexao)

# from conexao import variavelYAML
# import os
# from dotenv import load_dotenv

# load_dotenv()

# st.info("Essa página está sendo utilizada para a realização de testes no sistema. \n\n Ignore toda informação presente aqui!")

# connect = variavelYAML()

# st.write(connect)

# env_variables = os.environ

# # Itera sobre as variáveis de ambiente e imprime seus valores
# for key, value in env_variables.items():
#     st.write(f'{key}: {value}')