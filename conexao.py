import os
import mysql.connector
import streamlit as st

def variavelYAML():
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_database = os.environ.get('DB_DATABASE')

    return [db_user, db_password, db_host, db_port, db_database]

def conexaoBD():
    conexao = mysql.connector.connect(
        passwd='nineboxeucatur',
        port=3306,
        user='ninebox',
        host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
        database='projeu'
    )

    return conexao