import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
from util import font_TITLE
from util import cardMyProject
from util import cardGRANDE
from collections import Counter
import mysql.connector 
import streamlit_authenticator as stauth


icone = Image.open('imagens/icone.png')
st.set_page_config(
    page_title="Meus Projetos",
    page_icon=icone,
    layout="wide")


#CONEXÃO COM O BANCO DE DADOS AWS
conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)

mat_gestor = 56126
mycursor = conexao.cursor()
comand = f"""SELECT 
    projeu_projetos.id_proj, 
    projeu_projetos.name_proj,
    (SELECT Nome FROM projeu_users WHERE id_user = projeu_projetos.gestor_id_fgkey) AS name_gestor, 
    (SELECT Matricula FROM projeu_users WHERE id_user = projeu_projetos.gestor_id_fgkey) AS matricula_gestor,
    (SELECT type_proj FROM projeu_type_proj WHERE id_type = projeu_projetos.type_proj_fgkey) AS type_proj,
    (SELECT macroprocesso FROM projeu_macropr WHERE id = projeu_projetos.macroproc_fgkey) AS macroprocesso,
    (SELECT nome_prog FROM projeu_programas WHERE id_prog = projeu_projetos.progrm_fgkey) AS programa,
    projeu_projetos.nome_mvp,
    projeu_projetos.investim_proj,
    projeu_projetos.objtv_projet as objetivo_projet,
    projeu_projetos.produto_entrega_final,
    (
        SELECT GROUP_CONCAT(number_sprint) 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as number_sprint,
    (
        SELECT GROUP_CONCAT(status_sprint) 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as status_sprint,
    (
        SELECT GROUP_CONCAT(date_inic_sp) 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as inic_sprint,
    (
        SELECT GROUP_CONCAT(date_fim_sp) 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as fim_sprint,
    (
        SELECT GROUP_CONCAT(status_homolog) 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as status_homolog_sprint,
    (
        SELECT GROUP_CONCAT(nome_Entrega) 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as entrega_name,
    (
        SELECT GROUP_CONCAT(executor) 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as executor_entrega,
    (
        SELECT GROUP_CONCAT(hra_necess) 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as hrs_entrega,
    (
        SELECT GROUP_CONCAT(compl_entrega) 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as complex_entreg,
    (
        SELECT GROUP_CONCAT(id_registro) 
        FROM projeu_registroequipe 
        WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
    ) as id_registro,
    (
        SELECT GROUP_CONCAT(Nome) 
        FROM projeu_users 
        WHERE id_user IN (
            SELECT id_colab 
            FROM projeu_registroequipe 
            WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
        )
    ) as colaborador,
    (
        SELECT GROUP_CONCAT(papel) 
        FROM projeu_registroequipe 
        WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
    ) as PAPEL,
    (
        SELECT 
            GROUP_CONCAT(Matricula) AS MATRICULA_EQUIPE
        FROM projeu_users AS PU
        INNER JOIN projeu_registroequipe AS PR ON PU.id_user = PR.id_colab 
        WHERE PR.id_projeto = projeu_projetos.id_proj
    ) as matriculaEQUIPE
FROM 
    projeu_projetos
GROUP BY
    projeu_projetos.id_proj;"""

mycursor.execute(comand)
ddPaging = mycursor.fetchall()

comandUSERS = 'SELECT * FROM projeu_users;'
mycursor.execute(comandUSERS)
dadosUser = mycursor.fetchall()
mycursor.close()

