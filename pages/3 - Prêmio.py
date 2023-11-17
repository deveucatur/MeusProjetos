import streamlit as st
from util import font_TITLE
from PIL import Image
import mysql.connector
from datetime import datetime, timedelta
import streamlit_authenticator as stauth
from utilR import menuProjeuHtml, menuProjeuCss

icone = Image.open('imagens/icone.png')
st.set_page_config(
    page_title="Meus Prêmio",
    page_icon=icone,
    layout="wide")

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
    )

mycursor = conexao.cursor()

def premios_user_bd(matricula):
    mycursor = conexao.cursor() 
    mycursor.execute(f"""
    SELECT 
        PS.id_sprint,
        PS.number_sprint,
        PS.date_inic_sp,
        PS.date_fim_sp,
        PP.name_proj,
        PE.nome_Entrega,
        PU.Matricula,
        PU.Nome,
        PPE.funcao_premio as FUNCAO_PREMIO,
        PE.hra_necess as HORAS_NECESSÁRIAS,
        PPE.hrs_normalizadas AS HORAS_NORMALIZADAS,
        PPE.dificuldade,
        PPE.valor,
        PS.check_aprov,
        PU.email_pj,
        (
            SELECT 
                nome_empresa 
            FROM 
                projeu_empresas AS PEM 
            WHERE id_empresa = PU.empresa_fgkey
        ) AS NAME_EMPRESA,
        (
            SELECT 
                number_empresa
            FROM 
                projeu_empresas AS PEM 
            WHERE id_empresa = PU.empresa_fgkey
        ) AS NUMBER_EMPRESA
    FROM projeu_premio_entr AS PPE
    LEFT JOIN 
        projeu_sprints PS ON PS.id_sprint = PPE.id_sprint_fgkey
    LEFT JOIN 
        projeu_users PU ON PU.id_user = PPE.bonificado_fgkey
    LEFT OUTER JOIN 
        projeu_entregas PE ON PE.id_entr = PPE.id_entreg_fgkey
    LEFT JOIN 
        projeu_projetos PP ON PP.id_proj = PS.id_proj_fgkey
    WHERE 
        PPE.bonificado_fgkey = (SELECT id_user FROM projeu_users WHERE Matricula = {str(matricula).strip()})
        AND
            PS.check_consolid = 1 OR PS.check_consolid IS NULL
    GROUP BY PPE.id_premio;""")
    premiosbd = mycursor.fetchall()
    mycursor.close()

    return premiosbd

def cardImg(image_url):
    st.markdown(
        f"""
        <style>
        .caixa {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #FFFFFF;
            color: white;
            font-family: ;
            padding: 12px 35px;
            text-align: center;
            text-decoration: none;
            font-size: 15px;
            border-radius: 10px;
            border: 1px solid #ccc; /* Adiciona uma borda de 1px sólida */
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2); /* Adiciona sombreamento */
            transition: background-color 0.3s ease;
        }}
        .botao-imagem {{
            height: 50px;
            width: 50px;
            margin-bottom: 10px;
        }}            
        </style>

        <div target="_self" class="caixa">
            <img src="{image_url}" class="botao-imagem">
        </div>
        """,
        unsafe_allow_html=True
    )

def complexidade_name(number):
    aux = {1: 'Fácil',
           2: 'Médio',
           3: 'Difícil'}
    
    return aux[number]


meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]


def meses_by_number(mes):
    meses_do_ano = {
            "Janeiro":12,
            "Fevereiro":1,
            "Março":2,
            "Abril":3,
            "Maio":4,
            "Junho":5,
            "Julho":6,
            "Agosto":7,
            "Setembro":8,
            "Outubro":9,
            "Novembro":10,
            "Dezembro":11
        }
    return meses_do_ano[mes]

comandUSERS = 'SELECT * FROM projeu_users;'
mycursor.execute(comandUSERS)
dadosUser = mycursor.fetchall()
mycursor.close()

names = [x[2] for x in dadosUser]
usernames = [x[3] for x in dadosUser]
hashed_passwords = [x[7] for x in dadosUser]

menuHtml = menuProjeuHtml()
menuCss = menuProjeuCss()
st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

def convert_to_dict(names, usernames, passwords):
    credentials = {"usernames": {}}
    for name, username, password in zip(names, usernames, passwords):
        user_credentials = {
            "email":username,
            "name": name,
            "password": password
        }
        credentials["usernames"][username] = user_credentials
    return credentials

credentials = convert_to_dict(names, usernames, hashed_passwords)
authenticator = stauth.Authenticate(credentials, "Teste", "abcde", 30)

col1, col2,col3 = st.columns([1,3,1])
with col2:
    name, authentication_status, username = authenticator.login('Acesse o sistema PROJEU', 'main')

