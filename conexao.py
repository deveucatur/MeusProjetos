import os
import mysql.connector

def conexaoBD():
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_database = os.environ.get('DB_DATABASE')

    conexao = mysql.connector.connect(
        user=db_user,
        passwd=db_password,
        host=db_host,
        port=db_port,
        database=db_database
    )

    return conexao