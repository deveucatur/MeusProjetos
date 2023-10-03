import streamlit as st
import mysql.connector
from util import font_TITLE
from util import string_to_datetime
from datetime import date

st.set_page_config(page_title="Cadastro de Parâmetros", layout="wide")
conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)

####### CONCULTA BAGUNÇADA DE DADOS GERAIS SOBRE OS PROGRAMAS #######
mycursor = conexao.cursor()
consult1AUX = """
            SELECT 
                T2.id_prog AS idTIPOPROG,
                T2.nome_prog AS NOMEPROG,
                T2.inic_pg AS INICIO,
                T2.fim_pg AS FIM,
                T2.status_pg AS STATUS_PG,
                (SELECT macroprocesso FROM projeu_macropr WHERE id = T2.macroprocesso_fgkey) as macroprocPROG,
                T3.id as idMACROP,
                T3.macroprocesso as MACROPROCESS,
                T1.id_type AS idTIPOPROJ, 
                T1.type_proj AS TIPOPROJ,
                T2.id_prog AS IDPROG,
                (SELECT GROUP_CONCAT(nome_prog) FROM projeu_programas WHERE id_prog IN (
                    SELECT distinct(progrm_fgkey) FROM projeu_projetos
                    )) AS PROGPROJT
            FROM 
                projeu_type_proj AS T1
            JOIN 
                projeu_programas AS T2
            JOIN 
                projeu_macropr as T3
            ON 1=1
            GROUP BY T2.id_prog, T3.id, T1.id_type;"""

mycursor.execute(consult1AUX)
consulta1 = mycursor.fetchall()

####### CONSULTANDO AS PORCENTAGENS DOS PRÊMIOS #######
consult2AUX = '''
SELECT 
	projeu_param_premio.id_pp,
    TYP.type_proj,
    PCP.nome_parm,
    projeu_param_premio.typ_event,
    CAST(projeu_param_premio.porc AS DECIMAL(10, 2)) AS porc,
    projeu_param_premio.qntd_event 
FROM 
	projeu_param_premio
JOIN 
	projeu_type_proj TYP ON projeu_param_premio.typ_proj_fgkey = TYP.id_type
JOIN 
	projeu_compl_param PCP ON projeu_param_premio.complx_param_fgkey = PCP.id_compl_param;
'''
mycursor.execute(consult2AUX)
consulta2 = mycursor.fetchall()

####### CONSULTANDO OS VALORES BASES DE PRÊMIOS #######
consult3AUX = '''
SELECT 
	id_premiob,
    TYP.type_proj,
    PPP.nome_parm,
    valor_base
FROM 
	projeu_premio_base
JOIN
	 projeu_type_proj TYP ON projeu_premio_base.typ_proj_fgkey = TYP.id_type
JOIN 
	projeu_compl_param PPP ON projeu_premio_base.complx_param_fgkey = PPP.id_compl_param;
'''
mycursor.execute(consult3AUX)
consulta3 = mycursor.fetchall()

####### CONSULTANDO AS PORCENTAGENS POR FUNÇÃO #######
consult4AUX = """SELECT 
    id_equip,
    tip_fun,
    PPP.nome_parm,
    porcentual
FROM 
    projeu_porc_func
JOIN 
    projeu_compl_param PPP ON PPP.id_compl_param = projeu_porc_func.complx_fgkey
ORDER  BY projeu_porc_func.id_equip;"""
mycursor.execute(consult4AUX)
consulta4 = mycursor.fetchall()

mycursor.close()

################### TRATAMENTO DOS DADOS ###################
    #RETORNO --->IDPROGRAMA,  NOME DO PROGRAMA,  MACROPROCESSO DE PROGRAMA    
progrmBD = [[idPG, list(set([linh[1] for linh in consulta1 if linh[0] == idPG]))[0], list(set([linh1[2] for linh1 in consulta1 if linh1[0] == idPG]))[0], list(set([linh1[3] for linh1 in consulta1 if linh1[0] == idPG]))[0], list(set([linh1[4] for linh1 in consulta1 if linh1[0] == idPG]))[0], list(set([linh1[5] for linh1 in consulta1 if linh1[0] == idPG]))[0], list(set([linh1[10] for linh1 in consulta1 if linh1[0] == idPG]))[0]] for idPG in list(set([x[0] for x in consulta1]))]
    #RETORNO --->IDTYPE,  TIPO DE PROJETO
typProgBD = list(set(tuple([x[8], x[9]]) for x in consulta1))
    #RETORNO --->IDMACRO,  NOME MACROPROCESSO