def tableRow():
    projeto = projetos
    mvp = mvps
    investimento = investimentos

    projetoCode = ""
    for i in range(len(projeto)):
        projetoCode += f"""<tr class="tdata1">
                <td>{projeto[i]}</td>
            </tr>"""

    mvpCode = ""
    for i in range(len(mvp)):
        mvpCode += f"""<tr class="tdata2">
                <td>{mvp[i]}</td>
            </tr>"""

    investimentoCode = ""
    for i in range(len(investimento)):
        investimentoCode += f"""<tr class="tdata3">
                <td>R${investimento[i]}</td>
            </tr>"""

    htmlRow = f"""<div class="flex-row">
            <div class="box">
                <div class="box1">
                    <table class="table1">
                        <tr class="thead1">
                            <th>Projeto<img src="https://cdn-icons-png.flaticon.com/128/10484/10484735.png" alt="Icone da tabela Projetos" class="table-icon"></th>
                        </tr>
                        <div>{projetoCode}</div>
                    </table>
                </div>
            </div>
            <div class="box">
                <div class="box2">
                    <table class="table2">
                        <tr class="thead2">
                            <th>MVP<img src="https://cdn-icons-png.flaticon.com/128/9238/9238294.png" alt="Icone da tabela MVPs" class="table-icon"></th>
                        </tr>
                        <div>{mvpCode}</div>
                    </table>
                </div>
            </div>
            <div class="box">
                <div class="box3">
                    <table class="table3">
                        <tr class="thead3">
                            <th>Investimento<img src="https://cdn-icons-png.flaticon.com/128/7928/7928255.png" alt="Icone da tabela Investimentos" class="table-icon"></th>
                        </tr>
                        <div>{investimentoCode}</div>
                    </table>
                </div>
            </div>
        </div>"""
    
    return htmlRow


def tableEqp():
    gestor = gestores
    especialista = especialistas
    squad = squads

    gestorCode = ""
    for i in range(len(gestor)):
        gestorCode += f"""<tr class="tdata4">
                <td>{gestor[i]}</td>
            </tr>"""

    especialistaCode = ""
    for i in range(len(especialista)):
        especialistaCode += f"""<tr class="tdata4">
                <td>{especialista[i]}</td>
            </tr>"""

    squadCode = ""
    for i in range(len(squad)):
        squadCode += f"""<tr class="tdata4">
                <td>{squad[i]}</td>
            </tr>"""

    htmlEqp = f"""
        <div class="box">
            <div class="box4">
                <table class="table4">
                    <tr class="thead4">
                        <th>Equipe<img src="https://cdn-icons-png.flaticon.com/128/5069/5069162.png" alt="Icone da tabela Equipe" class="table-icon"></th>
                    </tr>
                    <tr class="thead4-eqp">
                        <th><img src="https://cdn-icons-png.flaticon.com/128/3916/3916615.png" alt="Ícone do gestor para a tabela de Equipe" class="table-icon"> Gestor</th>
                    </tr>
                    <div>{gestorCode}</div>
                    <tr class="thead4-eqp">
                        <th><img src="https://cdn-icons-png.flaticon.com/128/9795/9795619.png" alt="Ícone do especialista para a tabela de Equipe" class="table-icon"> Especialista</th>
                    </tr>
                    <div>{especialistaCode}</div>
                    <tr class="thead4-eqp">
                        <th><img src="https://cdn-icons-png.flaticon.com/128/9856/9856655.png" alt="Ícone do squad para a tabela de Equipe" class="table-icon"> Squad</th>
                    </tr>
                    <div>{squadCode}</div>
                </table>
            </div>
        </div>
    """
    return htmlEqp

def tableUnic():
    entrega = entregas

    entregaCode = ""
    for i in range(len(entrega)):
        entregaCode += f"""<tr class="tdata5">
                <td>{entrega[i]}</td>
            </tr>"""

    htmlUnic = f"""
        <div class="box">
            <div class="box5">
                <table class="table5">
                    <tr class="thead5">
                        <th>Principais entregas<img src="https://cdn-icons-png.flaticon.com/128/10801/10801807.png" alt="Icone da tabela Principais entregas" class="table-icon"></th>
                    </tr>
                    <div>{entregaCode}</div>
                </table>
            </div>
        </div>
    """
    return htmlUnic

def tableCol():
    resultado = resultados
    metrica = metricas

    resultadoCode = ""
    for i in range(len(resultado)):
        resultadoCode += f"""<tr class="tdata6">
                <td>{resultado[i]}</td>
            </tr>"""
        
    metricaCode = ""
    for i in range(len(metrica)):
        metricaCode += f"""<tr class="tdata7">
                <td>{metrica[i]}</td>
            </tr>"""

    htmlCol = f"""
        <div class="flex-column">
            <div class="box">
                <div class="box6">
                    <table class="table6">
                        <tr class="thead6">
                            <th>Resultado esperado<img src="https://cdn-icons-png.flaticon.com/128/9797/9797853.png" alt="Icone da tabela Resultado esperado" class="table-icon"></th>
                        </tr>
                        <div>{resultadoCode}</div>
                    </table>
                </div>
            </div>
            <div class="box">
                <div class="box7">
                    <table class="table7">
                        <tr class="thead7">
                            <th>Métricas<img src="https://cdn-icons-png.flaticon.com/128/7931/7931125.png" alt="Icone da tabela Métricas" class="table-icon"></th>
                        </tr>
                        <div>{metricaCode}</div>
                    </table>
                </div>
            </div>
        </div>
    """
    return htmlCol

