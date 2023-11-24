import streamlit as st
from PIL import Image
from utilR import font_TITLE, ninebox_home, css_9box_home, nineboxDatasUnidades_home
from time import sleep
import mysql.connector 
import streamlit_authenticator as stauth
from utilR import menuProjeuHtml, menuProjeuCss

st.set_page_config(layout="wide",
    initial_sidebar_state='collapsed')

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)

def cardMyProject(nome_user, dados_user):
    param = ['Atividades', 'Entregues', 'Horas Total', 'Complexidade']
    css = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    
    .card {
        font-family: Poppins, sans-serif;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 13px;
        width: 100%;
        margin: 20px auto;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%; 
    }

    .linha1 {
        font-size: 30px;
        text-align: left;
        margin-bottom: 10px;
    }

    .titulos2 {
        font-size: 12px;
        opacity: 60%
    }

    p {
        margin: 0%;
    }

    .linha2 {
        display: flex;
    }

    .coluna {
        flex: 1;
        background-color:#ffffff;
        padding: 0%;
    }
    .coluna p{
        font-size: 29px;    
    }
    '''

    html = f'''
    <body>
        <div class="card">
            <div class="linha1">
            <p style="font-size: 12px; opacity: 60%;">Nome</p>
            {nome_user}
            </div>
            <div class="linha2">'''
    
    for a in range(len(param)):
        html += f"""
                <div class="coluna">
                    <div class="titulos2">{param[a]}</div>
                    <p>{dados_user[a]}</p>
                </div>"""

    html += ''' 
            </div>
        </div>
    </body>'''    

    st.write(f'<style>{css}</style>', unsafe_allow_html=True)
    st.write(html, unsafe_allow_html=True)
        
def botao1(nomeBotao, link, image_path):
    st.markdown(
        f"""
        <style>
        .botao-estiloso {{
            text-decoration: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #fff;
            padding: 12px 35px;
            text-align: center;
            font-size: 15px;
            border-radius: 10px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            max-width: 100%;
            border-radius: 20px;
            transition: background-color 0.5s ease;
        }}
        .botao-estiloso:hover {{
            background: linear-gradient(to bottom, #9fdafc, #bae6ff, #dbf2fe);
            border-radius: 20px;
        }}
        .botao-imagem {{
            height: 50px;
            width: 50px;
            margin-bottom: 10px;
        }}

        .botao-texto {{
            font-weight: bold;
            color: black;
        }}
            
        </style>
        <a href="{link}" target="_self" class="botao-estiloso" style="color: inherit; text-decoration: none;">
            <img src="{image_path}" class="botao-imagem">
            <span class="botao-texto">{nomeBotao}</span>
        </a>
        """,
        unsafe_allow_html=True
    )


fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
'''

mycursor = conexao.cursor()

sqlProjetoLider = f"""SELECT p.name_proj, p.id_proj FROM projeu_projetos p JOIN projeu_complexidade c ON p.id_proj = c.proj_fgkey WHERE c.check_lider IS NULL OR c.check_lider = '' GROUP BY p.id_proj;"""
mycursor.execute(sqlProjetoLider)
projetoNomeLider = mycursor.fetchall()

sqlProjetoGover = f"""SELECT p.name_proj, p.id_proj FROM projeu_projetos p JOIN projeu_complexidade c ON p.id_proj = c.proj_fgkey WHERE c.check_govern IS NULL OR c.check_govern = '' GROUP BY p.id_proj;"""
mycursor.execute(sqlProjetoGover)
projetoNomeGover = mycursor.fetchall()

sqlCanva = f"""SELECT 
	id_proj, 
	name_proj, 
    produto_entrega_final, 
    nome_mvp, produto_mvp, 
    (
		SELECT 
			GROUP_CONCAT(name_metric) 
		FROM projeu_metricas 
        WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS metricas, 
    result_esperad, 
    (
        SELECT 
            GROUP_CONCAT(Nome) 
        FROM projeu_users 
        WHERE id_user IN (
                            SELECT 
                                id_colab 
                            FROM 
                                projeu_registroequipe 
                            WHERE 
                                projeu_registroequipe.id_projeto = projeu_projetos.id_proj)
    ) AS colaborador, 
    (
        SELECT 
            GROUP_CONCAT(papel) 
        FROM 
            projeu_registroequipe 
        WHERE 
            projeu_registroequipe.id_projeto = projeu_projetos.id_proj
    ) AS papel, 
    (
        SELECT 
            GROUP_CONCAT(entreg) 
        FROM 
            projeu_princEntregas 
        WHERE id_proj_fgkey = projeu_projetos.id_proj
    ) AS entregas,
    investim_proj,
    PM.macroprocesso,
    PP.nome_prog
FROM projeu_projetos
JOIN 
    projeu_macropr PM ON PM.id = projeu_projetos.macroproc_fgkey
JOIN 
    projeu_programas PP ON PP.id_prog = projeu_projetos.progrm_fgkey;"""