macroProcBD = list(set(tuple([x[6], x[7]]) for x in consulta1))

#PROGRAMAS PRESENTES NOS PROJETOS
prog_pj = []
for list11 in list(set([x[11] for x in consulta1])):
    for prog in str(list11).split(','):
       prog_pj.append(prog.strip()) 

################### APRESENTAÇÃO DO FRONT ###################
fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
font_TITLE('CADASTRO DE PARÂMETROS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')

ParamEscolh = st.selectbox("Escolha o parâmetro", ["Programas", "Prêmio"])
st.text(' ')
if ParamEscolh == 'Programas':
    col1, col2 = st.columns((3,1.7))
    with col2:
        st.text(' ')
        st.dataframe({ "ID" :[x[0] for x in progrmBD],
                "Nome" : [x[1] for x in progrmBD]})
    with col1:
        tab1, tab2, tab3 = st.tabs(["Adicionar", "Editar",  "Excluir"])
        with tab1:
            font_TITLE('ADICIONAR NOVO PROGRAMA', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left')  
            NewProg = st.text_input("Nome Programa")
            NewMacrop = st.selectbox('Macroprocesso', [x[1] for x in macroProcBD])
            
            colv, colv1, colv2 = st.columns([1,1,2])
            with colv:
                inic_pg = st.date_input('Início Programa')
            with colv1:
                fim_pg = st.date_input('Fim Programa')
            with colv2:
                status_pg = st.selectbox('Status', ['ATIVO', 'DESATIVO', 'CANCELADO'])

            if st.button("Adicionar"):
                if NewProg.strip().lower() not in list(set([str(x[1]).strip().lower() for x in progrmBD])):
                    mycursor = conexao.cursor()
                    cmd_add_prog = f"""INSERT INTO projeu_programas (nome_prog, macroprocesso_fgkey, inic_pg,fim_pg,status_pg)
                                            VALUES (
                                            '{NewProg}',
                                            (SELECT id FROM projeu_macropr WHERE macroprocesso = '{NewMacrop}'),
                                            '{inic_pg}',
                                            '{fim_pg}',
                                            '{status_pg}');"""
                    
                    mycursor.execute(cmd_add_prog)
                    conexao.commit()
                    mycursor.close()     
                    st.toast('Sucesso na adição do novo programa.', icon='✅')
                    st.rerun()
                else:
                    st.toast('Já existe um programa com um nome semelhante.', icon='❌')

        with tab2:
            font_TITLE('EDITAR PROGRAMA', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left')  
            colA, colB = st.columns([1,8])
            with colA: 
                ED_idprogm = st.selectbox('ID', [x[0] for x in progrmBD], key='editar id')
            with colB:
                ED_progrm = st.text_input("Programa", [x[1] for x in progrmBD if str(x[0]) == str(ED_idprogm)][0], key='editar name')
            
            NewMacrop = st.selectbox('Macroprocesso', [x[1] for x in macroProcBD], list([x[1] for x in macroProcBD]).index([x[5] for x in progrmBD if str(x[0]) == str(ED_idprogm)][0]), key='editar macro')
            colv, colv1, colv2 = st.columns([1,1,2])
            with colv:
                ED_inic_pgE = st.date_input('Início Programa', [string_to_datetime(x[2]) if x[2] != None and x[2] != '' else date.today() for x in progrmBD if str(x[0]) == str(ED_idprogm)][0], key='editar inic')
            with colv1:
                ED_fim_pgE = st.date_input('Fim Programa', [string_to_datetime(x[3]) if x[3] != None and x[3] != '' else date.today() for x in progrmBD if str(x[0]) == str(ED_idprogm)][0], key='editar fim')
            with colv2:
                ED_status_pgE = st.selectbox('Status', ['ATIVO', 'DESATIVO', 'CANCELADO'],list(['ATIVO', 'DESATIVO', 'CANCELADO']).index([x[4] for x in progrmBD if str(x[0]) == str(ED_idprogm)][0]),key='editar stats')
           
            if st.button("Editar"):
                mycursor = conexao.cursor()

                values = [f'"{ED_progrm}"', f'(SELECT id FROM projeu_macropr WHERE macroprocesso = "{NewMacrop}")', f'"{ED_inic_pgE}"', f'"{ED_fim_pgE}"', f'"{ED_status_pgE}"']
                columns = ["nome_prog", "macroprocesso_fgkey", "inic_pg", "fim_pg", "status_pg"]
                for colum_idx in range(len(columns)):
                    cmd_up_pg = f'UPDATE projeu_programas SET {columns[colum_idx]} = {values[colum_idx]} WHERE id_prog = {ED_idprogm};'
                    mycursor.execute(cmd_up_pg)
                    conexao.commit()
                
                st.toast('Sucesso na atualização do programa.', icon='✅')  
                mycursor.close()
                st.rerun()

        with tab3:
            font_TITLE('EXCLUIR PROGRAMA', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left') 
            colA, colB = st.columns([1,8])
            with colB:
                EX_progrm = st.selectbox("Programa", [x[1] for x in progrmBD], key='excluir name')
            with colA:  
                EX_idprogm = st.text_input('ID', [x[0] for x in progrmBD if str(x[1]) == EX_progrm][0], key='excluir id', disabled=True)
            
            NewMacrop = st.selectbox('Macroprocesso', [x[1] for x in macroProcBD], list([x[1] for x in macroProcBD]).index([x[5] for x in progrmBD if str(x[0]) == str(EX_idprogm)][0]), key='excluir macro' ,disabled=True)
            colv, colv1, colv2 = st.columns([1,1,2])
            with colv:
                EX_inic_pgE = st.date_input('Início Programa', [string_to_datetime(x[2]) if x[2] != None and x[2] != '' else date.today() for x in progrmBD if str(x[0]) == str(EX_idprogm)][0], key='excluir inic' ,disabled=True)
            with colv1:
                EX_fim_pgE = st.date_input('Fim Programa', [string_to_datetime(x[3]) if x[3] != None and x[3] != '' else date.today() for x in progrmBD if str(x[0]) == str(EX_idprogm)][0], key='excluir fim',disabled=True)
            with colv2:
                EX_status_pgE = st.selectbox('Status', ['ATIVO', 'DESATIVO', 'CANCELADO'],list(['ATIVO', 'DESATIVO', 'CANCELADO']).index([x[4] for x in progrmBD if str(x[0]) == str(EX_idprogm)][0]),key='excluir stats',disabled=True)
           
            if st.button("Excluir"):
                if EX_progrm not in prog_pj:
                    mycursor = conexao.cursor()

                    id_prog = [str(x[6]) for x in progrmBD if x[1] == EX_progrm][0]
                    cmd_ex_pg = f'DELETE FROM projeu_programas WHERE id_prog = {id_prog};'
                    mycursor.execute(cmd_ex_pg)
                    conexao.commit()
                    mycursor.close()     
                    st.toast('Sucesso ao excluir o programa.', icon='✅')
                    
                    st.rerun()
                else:
                    st.toast('Há projetos vinculados a esse programa, assim, tornando impossível a exclusão do programa.', icon='❌')

elif ParamEscolh == 'Prêmio':
    tab1, tab2, tab3 = st.tabs(["Valor Total", "Prêmio por Sprint", "Prêmio por Função"])
    
    with tab1:
        col1, col2 = st.columns([1, 0.5])

        with col1:
            st.text(' ')
            font_TITLE('VALOR BASE POR PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left') 
            
            typ_proj_event = typ_proj = st.selectbox('Tipo de Projeto', [x[1] for x in typProgBD], list([x[1] for x in typProgBD]).index('Estratégico'), key='TYP PROJ VALOR TOTAL')
            complx_event = st.selectbox('Complexidade Projeto', list(set([x[2] for x in consulta3])), key='COMPLX VALOR TOTAL')
            
            dados_dql_param2 = [x for x in consulta3 if x[1] == typ_proj and x[2] == complx_event]
            col_aux, col_aux1 = st.columns([1,8])
            with col_aux:
                id_valor_event = st.text_input('Id Valor', dados_dql_param2[0][0], disabled=True)
            with col_aux1:
                valor_base = st.number_input('Valor Base', min_value=0.00, step=0.01, value=float(dados_dql_param2[0][3]))

        with col2:
            st.text(' ')
            st.dataframe({'ID': [x[0] for x in consulta3 if x[1] == typ_proj],
                          'TIPO PROJETO': [x[1] for x in consulta3 if x[1] == typ_proj],
                          'COMPLEXIDADE PROJETO': [x[2] for x in consulta3 if x[1] == typ_proj],
                          'VALOR BASE': [x[3] for x in consulta3 if x[1] == typ_proj]})
        
        btt_ValorTotal = st.button('Atualizar', key='btt_ValorTotal')
        if btt_ValorTotal:
            mycursor = conexao.cursor()
            cmdUP_vlb = f'UPDATE projeu_premio_base SET valor_base = {float(valor_base)} WHERE id_premiob = {id_valor_event};'
            mycursor.execute(cmdUP_vlb)
            conexao.commit()
            
            st.toast('Sucesso! Valor base atualizado.', icon='✅')
            mycursor.close()
            st.rerun()

    with tab2:
        col1, col2 = st.columns([1.1, 1])
        with col1:
            st.text(' ')
            font_TITLE('ESCOLHA DO PRÊMIO', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left') 

            typ_proj = st.selectbox('Tipo de Projeto', list(set([x[1] for x in consulta2])))
            event_spr = st.selectbox('Tipo Evento', list(set([x[3] for x in consulta2])))
            event_complx = st.selectbox('Complexidade', list(set([x[2] for x in consulta2])), key='UP COMPLX')
    
        with col2:
            st.dataframe({'ID': [x[0] for x in consulta2 if x[1] == typ_proj and x[3] == event_spr],
                          'TIPO PROJETO': [x[1] for x in consulta2 if x[1] == typ_proj and x[3] == event_spr],
                          'EVENTO': [x[3] for x in consulta2 if x[1] == typ_proj and x[3] == event_spr],
                          'COMPLEXIDADE': [x[2] for x in consulta2 if x[1] == typ_proj and x[3] == event_spr],
                          'PORCENTUAL': [x[4] for x in consulta2 if x[1] == typ_proj and x[3] == event_spr],
                          'QNTD EVENTOS': [x[5] for x in consulta2 if x[1] == typ_proj and x[3] == event_spr]})

        st.divider()
        dados_dql_param = [x for x in consulta2 if x[1] == typ_proj and x[3] == event_spr and x[2] == event_complx]
        font_TITLE('MUDAR PARA ', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left')
        
        id_prem = st.text_input('ID Prêmio', [x[0] for x in dados_dql_param][0], disabled=True)
        qntd_event = st.number_input('Quantidade Eventos', min_value=1, step=1, value=int([x[5] for x in dados_dql_param if x[0] == int(id_prem)][0]))
        porct_event = st.number_input('Porcentagem', min_value=0.00, step=0.01, max_value=1.00, value=float([x[4] for x in dados_dql_param if x[0] == int(id_prem)][0]))

        bttUP_premio = st.button('Atualizar', key='bttUP_premio')
        if bttUP_premio:
            mycursor = conexao.cursor()
            columns = ['porc', 'qntd_event']
            values = [porct_event, qntd_event]
            for idx_column in range(len(columns)):
                cmdUP_premio = f"UPDATE projeu_param_premio SET {columns[idx_column]} = {values[idx_column]} WHERE id_pp = {id_prem};"
            
                mycursor.execute(cmdUP_premio)
                conexao.commit()
            
            st.toast('Prêmio Atualizado', icon='✅')
            mycursor.close()
            st.rerun()

    with tab3:        
        col1, col2 = st.columns([2, 0.7])
        with col1:
            st.text(' ')
            font_TITLE('PRÊMIO POR FUNÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left')
            typFUN_proj = st.selectbox('Função', list(set([x[1] for x in consulta4])))
            complxFUN_proj = st.selectbox('Complexidade', list(set([x[2] for x in consulta4])))

            dados_dql_param3 = [x for x in consulta4 if x[1] == typFUN_proj and x[2] == complxFUN_proj]
            col_aux, col_aux1 = st.columns([1,8])
            with col_aux:
                idFUN_porc = st.text_input('ID', dados_dql_param3[0][0] , disabled=True)
            with col_aux1:
                UPporcFUN = st.number_input('Porcentagem', min_value=0.00, step=0.01, max_value=1.00, value=float(dados_dql_param3[0][3]))

        with col2:
            st.text(' ')
            st.dataframe({'ID': [x[0] for x in consulta4 if x[1] == typFUN_proj],
                          'FUNÇÃO': [x[1] for x in consulta4 if x[1] == typFUN_proj],
                          'COMPLEXIDADE': [x[2] for x in consulta4 if x[1] == typFUN_proj],
                          'PORCENTUAL': [x[3] for x in consulta4 if x[1] == typFUN_proj]})
                          
        btt_FUN = st.button('Atualizar', key='btt_FUN')
        if btt_FUN:
            mycursor = conexao.cursor()
            cmdFUN_UP = f"UPDATE projeu_porc_func SET porcentual = {float(UPporcFUN)} WHERE id_equip = {idFUN_porc};"
            
            mycursor.execute(cmdFUN_UP)
            conexao.commit()

            mycursor.close()
            
            st.toast('Prêmio por função atualizado com sucesso.', icon='✅')  
            st.rerun()