def tableGeral():
    dadosRow = tableRow()
    dadosEqp = tableEqp()
    dadosUnic = tableUnic()
    dadosCol = tableCol()

    htmlGeral = f"""
        <div class="flex-container">
            <div>{dadosRow}</div>
            <div class="flex-row">
                <div>{dadosEqp}</div>
                <div>{dadosUnic}</div>
                <div>{dadosCol}</div>
            </div>
        </div>
    """
    return htmlGeral

canvaStyle = """body{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #fff;
    }

    .box1,
    .box2,
    .box3,
    .box4,
    .box5,
    .box6,
    .box7{
        width: 100%;
        height: auto;
        max-width: 400px;
        max-height: 400px;
        overflow: auto;
        overflow-x: hidden;
        margin: 5px;
    }


    .box1:hover,
    .box2:hover,
    .box3:hover,
    .box4:hover,
    .box5:hover,
    .box6:hover,
    .box7:hover{
        transform: scale(0.98);
        border-radius: 20px;
    }

    .box1:hover{
        box-shadow: 0px 0px 25px rgba(74, 172, 252, 1);
    }

    .box2:hover{
        box-shadow: 0px 0px 25px rgba(255, 161, 189, 1);
    }

    .box3:hover{
        box-shadow: 0px 0px 25px rgba(255, 115, 84, 1);
    }

    .box4:hover{
        box-shadow: 0px 0px 25px rgba(73, 197, 57, 1);
    }

    .box5:hover{
        box-shadow: 0px 0px 25px rgba(141, 52, 135, 1);
    }

    .box6:hover{
        box-shadow: 0px 0px 25px rgba(255, 187, 78, 1);
    }

    .box7:hover{
        box-shadow: 0px 0px 25px rgba(255, 255, 68, 1);
    }

    .table1,
    .table2,
    .table3,
    .table4,
    .table5,
    .table6,
    .table7{
        width: 400px;
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden; 
    }

    .thead1{
        background-color: #4aacfc;
    }

    .thead2{
        background-color: #ffa1bd;
    }

    .thead3{
        background-color: #ff7354;
    }

    .thead4{
        background-color: #49c539;
    }

    .thead5{
        background-color: #8d348793;
    }

    .thead6{
        background-color: #ffbb4e;
    }

    .thead7{
        background-color: #ffff44;
    }

    .thead4-eqp{
        align-items: center;
        background-color: #b1ffa7;
        border-bottom: 1px solid #1eff00;
    }

    .thead1 th,
    .thead2 th,
    .thead3 th,
    .thead4 th,
    .thead5 th,
    .thead6 th,
    .thead7 th{
        text-align: center;
    }

    .thead4-eqp{
        text-align: center;
    }

    .thead1 img,
    .thead2 img,
    .thead3 img,
    .thead4 img,
    .thead5 img,
    .thead6 img,
    .thead7 img,
    .thead4-eqp img{
        vertical-align: middle;
        margin-left: 10px;
        width: 20px;
        height: auto;
    }

    .tdata1 td{
        border-top: 1px solid #008cff;
        background-color: #c8e6ff;
    }

    .tdata2 td{
        border-top: 1px solid #ffb7c9;
        background-color: #ffd8fd;
    }

    .tdata3 td{
        border-top: 1px solid #ff2600;
        background-color: #ffe1d7;
    }

    .tdata4 td{
        / border-top: 1px solid #1eff00; /
        background-color: #ccffc5;
    }

    .tdata5 td{
        border-top: 1px solid #96008c93;
        background-color: #e2cee193;
    }

    .tdata6 td{
        border-top: 1px solid #f3aa47;
        background-color: #fff7d5;
    }

    .tdata7 td{
        border-top: 1px solid #b3b301;
        background-color: #ffffc3;
    }

    .flex-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .flex-row {
        display: flex;
        justify-content: center;
        height: auto;
    }

    .flex-column {
        display: flex;
        flex-direction: column;
        height: auto;
        max-height: 100px;
        min-width: 400px;
    }"""


