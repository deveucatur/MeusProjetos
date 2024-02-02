import os
import mysql.connector
import streamlit as st

def variavelYAML():
    db_user = os.environ.get('HOSTNAME')
    db_password = os.environ.get('USER')
    db_host = os.environ.get('HOME')
    db_port = os.environ.get('SF_PARTNER')
    db_database = os.environ.get('STREAMLIT_SERVER_RUN_ON_SAVE')

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