if authentication_status == False:
    with col2:
        st.error('Email ou Senha Incorreto')
elif authentication_status == None:
    with col2:
        st.warning('Insira seu Email e Senha')
elif authentication_status:

    fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
    font_TITLE('MEUS PRÊMIOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
    
    matriUser = [x[1] for x in dadosUser if x[3] == username][0]
    premiosbd = premios_user_bd(matriUser)
    with st.expander('Filtro'):
        projetos = list(set([x[4] for x in premiosbd]))
        projetos.append('TODOS')
        user_project = st.selectbox('Projeto', projetos, projetos.index('TODOS'))
        if user_project == 'TODOS':
            user_project = [str(x).strip() for x in projetos if x != 'TODOS']
        else:
            user_project = [user_project]

        mes_atual = datetime.now()
        mes_project = st.selectbox('Período', meses, mes_atual.month)
        
        data_final = datetime(mes_atual.year, meses_by_number(mes_project), 25)                    
        data_inicial = datetime(int(mes_atual.year), meses_by_number(mes_project)-1, 26)
        
        range_datas = []
        data_atual = data_inicial
        while data_atual <= data_final:
            range_datas.append(data_atual)
            data_atual += timedelta(days=1)    

        premiosuser = [x for x in premiosbd if str(x[4]).strip().lower() in [str(x).strip().lower() for x in list(user_project)] and datetime.strptime(str(x[3]), "%Y-%m-%d") in range_datas] 

    if len(premiosuser) > 0:
        st.text(' ')
        col1, col2 = st.columns([1, 3])

        with col1:
            font_TITLE('DESEMPENHO MENSAL', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')

            image_url=  r"https://th.bing.com/th/id/R.5bef3f83aa5b90c7913386dde6143553?rik=vpAUUjGY9Rl50w&riu=http%3a%2f%2finterpacificoltda.hostdataset.com%2fipexports%2fppa%2fimg%2fUsuario.png&ehk=7QiNoqM5sO%2fJhX8rNRTAoWxozQEWhPz8xCZ7L7evY9s%3d&risl=&pid=ImgRaw&r=0"
            cardImg(image_url)
            st.markdown(f'{premiosuser[0][7]}')

        with col2:    
            st.text(' ')
            col1, col2, col3, col4, col5 = st.columns([0.6,1,1,1,1])
            with col2:
                font_TITLE('PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
                font_TITLE(f'{len(set([x[4] for x in premiosuser]))}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')
            with col3:
                font_TITLE('ATIVIDADES', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
                font_TITLE(f'{len(premiosuser)}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')
            with col4:
                font_TITLE('HORAS', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
                font_TITLE(f'{sum([x[9] if x[9] != None else 0 for x in premiosuser])}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')
            with col5:
                font_TITLE('BONIFICAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
                font_TITLE(f'R${round(sum([x[12] for x in premiosuser]), 2)}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')

        st.text(' ')
        st.text(' ')
        st.text(' ')
        st.divider()
        font_TITLE('RELATÓRIO TAREFAS MENSAIS', fonte_Projeto,"'Bebas Neue', sans-serif", 45, 'left')
        for name_proj in list(set([str(x[4]).strip() for x in premiosuser])):
            tarefas_do_project = [x for x in premiosuser if str(x[4]).strip() == name_proj] 
            font_TITLE(f'{name_proj}', fonte_Projeto,"'Bebas Neue', sans-serif", 22, 'left')
            
            col1, col2, col3, col4, col5 = st.columns([2,0.5,0.4,0.4,0.4])
            with col1:
                st.caption('Atividade')
            with col2:
                st.caption('Sprint')
            with col3:
                st.caption('Horas')
            with col4:
                st.caption('Compl.')
            with col5:
                st.caption('Valor')

            for name_entrg in tarefas_do_project:
                with col1:
                    st.text_input('Atividade', name_entrg[5] if name_entrg[5] != '' and name_entrg[5] != None else 'Gestor/Especialista', key=f'atividade{name_proj} - {name_entrg}', label_visibility="collapsed")
                with col2:
                    st.text_input('Sprint', name_entrg[1], key=f'sprint{name_proj} - {name_entrg}', label_visibility="collapsed")
                with col3:
                    st.text_input('Horas', f'{name_entrg[9] if name_entrg[9] != None else 0} hrs', key=f'horas{name_proj} - {name_entrg}', label_visibility="collapsed")
                with col4:
                    st.text_input('Compl.', complexidade_name(name_entrg[11]) if name_entrg[11] != None else '', key=f'complex{name_proj} - {name_entrg}', label_visibility="collapsed")
                with col5:
                    st.text_input('Valor', f'R$ {name_entrg[12]}', key=f'valor{name_proj} - {name_entrg}', label_visibility="collapsed")