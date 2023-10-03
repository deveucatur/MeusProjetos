import streamlit as st
import pandas as pd
from PIL import Image
from utilR import font_TITLE, string_to_datetime, cardGRANDE, displayInd, ninebox, css_9box, nineboxDatasUnidades
from time import sleep
import mysql.connector
from datetime import date
from collections import Counter
from utilR import PlotCanvas
import streamlit_authenticator as stauth


icone = Image.open('imagens/icone.png')
st.set_page_config(
    page_title="Gerir Projetos",
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
comand = f"""
SELECT 
    projeu_projetos.id_proj, 
    projeu_projetos.name_proj,
    (SELECT Nome FROM projeu_users WHERE id_user = projeu_projetos.gestor_id_fgkey) AS name_gestor, 
    (SELECT Matricula FROM projeu_users WHERE id_user = projeu_projetos.gestor_id_fgkey) AS matricula_gestor,
    (SELECT type_proj FROM projeu_type_proj WHERE id_type = projeu_projetos.type_proj_fgkey) AS type_proj,
    (SELECT macroprocesso FROM projeu_macropr WHERE id = projeu_projetos.macroproc_fgkey) AS macroprocesso,
    (SELECT nome_prog FROM projeu_programas WHERE id_prog = projeu_projetos.progrm_fgkey) AS programa,
    projeu_projetos.nome_mvp,
    projeu_projetos.investim_proj,
    projeu_projetos.result_esperad as objetivo_projet,
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
    ) as matriculaEQUIPE,
    projeu_projetos.status_proj AS STATUS_PROJETO,
    projeu_projetos.produto_mvp AS PRODUTO_MVP,
    projeu_projetos.prazo_entreg_final,
    (
        SELECT GROUP_CONCAT(id_sprint) 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as id_sprint,
    projeu_projetos.date_aprov_proj,
    projeu_projetos.date_posse_gestor,
    projeu_projetos.date_imersao_squad,
    projeu_projetos.status_proj,
    (
		SELECT 
			GROUP_CONCAT(entreg) 
		FROM projeu_princEntregas 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			GROUP_CONCAT(name_metric) 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS METRICAS   
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

def tableGeral():
    dadosUnic = tableUnic()

    htmlGeral = f"""
        <div class="flex-container">
            <div class="flex-row">
                <div>{dadosUnic}</div>
            </div>
        </div>
    """
    return htmlGeral

canvaStyle = """
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
    bodyC{
        margin: 0;
        padding: 0;
        background-color: #fff;
    }
    
    .boxC{
        display: flex;
        align-items: flex-end;
        justify-content: center;
        width: 100%;
    }

    .box5C {
        width: 100%;
        height: auto;
        margin: 5px;
        overflow: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.0), 0 4px 6px -2px rgba(0, 0, 0, 0.0);
        border-radius: 25px;
    }

    .box5C:hover{
        transform: scale(0.98);
        border-radius: 20px;
    }

    .table5C{
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden; 
        min-height: 220px;
        max-height: 220px;
    }

    .thead5C{
        background-color: #DADADA;
        position: sticky;
        top: 0;
        z-index: 1;
    }

    .thead5C{
        min-height: 50px;
        max-height: 50px;
    }

    .thead5C th{
        text-align: center;
        min-height: 50px;
        max-height: 50px;
        font-weight: bold;
        font-family: Bebas Neue;
        font-size: 22px;
    }

    .thead5C img{
        vertical-align: middle;
        margin-left: 10px;
        width: 20px;
        height: auto;
    }

    .tdata5C td{
        border-top: 1px solid #96008c93;
        background-color: #fff;
    }

    .flex-rowC {
        display: flex;
        justify-content: center;
        height: auto;
    }
    
    .box5C::-webkit-scrollbar{
        width: 6px;
        border-radius: 20px;
    }
    
    .box5C::-webkit-scrollbar-track{
        border-radius: 20px;
    }
    
    .box5C::-webkit-scrollbar-thumb{
        border-radius: 20px;
        border: 1px solid;
    }"""

def tableUnic():
    entrega = entregas
    entregaCode = ""
    for i in range(len(entrega)):
        entregaCode += f"""<tr class="tdata5C">
                <td>{entrega[i]}</td>
            </tr>"""

    htmlUnic = f"""
        <div class="boxC">
            <div class="box5C">
                <table class="table5C">
                    <tr class="thead5C">
                        <th>PROJETOS</th>
                    </tr>
                    <div>{entregaCode}</div>
                </table>
            </div>
        </div>
    """
    return htmlUnic

    
def mapear_dificuldade(dificuldade):
    if dificuldade == 'Fácil':
        return 'F'
    elif dificuldade == 'Médio':
        return 'M'
    elif dificuldade == 'Difícil':
        return 'D'
    else:
        return '---' 

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

    fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
    font_TITLE('GERIR PORTIFÓLIO', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')

    st.text(' ')
    font_TITLE('ACOMPANHAMENTO DOS PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 30, 'left', '#228B22')
    st.text(' ')
    #############INFORMAÇÕES GERAIS DE PROJETOS#############
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        displayInd('Total', f'{len(id_projcts:=list(set([x[0] for x in ddPaging])))}', 1, 3)
    with col2:
        displayInd('Não Iniciado', f'{len(list(set([x[0] for x in ddPaging if x[13] == None or string_to_datetime(str(x[13]).split(",")[0]) > date.today()])))}', 1, 3)
    with col3:
        displayInd('Em Andamento', f'{len(list(set([x[0] for x in ddPaging if x[13] != None and string_to_datetime(str(x[13]).split(",")[0]) < date.today() and x[24] != "Concluído"])))}', 1, 3)
    with col4:
        displayInd('Paralisado', f'{len([x[1] for x in ddPaging if str(x[31]).strip() == "Paralisado"])}', 1, 3)
    with col5:
        displayInd('Concluído', f'{len(list(set([x[0] for x in ddPaging if x[24] == "Concluído"])))}', 1, 3)
    #AGUARDANDO INÍCIO, EM ANDAMENTO, PARALISADO
    dadosbox = [[],[[x[1] for x in ddPaging if str(x[31]).strip() == 'Aguardando Início'], 
                    [x[1] for x in ddPaging if str(x[31]).strip() == 'Em Andamento'], 
                    [x[1] for x in ddPaging if str(x[31]).strip() == 'Paralisado']]]
    ninebox_style = css_9box()

    colbox, colbox1, colbox2 = st.columns(3)
    with colbox:
        html1 = ninebox(2, nineboxDatasUnidades(dadosbox), dadosbox, 'Aguardando Início')
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)
        
    with colbox1:
        html1 = ninebox(1, nineboxDatasUnidades(dadosbox), dadosbox, 'Em Andamento')
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)    
            
    with colbox2:
        html1 = ninebox(0, nineboxDatasUnidades(dadosbox), dadosbox, 'Paralisado')
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)
    
    st.text(' ')
    font_TITLE('ACOMPANHAMENTO POR PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 30, 'left', '#228B22')
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
        
        cmd_observcao = f"""SELECT 
                                id_observ AS ID_OBSERVAÇÃO, 
                                id_sprint_fgkey AS ID_SPRINT, 
                                PS.number_sprint AS NUMBER_SPRINT, 
                                observacao AS TEXTO_OBSERVACAO, 
                                data_observ AS DATA_OBSERVACAO, 
                                (
                                    SELECT Nome FROM projeu_users WHERE id_user = ultm_edicao LIMIT 1
                                ) AS ULTIMA_EDICAO
                            FROM 
                                projeu_projt_observ 
                            JOIN 
                                projeu_sprints PS ON id_sprint = id_sprint_fgkey
                            WHERE 
                                PS.id_sprint IN ({dadosOrigin[0][27] if dadosOrigin[0][27] != None else 'null'});"""

    st.text(' ')
    st.text(' ')
    if len(dadosOrigin) > 0:
        #CONSULTANDO OS DADOS DAS ENTREGAS
        mycursor = conexao.cursor()  
        mycursor.execute(cmd_entregas)
        EntregasBD = mycursor.fetchall()
        
        #CONSULTANDO OS DADOS DE OBSERVAÇÕES
        mycursor.execute(cmd_observcao)
        ObservBD = mycursor.fetchall()
        mycursor.close()
        
        font_TITLE(f'{dadosOrigin[0][1]}', fonte_Projeto,"'Bebas Neue', sans-serif", 31, 'center', '#228B22')
        ########CANVAS DO PROJETO SELECIONADO########
        projetos = [dadosOrigin[0][1]] if dadosOrigin[0][1] != "None" else " "
        mvps = [dadosOrigin[0][7]] if dadosOrigin[0][7] != "None" else " "  
        investimentos = [f"{dadosOrigin[0][8]}"] if f"{dadosOrigin[0][8]}" != "None" else " "
        gestores = [f"{dadosOrigin[0][2]}"] if f"{dadosOrigin[0][2]}" != "None" else " "
        
        pessoas = str(dadosOrigin[0][21]).split(',') if dadosOrigin[0][21] != None else ''
        funcao = str(dadosOrigin[0][22]).split(',') if dadosOrigin[0][22] != None else ''
        equipBD = [[pessoas[x], funcao[x]] for x in range(len(pessoas))]

        resultados = []
        for i in range(len(dadosOrigin)):
            if dadosOrigin[i][9] != None:
                resultados.append(f"{dadosOrigin[i][9]}")
            else:
                resultados = " "
        
        if dadosOrigin[0][32] != None:
            entregas = str(dadosOrigin[0][32]).split(';') if ';' in str(dadosOrigin[0][32]) else str(dadosOrigin[0][32]).split(',')
        else:
            entregas = ' '

        metricas = str(dadosOrigin[0][33]).split(',') if dadosOrigin[0][33] != None else ' '
        prodProjetos = str(dadosOrigin[0][10]).split(',') if dadosOrigin[0][10] != None else " "
        prodMvps = str(dadosOrigin[0][25]).split(',') if dadosOrigin[0][24] != None else " "

        
    #SEQUÊNCIA --> projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, especialistas, squads, entregas, investimentos
        canvas = PlotCanvas(projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, [x[0] for x in equipBD if x[1] == 'Especialista'], [x[0] for x in equipBD if x[1] == 'Executor'], entregas, investimentos)
        htmlRow = canvas.CreateHTML()
        htmlEqp = canvas.tableEqp()
        htmlUnic = canvas.tableUnic()
        htmlCol = canvas.tableCol()

        html = canvas.tableGeral(htmlRow, htmlEqp, htmlUnic, htmlCol)
        canvaStyle = canvas.cssStyle()

        st.write(f'<div>{html}</div>', unsafe_allow_html=True)
        st.write(f'<style>{canvaStyle}</style>', unsafe_allow_html=True)

        ########APRESENTAÇÃO DOS DADOS DO PROJETO SELECIONADO########
        st.text(' ')
        st.text(' ')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            displayInd('Status do Projeto', f'{dadosOrigin[0][31]}', 1, 3)
        with col2:
            displayInd('Progresso do Projeto', f'{50}%', 1, 3)
        with col3:
            displayInd('Sprint Atual', f'{len(str(dadosOrigin[0][11]).split(","))}', 1, 3)
        with col4:
            displayInd('Total de Horas', f'{sum([int(x) for x in str(dadosOrigin[0][18]).split(",")]) if dadosOrigin[0][18] != None else 0}', 1, 3)

        st.text(' ')
        dados_control = [string_to_datetime(dadosOrigin[0][28]) if dadosOrigin[0][28] != None else None,  
                        string_to_datetime(dadosOrigin[0][29]) if dadosOrigin[0][29] != None else None, 
                        string_to_datetime(dadosOrigin[0][30]) if dadosOrigin[0][30] != None else None, 
                        dadosOrigin[0][31]]
        
        with st.expander('Controle do Projeto', expanded=True): 
            
            font_TITLE('DATAS', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')  
            dt_aprov = st.date_input('Aprovação do Projeto', dados_control[0])
            dt_poss_gtr = st.date_input('Posse do Gestor', dados_control[1])
            dt_ims_sqd = st.date_input('Imersão Squad', dados_control[2])
            
            st.text(' ')
            font_TITLE('STATUS PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
            opc_stt = ['Aguardando Início', 'Em Andamento', 'Concluído', 'Paralisado', 'Cancelado']
            stt_proj = st.selectbox('stt', opc_stt, opc_stt.index(str(dados_control[3]).strip()), label_visibility='collapsed')

            st.text(' ')
            btt_control_proj = st.button('Atualizar', key='btt_control_proj')
            if btt_control_proj:
                try:
                    mycursor = conexao.cursor()
                    columns_control = ['date_aprov_proj', 'date_posse_gestor', 'date_imersao_squad', 'status_proj']
                    values_control = [dt_aprov, dt_poss_gtr, dt_ims_sqd, stt_proj]

                    for idx_control in range(len(columns_control)):
                        if values_control[idx_control] != None:
                            cmd_up_control_proj = f'UPDATE projeu_projetos SET {columns_control[idx_control]} = "{values_control[idx_control]}" WHERE id_proj = 1;'
                            mycursor.execute(cmd_up_control_proj)
                            conexao.commit()
                    
                    mycursor.close()
                    st.toast('Dados Atualizados!', icon='✅')
                    sleep(1.3)
                    st.rerun()

                except:
                    st.toast('Erro ao atualizar dados de controle do projeto.', icon='❌')


        func_split = lambda x: x.split(",") if x is not None else [x]
        param_sprint = ['PRÉ MVP', 'MVP', 'PÓS MVP']
        if func_split(dadosOrigin[0][11])[0] != None:
            # ----> DADOS [NUMBER_SPRINT, STATUS_SPRINT,  DATA INC SPRINT, DATA FIM SPRINT]
            sprints = [[func_split(dadosOrigin[0][11])[x], param_sprint.index(func_split(dadosOrigin[0][12])[x]), func_split(dadosOrigin[0][13])[x], func_split(dadosOrigin[0][14])[x], func_split(dadosOrigin[0][27])[x]] for x in range(len(func_split(dadosOrigin[0][11])))]
            
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
                            
                            #PREPARANDO OS DADOS PARA APRESENTAR NO CARD DA SPRINT
                            contagem_dif = Counter([x[4] for x in spEntregas])                
                            dif_comum = contagem_dif.most_common(1)
                            
                            porc_avan = f'{int((len([x for x in spEntregas if str(x[5]).strip() == "🟩 Concluído"]) / len([x for x in spEntregas if x[1] != None])) * 100) if len([x for x in spEntregas if x[1] != None]) > 0 else 0}%'           
                            cardGRANDE(['Colaboradores', 'Atividades', 'Entregues', 'Avanço', 'Horas', 'Complexidade'], [len(list(set([x[2] for x in spEntregas if x[2] != None]))), len([x for x in spEntregas if x[1] != None]), len([x for x in spEntregas if str(x[5]).strip() == '🟩 Concluído']), porc_avan, sum([x[3] for x in spEntregas]), mapear_dificuldade(dif_comum[0][0])])
                            st.text(' ')

                            tab1, tab2, tab3, tab4 = st.tabs(['Entregas', 'Excluir', 'Homologação', 'Observação'])
                            with tab1:
                                font_TITLE('ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')  
                                #FORMULÁRIO APRESENTANDO AS ENTREGAS
                                col1, col2, col3 = st.columns([3,1,1])
                                qnt_att = st.number_input('Adcionar Atividade', min_value=0, step=1, key=f'add{idx_spr} - {idx_parm}')
                                
                                spEntregas.extend([[idx_spr, None, None, 0 , '---', '🟨 Backlog', None] for x in range(qnt_att)])

                                st.text(' ')
                                col1, col2, col3, col4, col5 = st.columns([1, 0.3, 0.25, 0.25, 0.2])
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
                                                cmd_update = f'''UPDATE projeu_entregas SET {columnsUP[idxColum]} = {f'"{list_atual[idxColum]}"' if idxColum != 1 else f'(SELECT id_user FROM projeu_users WHERE Nome = "{list_atual[idxColum]}" LIMIT 1)'} WHERE id_entr = {list_atual[5]};'''
                                                mycursor.execute(cmd_update)
                                                conexao.commit()
                                            
                                            
                                        else: #INSERT DA ENTREGA CASO ELA NÃO ESTEJA PRESENTE DENTRO DO BANCO DE DADOS
                                            if list_atual[0] != None and list_atual[0] != '': 
                                                cmd_insert = f'''
                                                    INSERT INTO projeu_entregas (id_sprint, nome_Entrega, executor, hra_necess, stt_entrega, compl_entrega) 
                                                        values((SELECT id_sprint FROM projeu_sprints WHERE number_sprint = {spEntregas[0][0]}  
                                                            AND id_proj_fgkey = 
                                                                (SELECT id_proj FROM projeu_projetos WHERE name_proj = '{dadosOrigin[0][1]}') LIMIT 1),
                                                                "{list_atual[0]}", 
                                                                (SELECT id_user FROM projeu_users WHERE Nome = '{list_atual[1]}' LIMIT 1),
                                                                {list_atual[2]},
                                                                "{list_atual[3]}",
                                                                "{list_atual[4]}");'''
                                                mycursor.execute(cmd_insert)
                                                conexao.commit()
                                    
                                    mycursor.close()
                                    st.toast('Dados Atualizados!', icon='✅')
                                    sleep(1.3)
                                    st.rerun()

                            with tab2:
                                font_TITLE('EXCLUIR', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')  
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
                                                    nome_entrega = '{atvdd_exc}' 
                                                    AND executor = (SELECT id_user FROM projeu_users WHERE Nome = '{exec_exc}' LIMIT 1)
                                                    AND compl_entrega = '{compl_exc}'
                                                    AND stt_entrega = '{stt_exc}';"""
                                                    
                                    mycursor.execute(cmd_exc)
                                    conexao.commit()

                                    st.toast('Entrega Excluida!', icon='✅')
                                    mycursor.close()
                                    sleep(1.3)
                                    st.rerun()

                            with tab3:
                                font_TITLE('HOMOLOGAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
                                col1, col2, col3 = st.columns([2,1,1])
                                with col1:
                                    st.caption('Tipo de Homologação')
                                    type_homol = st.selectbox('Tipo de Homologação', ['SPRINT PRÉ MVP', 'MVP', 'SPRINT PÓS MVP', 'ENTREGA FINAL'], label_visibility="collapsed", key=f' - {idx_spr} typHomo')
                                with col2:
                                    st.caption('Data Homologação')
                                    date_homol = st.date_input('Fím Sprint', label_visibility="collapsed", key=f'Homo_sprint{idx_spr}')
                                with col3:
                                    st.caption('Status Homologação')
                                    stt_homol = st.selectbox('Fím Sprint', ['PARA AGENDAR', 'AGUARDANDO HOMOLOGAÇÃO', 'HOMOLOGADO COM AJUSTES', 'HOMOLOGADO', 'NÃO HOMOLOGADO'],label_visibility="collapsed", key=f'status_homo{idx_spr}')
                                st.caption('Parecer Homologação')
                                parec_homol = st.text_area('Planejamento Sprint', label_visibility="collapsed", key=f'parec_homol{idx_spr}')
                                
                                btt_homo = st.button('Enviar', key=f'btt homolog {idx_spr}')
                                if btt_homo:
                                    if len(parec_homol) > 0:
                                        try:
                                            mycursor = conexao.cursor()
                                            columns = ['tip_homolog', 'date_homolog', 'status_homolog', 'parecer_homolog']
                                            values = [f'"{type_homol}"', f'STR_TO_DATE("{date_homol}", "%Y-%m-%d")', f'"{stt_homol}"', f'"{parec_homol}"']
                                            for idx_clm in range(len(columns)):
                                                cmdHOMO = f'UPDATE projeu_sprints SET {columns[idx_clm]} = {values[idx_clm]} WHERE id_sprint = {ddSprint[idx_spr - 1][4]};'
                                                mycursor.execute(cmdHOMO)
                                                conexao.commit()
                                            
                                            st.toast('Dados de homologação atualizados', icon='✅')
                                            mycursor.close()
                                            sleep(1.3)

                                        except:
                                            st.toast('Erro ao adcionar homologação ao banco de dados.', icon='❌')
                                        
                                        st.rerun()
                                    else:
                                        st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')

                            with tab4:
                                #OBSERVAÇÃO DA SPRINT SELECIONADA
                                obsv_sprint = [x for x in ObservBD if x[2] == idx_spr]
                                if len(obsv_sprint)>0:
                                    font_TITLE('Histórico de Observações', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
                                    for idx_spt in range(len(obsv_sprint)):
                                        font_TITLE(f'{str(obsv_sprint[idx_spt][5])} - {str(obsv_sprint[idx_spt][4])}', fonte_Projeto,"'Bebas Neue', sans-serif", 17, 'left', '#228B22')
                                        st.markdown(obsv_sprint[idx_spt][3])

                                    st.text(' ')                                
                                
                                font_TITLE('ADCIONAR OBSERVAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')  
                                obs_sprt = st.text_area('awdadad',label_visibility="collapsed", key=f'OBSERVAÇAÕ{idx_spr}')
                                btt_homo = st.button('Enviar', key=f'btt obsrv {idx_spr}')
                                
                                if btt_homo:
                                    if len(obs_sprt) > 0:
                                        try:
                                            mycursor = conexao.cursor()
                                            cmd_observ = f"INSERT INTO projeu_projt_observ(id_sprint_fgkey, observacao, data_observ, ultm_edicao) values ({ddSprint[idx_spr - 1][4]}, '{obs_sprt}', STR_TO_DATE('{date.today()}', '%Y-%m-%d'), (SELECT id_user FROM projeu_users WHERE Matricula = {matriUser} LIMIT 1));"
                                            
                                            mycursor.execute(cmd_observ)
                                            conexao.commit()
                                            mycursor.close()
                                            st.toast('Observação vinculada a sprint.', icon='✅')
                                           
                                        except:
                                            st.toast('Erro ao adcionar a obeservação.', icon='❌')
                                        
                                        st.rerun()
                                    else:
                                        st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')

    

            
