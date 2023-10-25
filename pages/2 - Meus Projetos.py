import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
from util import font_TITLE, string_to_datetime, cardMyProject, cardGRANDE
from collections import Counter
import mysql.connector 
import streamlit_authenticator as stauth
from utilR import PlotCanvas


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
    projeu_projetos.result_esperad as resultado_esperad,
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
    projeu_projetos.produto_mvp,
    (
        SELECT group_concat(entreg)
        FROM projeu_princEntregas
        WHERE projeu_princEntregas.id_proj_fgkey = projeu_projetos.id_proj
    )as PrincipaisEntregas,
    (
        SELECT group_concat(name_metric)
        FROM projeu_metricas
        WHERE id_prj_fgkey = projeu_projetos.id_proj
    ) AS metricas
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

def mapear_dificuldade(dificuldade):
    if dificuldade == 'Fácil':
        return 'F'
    elif dificuldade == 'Médio':
        return 'M'
    elif dificuldade == 'Difícil':
        return 'D'
    else:
        return '---'  # Retornar None ou lançar um erro para outros valores


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
            
            pessoas = str(dadosOrigin[0][21]).split(',') if dadosOrigin[0][21] != None else ''
            funcao = str(dadosOrigin[0][22]).split(',') if dadosOrigin[0][22] != None else ''
            equipBD = [[pessoas[x], funcao[x]] for x in range(len(pessoas))]

            resultados = []
            for i in range(len(dadosOrigin)):
                if dadosOrigin[i][9] != None:
                    resultados.append(f"{dadosOrigin[i][9]}")
                else:
                    resultados = " "
            
            if dadosOrigin[0][16] != None:
                entregas = str(dadosOrigin[0][25]).split(';') if ';' in str(dadosOrigin[0][25]) else str(dadosOrigin[0][25]).split(',')
            else:
                entregas = ' '

            metricas = str(dadosOrigin[0][26]).split(',') if dadosOrigin[0][26] != None else ' '
            prodProjetos = str(dadosOrigin[0][10]).split(',') if dadosOrigin[0][10] != None else " "
            prodMvps = str(dadosOrigin[0][24]).split(',') if dadosOrigin[0][24] != None else " "

            canvas = PlotCanvas(projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, [x[0] for x in equipBD if x[1] == 'Especialista'], [x[0] for x in equipBD if x[1] == 'Executor'], entregas, investimentos)
            htmlRow = canvas.CreateHTML()
            htmlEqp = canvas.tableEqp()
            htmlUnic = canvas.tableUnic()
            htmlCol = canvas.tableCol()

            html = canvas.tableGeral(htmlRow, htmlEqp, htmlUnic, htmlCol)
            canvaStyle = canvas.cssStyle()

            st.write(f'<div>{html}</div>', unsafe_allow_html=True)
            st.write(f'<style>{canvaStyle}</style>', unsafe_allow_html=True)

            #####APRESENTANDO HORAS TOTAIS GASTAS NO PROJETO DAQUELE COLABORADOR
            st.text(' ')
            st.text(' ')
            font_TITLE('MEU DESEMPENHO NO PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 40, 'left', '#228B22')
            
            dffMyProject = Counter([x[4] for x in EntregasBD if x[7] == matriUser]) if len([x for x in EntregasBD if x[7] == matriUser]) > 0 else Counter(['-'])
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
                    
                    if number_sprint_new == 1:
                        cmdUP_stt_proj = f'UPDATE projeu_projetos SET status_proj = "Em Andamento" WHERE id_proj = {dadosOrigin[0][0]};'
                        mycursor.execute(cmdUP_stt_proj)
                        conexao.commit()
                        
                    mycursor.close()
                    st.toast('Sucesso na adição da sprint!', icon='✅')
                    st.text(' ')
                    st.rerun()

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
                            st.rerun()
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
                                
                                #PREPARANDO OS DADOS PARA APRESENTAR NO CARD DA SPRINT
                                contagem_dif = Counter([x[4] for x in spEntregas])                
                                dif_comum = contagem_dif.most_common(1)
                                
                                porc_avan = f'{int((len([x for x in spEntregas if str(x[5]).strip() == "🟩 Concluído"]) / len([x for x in spEntregas if x[1] != None])) * 100) if len([x for x in spEntregas if x[1] != None]) > 0 else 0}%'           
                                cardGRANDE(['Colaboradores', 'Atividades', 'Entregues', 'Avanço', 'Horas', 'Complexidade'], [len(list(set([x[2] for x in spEntregas if x[2] != None]))), len([x for x in spEntregas if x[1] != None]), len([x for x in spEntregas if str(x[5]).strip() == '🟩 Concluído']), porc_avan, sum([x[3] for x in spEntregas]), mapear_dificuldade(dif_comum[0][0])])
         
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
                                    col1, col2, col3, col4, col5 = st.columns([1, 0.3, 0.25, 0.25, 0.2])
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
                                        st.rerun()

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
                                                        nome_entrega = '{atvdd_exc}' 
                                                        AND executor = (SELECT id_user FROM projeu_users WHERE Nome = '{exec_exc}' LIMIT 1)
                                                        AND compl_entrega = '{compl_exc}'
                                                        AND stt_entrega = '{stt_exc}';"""
                                                        
                                        mycursor.execute(cmd_exc)
                                        conexao.commit()

                                        st.toast('Entrega Excluida!', icon='✅')
                                        mycursor.close()
                                        st.rerun()
    else:
        st.text(' ')
        st.text(' ')
        font_TITLE(f'AINDA NÃO HÁ PROJETOS VINCULADOS A VOCÊ!! ⏳', fonte_Projeto,"'Bebas Neue', sans-serif", 22, 'center')