def mapear_dificuldade(dificuldade):
    if dificuldade == 'Fácil':
        return 'F'
    elif dificuldade == 'Médio':
        return 'M'
    elif dificuldade == 'Difícil':
        return 'D'
    else:
        return '---'  # Retornar None ou lançar um erro para outros valores


def string_to_datetime(string):
    date = datetime.strptime(str(string), "%Y-%m-%d").date()
    return date

names = [x[2] for x in dadosUser]
usernames = [x[3] for x in dadosUser]
hashed_passwords = [x[8] for x in dadosUser]

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
    with st.sidebar:
        authenticator.logout('Logout', 'main')

    matriUser = [x[1] for x in dadosUser if x[3] == username][0]
    ddPaging = [x for x in ddPaging if str(matriUser) in str(x[23]).split(',') or matriUser == x[3]]

    fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
    if len(ddPaging):
        font_TITLE('MEUS PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
        with st.expander('Filtro Projetos', expanded=False):
            macropr_filter = st.multiselect('Macroprocesso', set([x[5] for x in ddPaging]), set([x[5] for x in ddPaging]))
            program_filter = st.multiselect('Programas', set([x[6] for x in ddPaging if x[5] in macropr_filter]), set([x[6] for x in ddPaging if x[5] in macropr_filter]))
            project_filter = st.selectbox('Projetos', [x[1] for x in ddPaging if x[6] in program_filter])
            
            dadosOrigin = [x for x in ddPaging if x[1] == project_filter]
            cmd_entregas = f"""SELECT 
                                    (SELECT number_sprint FROM projeu_sprints WHERE id_sprint = projeu_entregas.id_sprint) AS NUMERO_SPRINT, 
                                    nome_Entrega AS NOME_ENTREGA, 
                                    (select Nome FROM projeu_users WHERE id_user = executor) AS EXECUTOR, 
                                    hra_necess AS HORAS, 
                                    compl_entrega AS COMPLEXIDADE,
                                    stt_entrega AS STATUS,
                                    id_entr,
                                    (SELECT Matricula FROM projeu_users WHERE id_user = executor) AS MATRICULA_EXECUTOR
                                FROM projeu_entregas 
                                    WHERE 
                                        id_sprint IN ( 
                                            SELECT id_sprint 
                                            FROM projeu_sprints 
                                            WHERE id_proj_fgkey = (
                                                SELECT id_proj 
                                                FROM projeu_projetos 
                                                WHERE name_proj = '{project_filter}'
                                                ) 
                                            );"""
            
        if len(dadosOrigin) > 0:
            mycursor = conexao.cursor()  
            mycursor.execute(cmd_entregas)
            EntregasBD = mycursor.fetchall()
            mycursor.close()

            ############CANVAS APRESENTANDO O PROJETO############
            font_TITLE('Canvas', fonte_Projeto,"'Bebas Neue', sans-serif", 40, 'left', '#228B22')
            projetos = [dadosOrigin[0][1]] if dadosOrigin[0][1] != "None" else " "
            mvps = [dadosOrigin[0][7]] if dadosOrigin[0][7] != "None" else " "
            investimentos = [f"{dadosOrigin[0][8]}"] if f"{dadosOrigin[0][8]}" != "None" else " "
            gestores = [f"{dadosOrigin[0][2]}"] if f"{dadosOrigin[0][2]}" != "None" else " "
            
            if dadosOrigin[0][21] != None:
                for i in range(len(dadosOrigin[0][21])): especialistas = f"{dadosOrigin[0][21]}".split(',') if f"{dadosOrigin[0][21]}" != "None" else " "
            else:
                especialistas = " "
            squads = [" "]
            equipe = [gestores, especialistas, squads]
            if dadosOrigin[0][16] != None:
                for i in range(len(dadosOrigin[0][16])): entregas = f"{dadosOrigin[0][16]}".split(',') if f"{dadosOrigin[0][16]}" != "None" else " "
            else:
                entregas = " "
            resultados = []
            for i in range(len(dadosOrigin)):
                if dadosOrigin[i][9] != None:
                    resultados.append(f"{dadosOrigin[i][9]}")
                else:
                    resultados = " "
            metricas = []
            for i in range(len(dadosOrigin)):
                if dadosOrigin[i][10] != None:
                    metricas.append(f"{dadosOrigin[i][10]}")
                else:
                    metricas = " "

            html = tableGeral()
            st.write(f'<div>{html}</div>', unsafe_allow_html=True)
            st.write(f'<style>{canvaStyle}</style>', unsafe_allow_html=True)

            #####APRESENTANDO HORAS TOTAIS GASTAS NO PROJETO DAQUELE COLABORADOR
            st.text(' ')
            st.text(' ')
            font_TITLE('MEU DESEMPENHO NO PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 40, 'left', '#228B22')

            dffMyProject = Counter([x[4] for x in EntregasBD if x[7] == matriUser]) if len(EntregasBD) > 0 else Counter(['-'])
            dif_comum = dffMyProject.most_common(1)
            complexidade = dif_comum[0][0]
            cardMyProject(f'{name}', [len([x for x in EntregasBD if x[7] == matriUser]), len([x for x in EntregasBD if str(x[5]).strip() == "🟩 Concluído" and x[7] == matriUser]), sum([x[3] for x in EntregasBD if x[7] == matriUser]), complexidade])
            ###APRESENTANDO DESEMPENHO POR SPRINT
            st.text(' ')
            st.text(' ')

            param_sprint = ['PRÉ MVP', 'MVP', 'PÓS MVP']
            font_TITLE('SPRINTS DO PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 40, 'left', '#228B22')
            with st.expander('Adcionar Sprint'):
                #FUNÇÃO PARA IDENTIFICAR SE A COLUNA DO BANCO DE DADOS ESTÁ VAZIA 
                func_split = lambda x: x.split(",") if x is not None else [x]
                maior_idx = max([param_sprint.index(x)+1 if x != None else 0 for x in func_split(dadosOrigin[0][12])])
                
                if None in func_split(dadosOrigin[0][11]):
                    on_ex = False
                else:    
                    on_ex = st.toggle('Excluir sprint')

                listAddSprOF_EX = [len([x for x in func_split(dadosOrigin[0][11]) if x != None]) + 1, param_sprint[:maior_idx+1], datetime.today()]
                listAddSprON_EX = [[int(x) if x != None else '' for x in func_split(dadosOrigin[0][11])], func_split(dadosOrigin[0][12]), [string_to_datetime(x) if x != None and x != " " else datetime.today() for x in func_split(dadosOrigin[0][13])]]

                disabledON = True if on_ex else False
                disabledOF = False if on_ex else True
                
                col0, col1, col2, col3 = st.columns([0.5,3,1,1])
                with col0:
                    number_sprint_new = st.text_input('Sprint', max(listAddSprON_EX[0]) if on_ex else listAddSprOF_EX[0], disabled=True)
                    number_sprint_new = int(number_sprint_new)
                with col1:
                    type_sprint_new = st.selectbox('Tipo', [listAddSprON_EX[1][listAddSprON_EX[0].index(number_sprint_new)]] if on_ex else listAddSprOF_EX[1], disabled=disabledON)
                with col2:
                    dat_inc_new = st.date_input('Início', value=listAddSprON_EX[2][listAddSprON_EX[0].index(number_sprint_new)] if on_ex else listAddSprOF_EX[2], disabled=disabledON)
                with col3:
                    dat_fim_new = st.date_input('Fim', value=dat_inc_new + timedelta(days=14), disabled=True)

                colAdd, colExc = st.columns([1,7])
                with colAdd:
                    button_addSprint = st.button('Adcionar Sprint', disabled=disabledON)
                with colExc:
                    button_exSprint = st.button('Excluir Sprint', disabled=disabledOF)
                
                if button_addSprint:
                    mycursor = conexao.cursor()
                    cmd_addSprint = f'''INSERT INTO projeu_sprints(number_sprint, id_proj_fgkey, status_sprint, date_inic_sp, date_fim_sp) 
                    VALUES ({number_sprint_new}, (SELECT id_proj FROM projeu_projetos WHERE name_proj = '{project_filter}'), '{type_sprint_new}', STR_TO_DATE('{dat_inc_new}', '%Y-%m-%d'), STR_TO_DATE('{dat_fim_new}', '%Y-%m-%d'));'''
                    mycursor.execute(cmd_addSprint)
                    
                    conexao.commit()
                    mycursor.close()
                    st.toast('Sucesso na adição da sprint!', icon='✅')
                    st.text(' ')

                if button_exSprint:
                    mycursor = conexao.cursor()
                    NoTentrg = False
                    if on_ex:
                        if len(EntregasBD) == 0:
                            NoTentrg = True
                        else:
                            NoTentrg = True if number_sprint_new not in list(set([x[0] for x in EntregasBD])) else False
                        
                        if NoTentrg:
                            cmdDEL = f'''DELETE FROM projeu_sprints 
                                        WHERE number_sprint = {number_sprint_new} 
                                        AND id_proj_fgkey = (SELECT id_proj FROM projeu_projetos 
                                            WHERE name_proj = '{project_filter}') 
                                        AND status_sprint = '{type_sprint_new}'
                                        AND date_inic_sp = STR_TO_DATE('{dat_inc_new}', '%Y-%m-%d')
                                        AND date_fim_sp = STR_TO_DATE('{dat_fim_new}', '%Y-%m-%d');'''                

                            mycursor.execute(cmdDEL)
                            conexao.commit()

                            mycursor.close()
                            st.toast('Excluido!', icon='✅') 
                        else:
                            st.toast('Primeiramente, é necessário excluir todas as atividades dessa sprint.', icon='❌')
                    else:
                        st.toast('Primeiramente, ative a opção de excluir sprint.', icon='❌')

            if func_split(dadosOrigin[0][11])[0] != None:
                # ----> DADOS [NUMBER_SPRINT, STATUS_SPRINT,  DATA INC SPRINT, DATA FIM SPRINT]
                sprints = [[func_split(dadosOrigin[0][11])[x], param_sprint.index(func_split(dadosOrigin[0][12])[x]), func_split(dadosOrigin[0][13])[x], func_split(dadosOrigin[0][14])[x]] for x in range(len(func_split(dadosOrigin[0][11])))]
                
                for idx_parm in range(len(param_sprint)):
                    ddSprint = [sprints[x] for x in range(len(sprints)) if str(sprints[x][1]) == str(idx_parm)] #DESCOBRINDO QUAL A SPRINT DAQUELE STATUS
                    #FUNÇÃO PARA LIMPAR AS ENTREGAS DAQUELA SPRINT 
                    # ----> DADOS [NUMBER_SPRINT, NOME_ENTREGA, EXECUTOR, HORAS, COMPLEXIDADE, STATUS]
                    SpritNotEntreg = [[int(sprt), None, None, 0 , '---', '🟨 Backlog', None] for sprt in [i[0] for i in ddSprint] if sprt not in list(set([ab_x[0] for ab_x in EntregasBD]))]
                    
                    SprintsEntregs = [list(x) for x in EntregasBD if str(x[0]) in [str(i[0]) for i in ddSprint]]
                    
                    SprintsEntregs.extend(SpritNotEntreg)
                    if len(ddSprint)> 0:
                        font_TITLE(f'{param_sprint[idx_parm]}', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')

                        for idx_spr in list(set([x[0] for x in SprintsEntregs])):
                            listDadosAux = []
                            with st.expander(f'Sprint {idx_spr}'):
                                #FILTRANDO ENTREGAS DAQUELA SPRINT
                                spEntregas = [x for x in SprintsEntregs if x[0] == idx_spr]
                                contagem_dif = Counter([x[4] for x in spEntregas])                
                                dif_comum = contagem_dif.most_common(1)

                                cardGRANDE(['Colaboradores', 'Atividades', 'Entregues', 'Avanço', 'Horas', 'Complexidade'], [len([x for x in spEntregas if x[2] != None]), len([x for x in spEntregas if x[1] != None]), len([x for x in spEntregas if str(x[5]).strip() == '🟩 Concluído']), '0%', sum([x[3] for x in spEntregas]), mapear_dificuldade(dif_comum[0][0])])
                                st.text(' ')
                                st.text(' ')

                                col1, col2, col3 = st.columns([3,1,1])
                                with col1:
                                    st.text(' ')
                                    font_TITLE('ATIVIDADES', fonte_Projeto,"'Bebas Neue', sans-serif", 40, 'left','#228B22')

                                with col2:
                                    st.caption('Status Sprint') 
                                    font_TITLE('Executando', fonte_Projeto,"'Bebas Neue', sans-serif", 27, 'left')#MUDAR DE ACORDO COM AS ATIVIDADES DA SPRINT - SE TODOAS AS ATIVIDADES ESTIVEREM COMPLETA A SPRINT ESTÁ CONCLUIDA - [Concluída, Executando, Backlog, Atrasada]
                                
                                st.text(' ')
                                tab1, tab2 = st.tabs(['Atualizar Entregas', 'Excluir Entregas'])
                                with tab1:
                                    #FORMULÁRIO APRESENTANDO AS ENTREGAS
                                    col1, col2, col3 = st.columns([3,1,1])
                                    qnt_att = st.number_input('Adcionar Atividade', min_value=0, step=1, key=f'add{idx_spr} - {idx_parm}')
                                    
                                    spEntregas.extend([[idx_spr, None, None, 0 , '---', '🟨 Backlog', None] for x in range(qnt_att)])

                                    st.text(' ')
                                    col0, col1, col2, col3, col4, col5 = st.columns([0.13, 1, 0.3, 0.25, 0.25, 0.2])
                                    with col0:
                                        st.caption('ID')
                                    with col1:
                                        st.caption('Atividades')
                                    with col2:
                                        st.caption('Status')
                                    with col3:
                                        st.caption('Executor')
                                    with col4:
                                        st.caption('Hrs Neces')
                                    with col5:
                                        st.caption('Compl')

                                    for ativIDX in range(len(spEntregas)): 
                                        with col0:
                                            id_entreg = st.text_input('id', key=f'id_entrega{idx_spr} - {ativIDX} - {idx_parm}', label_visibility="collapsed")                   
                                        with col1:
                                            name_entreg = st.text_input('Atividade', spEntregas[ativIDX][1] if spEntregas[ativIDX][1] != None else '', key=f'atividade{idx_spr} - {ativIDX} - {idx_parm}', label_visibility="collapsed")
                                        with col4:
                                            horas_entreg = st.number_input('Horas', value=spEntregas[ativIDX][3],min_value=0, step=1, key=f'horas{idx_spr} - {ativIDX} - {idx_parm}', label_visibility="collapsed")
                                        with col3:
                                            opc_colb = func_split(dadosOrigin[0][21])
                                            colab_entreg = st.selectbox('Colaborador', opc_colb, opc_colb.index(spEntregas[ativIDX][2]) if spEntregas[ativIDX][2] != None and spEntregas[ativIDX][2] != '' else 0, key=f'colab{idx_spr} - {ativIDX} - {idx_parm}', label_visibility="collapsed")
                                        with col2:
                                            opc_stt = ['🟨 Backlog', '🟥 Impeditivo', '🟦 Executando',  '🟩 Concluído']
                                            status_entreg = st.selectbox('Status', opc_stt, opc_stt.index(str(spEntregas[ativIDX][5]).strip()) if spEntregas[ativIDX][5] != None and spEntregas[ativIDX][5] != '' else 0, key=f'status{idx_spr}  - {idx_parm} - {ativIDX}', label_visibility="collapsed")
                                        with col5:
                                            opc_compl = ['Fácil', 'Médio', 'Difícil']
                                            compl_entreg = st.selectbox('Compl.', opc_compl, opc_compl.index(spEntregas[ativIDX][4]) if spEntregas[ativIDX][4] != None and spEntregas[ativIDX][4] != '---' else 0, key=f'complex{idx_spr}  - {idx_parm}- {ativIDX}', label_visibility="collapsed")

                                        listDadosAux.append([name_entreg, colab_entreg, horas_entreg, status_entreg, compl_entreg, spEntregas[ativIDX][6]]) 
                                    button_atual = st.button('Atualizar', key=f'{idx_spr} {idx_parm}')        
                                    if button_atual:
                                        mycursor = conexao.cursor()
                                        for list_atual in listDadosAux:
                                            if list_atual[5] != None: #SE A ENTREGA DA "list_atual" JÁ ESTIVER DENTRO DO BANCO DE DADOS SOMENTE VAI ATUALIZAR AS INFORMAÇÕES SOBRE A ENTREGA
                                                columnsUP = ['nome_Entrega', 'executor', 'hra_necess', 'stt_entrega', 'compl_entrega']
                                                
                                                for idxColum in range(len(columnsUP)):
                                                    cmd_update = f'''UPDATE projeu_entregas SET {columnsUP[idxColum]} = {f"'{list_atual[idxColum]}'" if idxColum != 1 else f"(SELECT id_user FROM projeu_users WHERE Nome = '{list_atual[idxColum]}' LIMIT 1)"} WHERE id_entr = {list_atual[5]};'''
                                                    mycursor.execute(cmd_update)
                                                    conexao.commit()
                                                
                                            else: #INSERT DA ENTREGA CASO ELA NÃO ESTEJA PRESENTE DENTRO DO BANCO DE DADOS
                                                if list_atual[0] != None and list_atual[0] != '': 
                                                    cmd_insert = f"""
                                                        INSERT INTO projeu_entregas (id_sprint, nome_Entrega, executor, hra_necess, stt_entrega, compl_entrega) 
                                                            values((SELECT id_sprint FROM projeu_sprints WHERE number_sprint = {spEntregas[0][0]}  
                                                                AND id_proj_fgkey = 
                                                                    (SELECT id_proj FROM projeu_projetos WHERE name_proj = '{dadosOrigin[0][1]}') LIMIT 1),
                                                                    '{list_atual[0]}', 
                                                                    (SELECT id_user FROM projeu_users WHERE Nome = '{list_atual[1]}' LIMIT 1),
                                                                    {list_atual[2]},
                                                                    '{list_atual[3]}',
                                                                    '{list_atual[4]}');"""
                                                    mycursor.execute(cmd_insert)
                                                    conexao.commit()
                                        mycursor.close()
                                        st.toast('Dados Atualizados!', icon='✅')

                                with tab2:
                                    font_TITLE('EXCLUIR', fonte_Projeto,"'Bebas Neue', sans-serif", 23, 'left')  
                                    atvdd_exc = st.selectbox('Atividade', [x[1] for x in spEntregas if x[1] != None and x[1] != ' '], key=f'NameExAtivid {idx_spr} - {idx_parm}')

                                    col_sel0, col_sel1, col_sel2, col_sel3 = st.columns([3,1,1,1])
                                    with col_sel0:
                                        exec_exc = st.text_input('Executor', value=f'{[x[2] for x in spEntregas if x[1] == atvdd_exc][0]}', disabled=True, key=f'ExcutExAtivid {idx_spr} - {idx_parm}')
                                    with col_sel1:
                                        compl_exc = st.text_input('Complexidade', value=[x[4] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'ComplexidadeExAtivid {idx_spr} - {idx_parm}')
                                    with col_sel2:
                                        hrs_exc = st.text_input('Horas', value=[x[3] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'HorsExAtivid {idx_spr} - {idx_parm}')
                                    with col_sel3:
                                        stt_exc = st.text_input('Status', value=[x[5] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'StatusExAtivid {idx_spr} - {idx_parm}')
                                    buttonEX = st.button('Excluir', key=f'Excluir{idx_spr} - {idx_parm}')

                                    if buttonEX: 
                                        mycursor = conexao.cursor()
                                        cmd_exc = f"""DELETE FROM projeu_entregas 
                                                    WHERE 
                                                        id_sprint = (SELECT id_sprint FROM projeu_sprints WHERE number_sprint = {idx_spr} LIMIT 1) 
                                                        AND nome_entrega = '{atvdd_exc}' 
                                                        AND executor = (SELECT id_user FROM projeu_users WHERE Nome = '{exec_exc}' LIMIT 1)
                                                        AND compl_entrega = '{compl_exc}'
                                                        AND stt_entrega = '{stt_exc}';"""
                                        mycursor.execute(cmd_exc)
                                        conexao.commit()

                                        st.toast('Entrega Excluida!', icon='✅')
                                        mycursor.close()
    else:
        st.text(' ')
        st.text(' ')
        font_TITLE(f'AINDA NÃO HÁ PROJETOS VINCULADOS A VOCÊ!! ⏳', fonte_Projeto,"'Bebas Neue', sans-serif", 22, 'center')