mycursor.execute(sqlCanva)
dadosCanva = mycursor.fetchall()

comandUSERS = 'SELECT * FROM projeu_users;'
mycursor.execute(comandUSERS)
dadosUser = mycursor.fetchall()

names = [x[2] for x in dadosUser]
usernames = [x[3] for x in dadosUser]
hashed_passwords = [x[7] for x in dadosUser]

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
    perfilUsuario = [x[8] for x in dadosUser if str(x[1]).strip() == str(matriUser).strip()][0]
    user = [x[2] for x in dadosUser if x[3] == username][0]

    primeiroNome = user.split()[0]

    menuHtml = menuProjeuHtml(primeiroNome)
    menuCss = menuProjeuCss()
    st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
    st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

    font_TITLE('HOME', fonte_Projeto,"'Bebas Neue', sans-serif", 42, 'left')

    sqlEntregas = f"""SELECT 
            projeu_entregas.id_sprint, 
            projeu_entregas.nome_Entrega, 
            projeu_entregas.executor, 
            projeu_entregas.stt_entrega,
            projeu_sprints.number_sprint,
            projeu_projetos.name_proj
        FROM projeu_entregas
        JOIN projeu_sprints ON projeu_entregas.id_sprint = projeu_sprints.id_sprint
        JOIN projeu_projetos ON projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        WHERE projeu_entregas.stt_entrega NOT LIKE '%Concluído%' AND projeu_entregas.executor = {matriUser};"""
    mycursor.execute(sqlEntregas)
    entregaProj = mycursor.fetchall()
    mycursor.close()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
        nomeBotão = "CADASTRO DE PROJETOS"
        link = "https://9box.eucatur.com.br/Dashboard_Administrativo"
        image_url=  "https://cdn-icons-png.flaticon.com/128/3803/3803936.png"
        botao1(nomeBotão,link,image_url)

    with col2:
        st.write("")
        nomeBotão = "MEUS PROJETOS"
        link = 'https://9box.eucatur.com.br/Dashboard_Administrativo'
        image_url=  "https://cdn-icons-png.flaticon.com/128/64/64572.png"
        botao1(nomeBotão,link,image_url)

    with col3:    
        st.write("")
        nomeBotão = 'PRÊMIO'
        link = 'https://9box.eucatur.com.br/PDI'
        image_url="https://cdn-icons-png.flaticon.com/128/4798/4798118.png"
        botao1(nomeBotão,link,image_url)

    st.text(' ')


    col1, col2 = st.columns([1, 1.7])
    with col1:    
        ddbox = [[], [['Projeto para teste', 'Projeto Teste 2', 'teste teste projeto 123']]]
        links = [None, None, None]
        img_doc = '''https://cdn-icons-png.flaticon.com/128/2665/2665632.png'''
        
        html1 = ninebox_home(0, nineboxDatasUnidades_home(ddbox, links), ddbox, 'Ranking de Projetos', links, img_doc)
        ninebox_style = css_9box_home()
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True) 
        
        links = ["https://drive.google.com/file/d/1HitZgZkpMxlpj6_hDVlnTdg8ja_uuZYJ/view?usp=sharing", "https://drive.google.com/file/d/1TL-H33TrjgwdBM_eUD8gA9udqNNkkYrw/view?usp=sharing", "https://drive.google.com/file/d/1Wiz1EoiHNrZw4exVUdNVaWlN7AXH_Q3x/view?usp=sharing", "https://drive.google.com/file/d/1IjKIIIfFqZcFSKddc3ZWFnxrwdmlZznS/view?usp=sharing"]
        img_doc = 'https://cdn-icons-png.flaticon.com/128/6802/6802306.png'
        matApoio = [[], [['Manual do gestor de projeto', 'Práticas de idealização, Planejamento, Implantação e Avaliação de Projetos', 'Política - Gerenciamento do portfólio de projetos', 'Produto MVP-Final']]]

        html1 = ninebox_home(0, nineboxDatasUnidades_home(matApoio, links), matApoio, 'Material de Apoio', links, img_doc)
        ninebox_style = css_9box_home()
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True) 

        

    with col2:
        font_TITLE('Atividades Pendentes', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')
        if str(perfilUsuario).upper() in ['L', 'A']:
            if len(projetoNomeLider) == 'None' or len(projetoNomeLider) <= 0:
                st.info("Você não possui atividades pendentes no momento.")

            for k in range(len(projetoNomeLider)):
                with st.expander(f"Avaliar Complexidade | {projetoNomeLider[k][0]}"):
                    titleClass = ["Orientação do Projeto", "Impacto do Projeto"]
                    infoClass = [["Orientação para Inovação em Produtos/Serviços  atuais", "Orientação para desenvolvimento de novos Produtos/Serviços", "Orientação para Aumento de Receita", "Orientação para Aumento de Produtividade", "Orientação para Redução de Custos/Despesas", "Orientação para Transformação de processos de Negócio"],["Impacto na Percepção de Valor do Cliente", "Pressão Por Prazos", "Investimento necessário", "Nível de transformação organizacional", "Valor para o Negócio"]]
                    optionClass = ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]

                    font_TITLE(f'{projetoNomeLider[k][0]}', fonte_Projeto,"'Bebas Neue', sans-serif", 30, 'center')

                    canva = [x for x in dadosCanva if x[1] == projetoNomeLider[k][0]][0]
                    
                    listaEquipe = []
                    gestores = []
                    especialistas = []
                    squads = []

                    projetos = [canva[1]] if canva[1] != None else " "
                    mvps = [canva[3]] if canva[3] != None else " "
                    prodProjetos = [canva[2]] if canva[2] != None else " "
                    prodMvps = [canva[4]] if canva[4] != None else " "
                    resultados = [canva[6]] if canva[6] != None else " "
                    metricas = [canva[5]] if canva[5] != None else " "
                    for i in range(len(canva[7].split(','))):
                        colab = str(canva[7]).split(',')[i]
                        funcao = str(canva[7]).split(',')[i]
                        listaEquipe.append([colab, funcao])

                    for i in range(len(listaEquipe)):
                        if listaEquipe[i][1] == "Gestor":
                            gest = listaEquipe[i][0]
                            listaEquipe.append(gest)
                            gestores.append(gest)
                        elif listaEquipe[i][1] == "Especialista":
                            espec = listaEquipe[i][0]
                            listaEquipe.append(espec)
                            especialistas.append(espec)
                        else:
                            executor = listaEquipe[i][0]
                            listaEquipe.append(executor)
                            squads.append(executor)
                    if len(gestores) == 0:
                        gestores = " "
                    if len(especialistas) == 0:
                        especialistas = " "
                    if len(squads) == 0:
                        squads = " "

                    entregas = str(canva[9]).split(';') if ';' in str(canva[9]) else str(canva[9]).split(',')
                    investimentos = [canva[10]] if canva[10] != None else " "

                    col1, col2, col3 = st.columns([1,1,0.6])
                    with col1:
                        st.text_input('Gestor', gestores, key=f'{projetos} 1')
                    with col2:
                        st.text_input('Macroprocesso', canva[11], key=f'{projetos} 2')#MACROPROCESSO
                    with col3:
                        st.text_input('Investimento', investimentos[0], key=f'{projetos} 6')
                        
                    st.text_input('Programa', canva[12], key=f'{projetos} 3')#PROGRAMA
                    st.text_input('MVP', mvps[0], key=f'{projetos} 4')
                    
                    col1, col2 = st.columns([3,2])
                    with col1:
                        st.multiselect('Squad', squads, squads, disabled=True, key=f'{projetos} 9')
                    with col2:
                        st.text_input('Especialistas', especialistas, key=f'{projetos} 7')
                    
                    font_TITLE(f'Principais Entregas', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
                    for entrg_idx in range(len(entregas)):
                        st.text_input('Entregas', entregas[entrg_idx], label_visibility='collapsed', key=f'entregas nomes{entrg_idx} {projetos[0]}')

                    notaGrau = []
                    for i in range(len(titleClass)):
                        font_TITLE(f'{titleClass[i]}', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left')
                        listNota = []
                        for j in infoClass[i]:
                            nota = int(st.select_slider(j, optionClass, key=f"chave{k}_{i}_{j}", value=optionClass[0])[0][0:1])
                            listNota.append(nota)
                            st.text(' ')
                            st.text(' ')
                        notaGrau.append(listNota)
                    mediaImpacto = round(sum(notaGrau[1]) / len(notaGrau[1]), 2)
                    maiorOrientacao = max(notaGrau[0])
                    grauProjeto = round(((mediaImpacto + maiorOrientacao) / 2), 2)
                    
                    if grauProjeto == 0:
                        complexidade = ""
                    elif grauProjeto <= 1:
                        complexidade = "Seguro"
                    elif grauProjeto <= 2:
                        complexidade = "Acessível"
                    elif grauProjeto <= 3:
                        complexidade = "Abstrato"
                    elif grauProjeto <= 4:
                        complexidade = "Singular"
                    else:
                        complexidade = "Valor inválido"

                    finalizar = st.button("Finalizar avaliação", key=f"notaLider_{k}")

                    if finalizar:
                        colunas = ["grauProjeto", "complxdd", "check_lider", "id_edic_fgkey"]
                        dadosLider = [grauProjeto, f"'{complexidade}'", 1, matriUser]

                        for i in range(len(colunas)):
                            sqlUpdate = f"UPDATE projeu_complexidade SET {colunas[i]} = {dadosLider[i]} WHERE proj_fgkey = {projetoNomeLider[k][1]}"
                            mycursor.execute(sqlUpdate)
                            conexao.commit()
                        st.toast('Dados Atualizados!', icon='✅')
                        sleep(3)
                        st.rerun()
        elif str(perfilUsuario).strip().upper() in ['GV', 'A']:
            if len(projetoNomeGover) == 'None' or len(projetoNomeGover) <= 0:
                st.info("Você não possui atividades pendentes no momento.")

            for k in range(len(projetoNomeGover)):
                with st.expander(f"Avaliar Complexidade | {projetoNomeLider[k][0]}"):
                    titleClass = ["Escopo do Projeto", "Squads do Projeto"]
                    infoClass = [["Impacto do escopo no Planejamento Estratégico", "Incerteza do escopo", "Complexidade  do escopo"], ["Senioridade da Squad", "Senioridade do Especialista", "Senioridade do Gestor do Projeto"]]
                    optionClass = ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]

                    font_TITLE(f'{projetoNomeLider[k][0]}', fonte_Projeto,"'Bebas Neue', sans-serif", 23, 'center')

                    st.text(' ')
                    canva = [x for x in dadosCanva if x[1] == projetoNomeGover[k][0]][0]
                    
                    listaEquipe = []
                    gestores = []
                    especialistas = []
                    squads = []

                    projetos = [canva[1]] if canva[1] != None else " "
                    mvps = [canva[3]] if canva[3] != None else " "
                    prodProjetos = [canva[2]] if canva[2] != None else " "
                    prodMvps = [canva[4]] if canva[4] != None else " "
                    resultados = [canva[6]] if canva[6] != None else " "
                    metricas = [canva[5]] if canva[5] != None else " "
                    for i in range(len(canva[7].split(','))):
                        colab = str(canva[7]).split(',')[i]
                        funcao = str(canva[7]).split(',')[i]
                        listaEquipe.append([colab, funcao])

                    for i in range(len(listaEquipe)):
                        if listaEquipe[i][1] == "Gestor":
                            gest = listaEquipe[i][0]
                            listaEquipe.append(gest)
                            gestores.append(gest)
                        elif listaEquipe[i][1] == "Especialista":
                            espec = listaEquipe[i][0]
                            listaEquipe.append(espec)
                            especialistas.append(espec)
                        else:
                            executor = listaEquipe[i][0]
                            listaEquipe.append(executor)
                            squads.append(executor)
                    if len(gestores) == 0:
                        gestores = " "
                    if len(especialistas) == 0:
                        especialistas = " "
                    if len(squads) == 0:
                        squads = " "

                    entregas = str(canva[9]).split(';') if ';' in str(canva[9]) else str(canva[9]).split(',')
                    investimentos = [canva[10]] if canva[10] != None else " "

                    col1, col2, col3 = st.columns([1,1,0.6])
                    with col1:
                        st.text_input('Gestor', gestores, key=f'{projetos} 1')
                    with col2:
                        st.text_input('Macroprocesso', canva[11], key=f'{projetos} 2')#MACROPROCESSO
                    with col3:
                        st.text_input('Investimento', investimentos[0], key=f'{projetos} 6')
                        
                    st.text_area('Programa', canva[12], key=f'{projetos} 3')#PROGRAMA
                    st.text_input('MVP', mvps[0], key=f'{projetos} 4')
                    
                    col1, col2 = st.columns([3,2])
                    with col1:
                        st.multiselect('Squad', squads, squads, disabled=True, key=f'{projetos} 9')
                    with col2:
                        st.text_input('Especialistas', especialistas, key=f'{projetos} 7')
                    
                    font_TITLE(f'Principais Entregas', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
                    for entrg in entregas:
                        st.text_input('Entregas', entrg, label_visibility='collapsed', key=f'{entrg} {projetos} 5')
    
                    st.text(' ')
                    notaGov = []
                    for i in range(len(titleClass)):
                        font_TITLE(f'{titleClass[i]}', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
                        listNota = []
                        for j in infoClass[i]:
                            nota = int(st.select_slider(j, optionClass, key=f"chave{k}_{i}_{j}", value=optionClass[0])[0][0:1])
                            listNota.append(nota)
                            st.write("---")
                        notaGov.append(listNota)
                    grauEscopo = round(sum(notaGov[0]) / len(notaGov[0]), 2)
                    grauSquad = round(sum(notaGov[1]) / len(notaGov[1]), 2)
                    mediaGov = round(((grauEscopo + grauSquad) / 2), 2)

                    if mediaGov == 0:
                        nivel = ""
                    elif mediaGov <= 2:
                        nivel = "I"
                    elif mediaGov <= 3:
                        nivel = "II"
                    elif mediaGov <= 4:
                        nivel = "III"
                    else:
                        nivel = "Valor médio fora do intervalo válido"

                    finalizar = st.button("Finalizar avaliação", key=f"notaGovernanca_{k}")

                    if finalizar:
                        colunas = ["grauEscopo", "grauSquad", "nivel", "check_govern", "id_edic_fgkey"]
                        dadosGover = [grauEscopo, grauSquad, f"'{nivel}'", 1, matriUser]

                        for i in range(len(colunas)):
                            sqlUpdate = f"UPDATE projeu_complexidade SET {colunas[i]} = {dadosGover[i]} WHERE proj_fgkey = {projetoNomeGover[k][1]}"
                            mycursor.execute(sqlUpdate)
                            conexao.commit()
                        st.toast('Dados Atualizados!', icon='✅')
                        sleep(3)
                        st.rerun()
        else:
            if entregaProj == 'None' or len(entregaProj) <= 0:
                st.info("Você não possui atividades pendentes no momento.")

        for i in range(len(entregaProj)):
            cardEntregaHtml = f"""<div class="main">
                    <div class="card">
                        <div class="sprint">Sprint {str(entregaProj[i][4])}</div>
                        <div class="entrega">Entrega: {entregaProj[i][1]}</div>
                        <div class="status">Status: {entregaProj[i][3]}</div>
                    </div>
                </div>"""
            
            cardEntregaCss = """.main{
                    display: flex;
                    align-items: center;
                }

                .card{
                    max-width: 100%;
                    min-width: 100%;
                }

                .card:hover{
                    transform: scale(1.03);
                }

                .sprint{
                    font-size: 18px;
                    font-weight: bold;
                }

                .entrega{
                    margin-top: 10px;
                    font-size: 16px;
                }

                .status{
                    margin-top: 10px;
                    font-size: 16px;
                }"""
            
            with st.expander(f"{str(entregaProj[i][5])} || {entregaProj[i][1]}"):
                st.write(f"{cardEntregaHtml}", unsafe_allow_html=True)
                st.write(f"<style>{cardEntregaCss}<style>", unsafe_allow_html=True)
