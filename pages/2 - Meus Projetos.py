import streamlit as st
from PIL import Image
from datetime import datetime, timedelta, date
from util import font_TITLE, string_to_datetime, cardMyProject, cardGRANDE, date_americ_by_brasil
from collections import Counter
import streamlit_authenticator as stauth
from utilR import PlotCanvas, menuProjeuHtml, menuProjeuCss, CanvaImplantacao, StyleCanvaImplantacao
from time import sleep
from conexao import conexaoBD

icone = Image.open('imagens/LogoProjeu.png')
st.set_page_config(
    page_title="Meus Projetos",
    page_icon=icone,
    layout="wide")


#CONEXÃO COM O BANCO DE DADOS AWS
conexao = conexaoBD()

mycursor = conexao.cursor()

setSession = "SET SESSION group_concat_max_len = 5000;"
mycursor.execute(setSession)

mycursor.execute("""SELECT Matricula, 
                 Nome FROM projeu_users;"""
)
users = mycursor.fetchall()

mycursor.execute('SELECT * FROM projeu_users;')
usersBD = mycursor.fetchall()

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
        SELECT GROUP_CONCAT(number_sprint SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as number_sprint,
    (
        SELECT GROUP_CONCAT(status_sprint SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as status_sprint,
    (
        SELECT GROUP_CONCAT(date_inic_sp SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as inic_sprint,
    (
        SELECT GROUP_CONCAT(date_fim_sp SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as fim_sprint,
    (
        SELECT GROUP_CONCAT(status_homolog SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as status_homolog_sprint,
    (
        SELECT GROUP_CONCAT(nome_Entrega SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as entrega_name,
    (
        SELECT GROUP_CONCAT(executor SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as executor_entrega,
    (
        SELECT GROUP_CONCAT(hra_necess SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as hrs_entrega,
    (
        SELECT GROUP_CONCAT(compl_entrega SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as complex_entreg,
    (
        SELECT GROUP_CONCAT(id_registro SEPARATOR '~/>') 
        FROM projeu_registroequipe 
        WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
        AND projeu_registroequipe.status_reg = 'A'
    ) as id_registro,
    (
        SELECT GROUP_CONCAT(Nome SEPARATOR '~/>') 
        FROM projeu_users 
        WHERE id_user IN (
            SELECT id_colab 
            FROM projeu_registroequipe 
            WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
            AND projeu_registroequipe.status_reg = 'A'
        )
    ) as colaborador,
    (
        SELECT GROUP_CONCAT(papel SEPARATOR '~/>') 
        FROM projeu_registroequipe 
        WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
        AND projeu_registroequipe.status_reg = 'A'
    ) as PAPEL,
    (
        SELECT 
            GROUP_CONCAT(Matricula SEPARATOR '~/>') AS MATRICULA_EQUIPE
        FROM projeu_users AS PU
        INNER JOIN projeu_registroequipe AS PR ON PU.id_user = PR.id_colab 
        WHERE PR.id_projeto = projeu_projetos.id_proj
        AND PR.status_reg = 'A'
    ) as matriculaEQUIPE,
    projeu_projetos.status_proj AS STATUS_PROJETO,
    projeu_projetos.produto_mvp AS PRODUTO_MVP,
    projeu_projetos.prazo_entreg_final,
    (
        SELECT GROUP_CONCAT(id_sprint SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as id_sprint,
    projeu_projetos.date_aprov_proj,
    projeu_projetos.date_posse_gestor,
    projeu_projetos.date_imersao_squad,
    projeu_projetos.status_proj,
    (
		SELECT 
			GROUP_CONCAT(entreg SEPARATOR '~/>') 
		FROM projeu_princEntregas 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			GROUP_CONCAT(name_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS METRICAS,
    (
		SELECT 
			GROUP_CONCAT(projeu_sprints.check_sprint SEPARATOR '~/>') 
		FROM projeu_sprints 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS CHECK_SPRINT,
    (
		SELECT 
			GROUP_CONCAT(projeu_sprints.data_check SEPARATOR '~/>') 
		FROM projeu_sprints 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS DATA_CHECK,
    PC.complxdd AS COMPLEXIDADE_PROJETO,
    PC.nivel AS NIVEL_COMPLEXIDADE,
    projeu_projetos.check_proj,
    (
		SELECT 
			group_concat(PPE.id_princ SEPARATOR '~/>') 
		FROM projeu_princEntregas AS PPE
        WHERE PPE.id_proj_fgkey = projeu_projetos.id_proj
	) AS ID_PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			group_concat(PPE.status_princp SEPARATOR '~/>') 
		FROM projeu_princEntregas AS PPE
        WHERE PPE.id_proj_fgkey = projeu_projetos.id_proj
	) AS STATUS_PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			GROUP_CONCAT(id_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS ID_METRICAS,
    (
		SELECT 
			GROUP_CONCAT(status_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS STATUS_METRICAS,
    (
        SELECT GROUP_CONCAT(IFNULL(check_homolog, 0) SEPARATOR '~/>')
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as CHECK_HOMOLOG_SPRINT,
	(
        SELECT GROUP_CONCAT(IFNULL(check_govern, 0) SEPARATOR '~/>')
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as CHECK_GOVERN,
    projeu_projetos.justific_impl_proj,
    projeu_projetos.stakeholders_impl_proj,
    projeu_projetos.premissas_impl_proj,
    projeu_projetos.riscos_impl_proj,
    projeu_projetos.restric_impl_proj,
    projeu_projetos.objSmart_impl_proj,
    projeu_projetos.requisitos_impl_proj,
    (
        SELECT COALESCE(GROUP_CONCAT(marco_line_tempo SEPARATOR '~/>'), " ") 
        FROM projeu_impl_linhaTempo 
        WHERE projeu_impl_linhaTempo.id_proj_fgkey = projeu_projetos.id_proj 
    ) AS linhaTempo,
    (SELECT id_type FROM projeu_type_proj WHERE id_type = projeu_projetos.type_proj_fgkey) AS id_type_proj,
    (
	 	SELECT 
		 	GROUP_CONCAT(DISTINCT(PPP.typ_event) SEPARATOR '~/>') 
		FROM 
			projeu_param_premio AS PPP 
		WHERE PPP.typ_proj_fgkey = projeu_projetos.type_proj_fgkey
	 ) AS EVENTOS_PROGRAMADOS
FROM 
    projeu_projetos
JOIN 
	projeu_complexidade PC on PC.proj_fgkey = projeu_projetos.id_proj
GROUP BY
    projeu_projetos.id_proj;"""

mycursor.execute(comand)
ddPaging = mycursor.fetchall()

mycursor.execute("""SELECT 
  p.nome_prog, 
  m.macroprocesso
FROM projeu_programas p
JOIN projeu_macropr m ON p.macroprocesso_fgkey = m.id;"""
)
dados_page = mycursor.fetchall()

prog_macro = [list(x) for x in dados_page]

mycursor.execute("SELECT DISTINCT(name_proj) FROM projeu_projetos;")
dd_proj = [x[0] for x in mycursor.fetchall()]

comandUSERS = 'SELECT * FROM projeu_users;'
mycursor.execute(comandUSERS)
dadosUser = mycursor.fetchall()
mycursor.close()

def tratar_name_event(name_event):
    name_event_aux = str(name_event).strip().upper()
    aux = {'SPRINT PÓS MVP': 'PÓS MVP',
           'SPRINT PRÉ MVP': 'PRÉ MVP'}
    
    retorno = aux[name_event_aux] if name_event_aux in list(aux.keys()) else name_event

    return retorno

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
    ddPaging = [x for x in ddPaging if str(matriUser) in str(x[23]).split('~/>') or matriUser == x[3]]
    dados_user = [x for x in usersBD if str(x[1]).strip() == str(matriUser).strip()][0]

    primeiroNome = str(dados_user[2]).strip().split()[0]

    menuHtml = menuProjeuHtml(primeiroNome)
    menuCss = menuProjeuCss()
    st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
    st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

    fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''

    tabs1, tabs2 = st.tabs(['Meus Projetos', 'Cadastrar Projeto'])

    with tabs1:
        if len(ddPaging):
            font_TITLE('MEUS PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
            with st.expander('Filtro Projetos', expanded=False):
                macropr_filter = st.multiselect('Macroprocesso', set([x[5] for x in ddPaging]), set([x[5] for x in ddPaging]))
                program_filter = st.multiselect('Programas', set([x[6] for x in ddPaging if x[5] in macropr_filter]), set([x[6] for x in ddPaging if x[5] in macropr_filter]))
                project_filter = st.selectbox('Projetos', [x[1] for x in ddPaging if x[6] in program_filter])
                
                gestorProj = [x[3] for x in ddPaging if x[1] == project_filter][0]

                dadosOrigin = [x for x in ddPaging if x[1] == project_filter]
                cmd_entregas = f"""
                                    SELECT 
                                        (SELECT number_sprint FROM projeu_sprints WHERE id_sprint = projeu_entregas.id_sprint) AS NUMERO_SPRINT,
                                        nome_Entrega AS NOME_ENTREGA,
                                        (SELECT Nome FROM projeu_users WHERE id_user = executor) AS EXECUTOR,
                                        hra_necess AS HORAS,
                                        compl_entrega AS COMPLEXIDADE,
                                        stt_entrega AS STATUS,
                                        id_entr,
                                        (SELECT Matricula FROM projeu_users WHERE id_user = executor) AS MATRICULA_EXECUTOR,
                                        id_sprint 
                                    FROM 
                                        projeu_entregas 
                                    WHERE 
                                        id_sprint IN (
                                            SELECT id_sprint 
                                            FROM projeu_sprints 
                                            WHERE id_proj_fgkey = (
                                                SELECT id_proj 
                                                FROM projeu_projetos 
                                                WHERE name_proj = '{str(project_filter).strip()}'
                                            )
                                        );
                                    ;"""
                
                cmd_especialist_sprint = f"""SELECT
                                        PES.id_sp, 
                                        PES.id_sprt_fgkey, 
                                        PS.number_sprint,
                                        PES.id_colab_fgkey, 
                                        PU.Matricula,
                                        PU.Nome,
                                        PES.status_sp
                                    FROM projeu_especialist_sprint PES
                                    JOIN projeu_users PU ON PU.id_user = PES.id_colab_fgkey
                                    JOIN projeu_sprints PS ON PS.id_sprint = PES.id_sprt_fgkey
                                    WHERE PS.id_proj_fgkey IN (SELECT PP_AUX.id_proj FROM projeu_projetos PP_AUX WHERE PP_AUX.name_proj LIKE '%{str(dadosOrigin[0][1]).strip()}%');"""
            
            if len(dadosOrigin) > 0:
                mycursor = conexao.cursor()  
                mycursor.execute(cmd_entregas)
                EntregasBD = mycursor.fetchall()

                mycursor.execute(cmd_especialist_sprint)
                especialist_by_proj = mycursor.fetchall()
                
                mycursor.close()

                tab1, tab2 = st.tabs(['Canvas', 'Editar'])
                with tab1:
                    font_TITLE(f'{dadosOrigin[0][1]}', fonte_Projeto,"'Bebas Neue', sans-serif", 31, 'center', '#228B22')
                    ########CANVAS DO PROJETO SELECIONADO########
                    projetos = [dadosOrigin[0][1]] if dadosOrigin[0][1] != None else " "
                    mvps = [dadosOrigin[0][7]] if dadosOrigin[0][7] != None else " "  
                    investimentos = [f"{dadosOrigin[0][8]}"] if f"{dadosOrigin[0][8]}" != None else " "
                    gestores = [f"{dadosOrigin[0][2]}"] if f"{dadosOrigin[0][2]}" != None else " "
                    
                    pessoas = str(dadosOrigin[0][21]).split("~/>") if dadosOrigin[0][21] != None else ' '
                    funcao = str(dadosOrigin[0][22]).split("~/>") if dadosOrigin[0][22] != None else ' '
                    equipBD = [[pessoas[x], funcao[x]] for x in range(len(pessoas))]

                    resultados = []
                    for i in range(len(dadosOrigin)):
                        if dadosOrigin[i][9] != None:
                            resultados.append(f"{dadosOrigin[i][9]}")
                        else:
                            resultados = " "
                    
                    if dadosOrigin[0][32] != None:
                        entregas = [str(dadosOrigin[0][32]).split("~/>")[x] for x in range(len(str(dadosOrigin[0][40]).split("~/>"))) if str(str(dadosOrigin[0][40]).split("~/>")[x]).strip() == 'A']
                    else:
                        entregas = ' '

                    metricas = [str(dadosOrigin[0][33]).split("~/>")[x] for x in range(len(str(dadosOrigin[0][33]).split("~/>"))) if str(str(dadosOrigin[0][42]).split("~/>")[x]).strip() == 'A'] if dadosOrigin[0][33] != None else ' '
                    prodProjetos = str(dadosOrigin[0][10]).split("~/>") if dadosOrigin[0][10] != None else " "
                    prodMvps = str(dadosOrigin[0][25]).split("~/>") if dadosOrigin[0][25] != None else " "
                        
                    if dadosOrigin[0][4] == "Implantação":
                        dadosImplantacao = [[dadosOrigin[0][45]], [dadosOrigin[0][10]], [dadosOrigin[0][46]], [dadosOrigin[0][47]], [dadosOrigin[0][48]], [dadosOrigin[0][50]], [dadosOrigin[0][51]], dadosOrigin[0][21].split("~/>"), dadosOrigin[0][32].split("~/>"), dadosOrigin[0][52].split("~/>"), [dadosOrigin[0][9]], [dadosOrigin[0][49]], [dadosOrigin[0][8]]]
                
                        html = CanvaImplantacao(dadosImplantacao)
                        css = StyleCanvaImplantacao()

                        st.write(f'<div>{html}</div>', unsafe_allow_html=True)
                        st.write(f'<style>{css}</style>', unsafe_allow_html=True)
                    else:
                        #SEQUÊNCIA --> projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, especialistas, squads, entregas, investimentos
                        canvas = PlotCanvas(projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, [x[0] for x in equipBD if x[1] == 'Especialista'], [x[0] for x in equipBD if x[1] == 'Executor'], entregas, investimentos)
                        htmlRow = canvas.CreateHTML()
                        htmlEqp = canvas.tableEqp()
                        htmlUnic = canvas.tableUnic()
                        htmlCol = canvas.tableCol()

                        html = canvas.tableGeral(htmlRow, htmlEqp, htmlUnic, htmlCol)
                        canvaStyle = canvas.cssStyle(mvps, prodMvps)

                        st.write(f'<div>{html}</div>', unsafe_allow_html=True)
                        st.write(f'<style>{canvaStyle}</style>', unsafe_allow_html=True)

                with tab2:
                    if str(matriUser).strip() in [str(dadosOrigin[0][3]).strip(), '56126']:
                    
                        def status_aux(sigla_status, func=0):
                            dic_aux = {'A': 'Ativo',
                                        'I': 'Inativo',
                                        'E': 'Irregular'}
                            
                            if func == 0:
                                retorno = dic_aux[str(sigla_status).strip().upper()] if str(sigla_status).strip().upper() in list(dic_aux.keys()) else 'Irregular'
                            else:
                                dic_invertido = {valor: chave for chave, valor in dic_aux.items()}
                                retorno = dic_invertido[str(sigla_status).strip()]
                            
                            return retorno

                        font_TITLE(f'EDITAR CANVAS', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left', 'black')
                        nomeproj_edit = st.text_input('Nome Projeto', projetos[0])
                        produtproj_edit = st.text_area('Produto Projeto', str(prodProjetos[0]).strip())
                        if dadosOrigin[0][4] != "Rápido":
                            mvp_edit = st.text_input('MVP', mvps[0])
                            produtmvp_edit = st.text_input('Produto MVP', prodMvps[0])
                        Resultado_edit = st.text_input('Resultado Esperado', resultados[0])
                        
                        ############################# MÉTRICAS #############################
                        font_TITLE(f'MÉTRICAS', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left', 'black')
                        
                        metricas_bd = [(str(dadosOrigin[0][41]).split("~/>")[x], str(dadosOrigin[0][33]).split("~/>")[x], str(dadosOrigin[0][42]).split("~/>")[x]) for x in range(len(str(dadosOrigin[0][41]).split("~/>"))) if str(dadosOrigin[0][41]).split("~/>")[x] != 'None']
                        qntd_metrc_edit = st.number_input('Quantidade', key='qntd Métricas', min_value=0, step=1, value=len(metricas_bd))
                        if qntd_metrc_edit > len(metricas_bd):
                            metricas_bd.extend([(None, '', 'A') for x in range(qntd_metrc_edit - len(metricas_bd))])

                        list_metric_edit = []
                        if qntd_metrc_edit > 0:
                            col1, col2 = st.columns([4,1])
                            with col1:
                                st.caption('Métrica')
                            with col2:
                                st.caption('Status')

                            for idx_metr in range(qntd_metrc_edit):
                                with col1:
                                    edit_metric_name = st.text_input('metricas_edit', value=metricas_bd[idx_metr][1], label_visibility='collapsed', key=f'edit metric {idx_metr}') 
                                with col2:
                                    edit_metric_status = st.selectbox('status_edit', ['Ativo', 'Inativo', 'Irregular'], ['Ativo', 'Inativo', 'Irregular'].index(status_aux(str(metricas_bd[idx_metr][2]).strip())), label_visibility='collapsed', key=f'edit status {idx_metr}')
                                list_metric_edit.append([metricas_bd[idx_metr][0], edit_metric_name, edit_metric_status])
            
                        ############################ ENTREGAS #############################
                        st.text(' ')
                        font_TITLE(f'PRINCIPAIS ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left', 'black')
                        
                        #ENTREGAS ORIGINAIS DO BANCO DE DADOS
                        
                        entregas_bd = [(str(dadosOrigin[0][39]).split("~/>")[x],  str(dadosOrigin[0][32]).split("~/>")[x], str(dadosOrigin[0][40]).split("~/>")[x]) for x in range(len(list(str(dadosOrigin[0][39]).split("~/>")))) if str(dadosOrigin[0][39]).split("~/>")[x] != None and str(dadosOrigin[0][39]).split("~/>")[x] != 'None']
                        qntd_princ_edit = st.number_input('Quantidade', key='qntd Principais entregas', min_value=0, step=1, value=len(entregas_bd))
                        entregas = list(entregas_bd)
                        if qntd_princ_edit > len(entregas): #PEGANDO A QUANTIDADE DE VEZES A MAIS QUE O USUÁRIO SELECIONOU E ADCIONANDO NA MINHA LISTA
                            entregas.extend([(None, '', 'A') for x in range(qntd_princ_edit - len(entregas))])
                            
                        list_entreg_edit = []
                        if qntd_princ_edit > 0:
                            
                            col1, col2 = st.columns([4,1])
                            with col1:
                                st.caption('Entrega')
                            with col2:
                                st.caption('Status')

                            for idx_princ_i in range(qntd_princ_edit):                        
                                with col1:
                                    mome_edit = st.text_input('principais_edit', value=entregas[idx_princ_i][1], label_visibility='collapsed', key=f'edit principais entreg{idx_princ_i}')
                                with col2:
                                    status_edit = st.selectbox('status_edit', ['Ativo', 'Inativo', 'Irregular'], ['Ativo', 'Inativo', 'Irregular'].index(status_aux(str(entregas[idx_princ_i][2]).strip())) ,label_visibility='collapsed', key=f'edit status entreg{idx_princ_i}')
                                list_entreg_edit.append((entregas[idx_princ_i][0], mome_edit, status_edit))

                        list_metric_edit = [x for x in list_metric_edit if len(str(x[1]).strip()) > 0]
                        list_entreg_edit = [x for x in list_entreg_edit if len(str(x[1]).strip()) > 0]
                        edit_canv_button = st.button('Enviar')
                        if edit_canv_button:
                            mycursor_edit = conexao.cursor()
                            ###################### FAZENDO A ATUALIZAÇÃO DAS INFORMAÇÕES GERAIS DO PROJETO ######################
                            columns1 = ['name_proj', 'produto_entrega_final', 'nome_mvp', 'produto_mvp', 'result_esperad']
                            values = [nomeproj_edit, produtproj_edit, mvp_edit, produtmvp_edit, Resultado_edit]
                            values_aux = [projetos[0], str(prodProjetos[0]).strip(), mvps[0], prodMvps[0], resultados[0]]
                            
                            #LISTA range_aux VAI RETORNAR 1 ONDE O INDEX DOS VALORES FOR DIFERENTE DOS VALORES ANTIGOS
                            #A IDEIA É DESCOBRIR EM QUAL INDEX ESTÁ O VALOR DIFERENTE E SOMENTE USAR O UPDATE ONDE DE FATO OUVER ALGUMA DIFERENÇA
                            range_aux = [1 if str(values[x]).strip() != str(values_aux[x]).strip() else 0 for x in range(len(values))]
                            for idx_clm in range(len(columns1)):
                                if range_aux[idx_clm] == 1:         
                                    cmd = f'UPDATE projeu_projetos SET {columns1[idx_clm]} = {values[idx_clm]} WHERE id_proj = {dadosOrigin[0][0]};'
                                    
                                    mycursor_edit.execute(cmd)
                                    conexao.commit()

                            ###################### FAZENDO ATUALIZAÇÃO DAS PRINCIPAIS ENTREGAS DO PROJETO ######################
                            for idx_entrg_edit in range(len(list_entreg_edit)):
                                if list_entreg_edit[idx_entrg_edit][0] == None:
                                    cmd_insert_entrg = f'INSERT INTO projeu_princEntregas(entreg, id_proj_fgkey) VALUES ("{list_entreg_edit[idx_entrg_edit][1]}", {dadosOrigin[0][0]});'
                                    mycursor_edit.execute(cmd_insert_entrg)
                                    conexao.commit()

                                else:
                                    id_entrg = list_entreg_edit[idx_entrg_edit][0]
                                    entr_original = [x for x in entregas_bd if x[0] == id_entrg]
                                    entr_editadad = [(x[0], x[1], status_aux(x[2], 1)) for x in list_entreg_edit if x[0] == id_entrg]
                                    
                                    if sum([1 if entr_original[x] != entr_editadad[x] else 0 for x in range(len(entr_original))]) > 0: #DESCOBRINDO SE HÁ ALGUMA DIFERENÇA ENTRE A LISTA ORIGINAL E A LISTA EDITADO
                                        cmd_edit_entrg = f'UPDATE projeu_princEntregas SET entreg = "{entr_editadad[0][1]}", status_princp = "{entr_editadad[0][2]}" WHERE id_princ = {entr_editadad[0][0]};'
                                        
                                        mycursor_edit.execute(cmd_edit_entrg)
                                        conexao.commit()
                            
                            ###################### FAZENDO ATUALIZAÇÃO DAS MÉTRICAS DO PROJETO ######################
                            for idx_metric_edit in range(len(list_metric_edit)):
                                if list_metric_edit[idx_metric_edit][0] == None:
                                    cmd_insert_metrc = f'INSERT INTO projeu_metricas (id_prj_fgkey, name_metric) VALUES ({dadosOrigin[0][0]} ,"{list_metric_edit[idx_metric_edit][1]}");'
                                    
                                    mycursor_edit.execute(cmd_insert_metrc)
                                    conexao.commit()
                                
                                else:
                                    id_metric = list_metric_edit[idx_metric_edit][0]
                                    metric_original = [x for x in metricas_bd if x[0] == id_metric]
                                    metric_editadad = [(x[0], x[1], status_aux(x[2], 1)) for x in list_metric_edit if x[0] == id_metric]
                                    
                                    if sum([1 if metric_original[x] != metric_editadad[x] else 0 for x in range(len(metric_original))]) > 0: #DESCOBRINDO SE HÁ ALGUMA DIFERENÇA ENTRE A LISTA ORIGINAL E A LISTA EDITADO
                                        cmd_edit_metric = f'UPDATE projeu_metricas SET name_metric = "{metric_editadad[0][1]}", status_metric = "{metric_editadad[0][2]}" WHERE id_metric = {metric_editadad[0][0]};'
                                        
                                        mycursor_edit.execute(cmd_edit_metric)
                                        conexao.commit()

                            st.toast('Canvas Atualizado!', icon='✅') 
                            mycursor_edit.close()

                        st.divider()
                    else:
                        st.error('VISUALIZAÇÃO NÃO DISPONÍVEL PARA SEU PERFIL.', icon='❌')

                st.text(' ')
                st.text(' ')
                
                func_split = lambda x: x.split("~/>") if x is not None else [x]
                #ESPAÇO PARA MANIPULAR OS COLABORADORES VINCULADOS À AQUELE PROJETO
                with st.expander('Equipe do Projeto'):
                    matriculasEQUIP = func_split(dadosOrigin[0][23])

                    equipe_atual = {matriculasEQUIP[idx_mat]: [matriculasEQUIP[idx_mat], func_split(dadosOrigin[0][21])[idx_mat], func_split(dadosOrigin[0][22])[idx_mat],  func_split(dadosOrigin[0][20])[idx_mat]] for idx_mat in range(len(matriculasEQUIP)) if matriculasEQUIP[idx_mat] != str(dadosOrigin[0][3]).strip()}

                    tab1, tab2 = st.tabs(['Adcionar', 'Excluir'])
                    
                    with tab1:
                        col1, col2 = st.columns([3,1])
                        with col2:
                            qntd_clb = st.number_input('Quantidade', min_value=0, step=1)
                        
                        for a in range(qntd_clb):
                            equipe_atual[f'{a}'] = [None, None, 'Executor']        

                        with st.form('FORMS ATUALIZAR EQUIPE'):
                                
                            col_equip1, col_equip2, col_equip3 = st.columns([0.3, 2, 1])
                            with col_equip1:
                                st.caption('Matricula')
                            with col_equip2:
                                st.caption('Colaboradores')
                            with col_equip3:
                                st.caption('Função')

                            list_colbs = []
                            equipe_list = [x for x in equipe_atual.values()]

                            for colb_a in range(len(equipe_list)):
                                with col_equip2:
                                    colb_name = st.selectbox('Colaboradores', [x[1] for x in users], list([x[1] for x in users]).index(equipe_list[colb_a][1]) if equipe_list[colb_a][0] != None else None,label_visibility="collapsed", key=f'Nome Colab{colb_a}')        
                                with col_equip1:
                                    colab_matric = st.text_input('Matricula', list(set([x[0] for x in users if x[1] == colb_name]))[0] if colb_name != None else None, label_visibility="collapsed", disabled=True, key=f'MatriculaColabs{colb_a}')
                                with col_equip3:
                                    colb_funç = st.selectbox('Função', ['Especialista', 'Executor'],list(['Especialista', 'Executor']).index(equipe_list[colb_a][2]) if colb_name != None else None, label_visibility="collapsed", key=f'funcaoColab{colb_a}')
                                list_colbs.append([colab_matric, colb_funç])
                            
                            button_att_equipe = st.form_submit_button('Atualizar')
                            if button_att_equipe:
                                equipe_limp = [x for x in list_colbs if str(x[0]).strip() != '0']
                                mycursor = conexao.cursor()

                                for matric, func in equipe_limp:
                                    if str(matric).strip() in [str(x).strip() for x in equipe_atual.keys()]: #VERIFICANDO SE O COLABORADOR JÁ ESTÁ VINCULADO A EQUIPE
                                                                        
                                        if str(equipe_atual[matric][2]).strip() != str(func).strip(): #VERIFICANDO SE OUVE ALGUMA MUDANÇA NOS COLABORADORES JÁ VINCULADOS        
                                            cmd_att_equipe = f'UPDATE projeu_registroequipe SET papel = "{func}" WHERE id_registro = {equipe_atual[matric][3]}'
                                            mycursor.execute(cmd_att_equipe)
                                            conexao.commit()
                                    
                                    else: #SE FOR UM COLABORADOR NOVO NA EQUIPE
                                        cmd_new_equip = f'''INSERT INTO projeu_registroequipe(id_projeto, id_colab, papel)
                                                        VALUES (
                                                            {dadosOrigin[0][0]}, 
                                                            (SELECT id_user FROM projeu_users WHERE Matricula = {matric}), 
                                                            '{func}');'''
                                        mycursor.execute(cmd_new_equip)
                                        conexao.commit()
                                    
                                mycursor.close()
                                st.toast('Equipe Atualizada!', icon='✅') 
                    with tab2:                
                        font_TITLE('EXCLUIR COLABORADOR DA EQUIPE', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')

                        if len(equipe_atual) > 0:
                        
                            st.text(' ')
                            col1, col2, col3 = st.columns([0.6,3,2])
                            with col2:
                                colab_ex = st.selectbox('Colaborador', [str(x[1]).strip() for x in equipe_atual.values()])                
                            with col1:
                                matric_ex = st.text_input('Matricula', [x[0] for x in users if str(x[1]).strip().lower() == str(colab_ex).strip().lower()][0], disabled=True)
                            with col3:
                                funca_ex = st.text_input('Função', equipe_atual[matric_ex][2], disabled=True)

                            button_ex_equip = st.button('Excluir', key='EXCLUIR COLABORADOR DO PROJETO')
                            if button_ex_equip:
                                mycursor = conexao.cursor()
                                cmd_ex_equip = f'UPDATE projeu_registroequipe SET status_reg = "I" WHERE id_registro = {equipe_atual[matric_ex][3]};'

                                mycursor.execute(cmd_ex_equip)
                                conexao.commit()

                        else:
                            st.error('Não há colaboradores vinculados a equipe do projeto.', icon='❌')


                #####APRESENTANDO HORAS TOTAIS GASTAS NO PROJETO DAQUELE COLABORADOR
                st.text(' ')
                font_TITLE('MEU DESEMPENHO NO PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 40, 'left', '#228B22')
                
                dffMyProject = Counter([x[4] for x in EntregasBD if x[7] == matriUser]) if len([x for x in EntregasBD if x[7] == matriUser]) > 0 else Counter(['-'])
                dif_comum = dffMyProject.most_common(1)
                complexidade = dif_comum[0][0]
                cardMyProject(f'{name}', [len([x for x in EntregasBD if x[7] == matriUser]), len([x for x in EntregasBD if str(x[5]).strip() == "🟩 Concluído" and x[7] == matriUser]), sum([x[3] for x in EntregasBD if x[7] == matriUser]), complexidade])
                ###APRESENTANDO DESEMPENHO POR SPRINT
                st.text(' ')
                st.text(' ')

                param_sprint_aux = [str(tratar_name_event(x)).strip().upper() for x in list(str(dadosOrigin[0][54]).split("~/>"))]

                eventos_aux_sorted = ['SPRINT', 'PRÉ MVP', 'MVP', 'PÓS MVP', 'ENTREGA FINAL']

                if int(dadosOrigin[0][53]) == 3:
                    eventos_aux_sorted = ['SPRINT PRÉ MARCO 1', 'MARCO 1', 'SPRINT PRÉ MARCO 2', 'MARCO 2', 'SPRINT PRÉ MARCO 3', 'MARCO 3', 'SPRINT PRÉ MARCO 4', 'MARCO 4', 'SPRINT PRÉ MARCO 5', 'MARCO 5', 'SPRINT PRÉ MARCO 6', 'MARCO 6', 'SPRINT PRÉ MARCO 7', 'MARCO 7', 'SPRINT PRÉ MARCO 8', 'MARCO 8']
                    param_sprint_aux = list(set([str(x).strip() for x in str(dadosOrigin[0][12]).split("~/>")] + [eventos_aux_sorted[eventos_aux_sorted.index([str(x).strip() for x in str(dadosOrigin[0][12]).split("~/>")][-1])+1]] if dadosOrigin[0][12] != None else ['SPRINT PRÉ MARCO 1']))
                    
                    eventos_aux_sorted = ['SPRINT PRÉ MARCO 1', 'MARCO 1', 'SPRINT PRÉ MARCO 2', 'MARCO 2', 'SPRINT PRÉ MARCO 3', 'MARCO 3', 'SPRINT PRÉ MARCO 4', 'MARCO 4', 'SPRINT PRÉ MARCO 5', 'MARCO 5', 'SPRINT PRÉ MARCO 6', 'MARCO 6', 'SPRINT PRÉ MARCO 7', 'MARCO 7', 'SPRINT PRÉ MARCO 8', 'MARCO 8']

                param_sprint = [str(x).strip().upper() for x in eventos_aux_sorted if str(x).strip().upper() in param_sprint_aux]
                font_TITLE('SPRINTS DO PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left', '#228B22')
                with st.expander('Adcionar Sprint'):
                    #FUNÇÃO PARA IDENTIFICAR SE A COLUNA DO BANCO DE DADOS ESTÁ VAZIA 
                    maior_idx = max([param_sprint.index(x)+1 if x != None else 0 for x in func_split(dadosOrigin[0][12])])
        
                    if None in func_split(dadosOrigin[0][11]):
                        on_ex = False
                    else:    
                        on_ex = st.toggle('Excluir sprint')

                    listAddSprOF_EX = [max([int(x) for x in func_split(dadosOrigin[0][11]) if x != None]) if len([int(x) for x in func_split(dadosOrigin[0][11]) if x != None]) != 0 else 0, param_sprint[:maior_idx+1], datetime.today()]
                    
                    listAddSprON_EX = [[int(x) if x != None else '' for x in func_split(dadosOrigin[0][11])], func_split(dadosOrigin[0][12]), [string_to_datetime(x) if x != None and x != " " else datetime.today() for x in func_split(dadosOrigin[0][13])]]

                    disabledON = True if on_ex else False
                    disabledOF = False if on_ex else True

                    col0, col1, col2, col3 = st.columns([0.5,3,1,1])
                    with col1:
                        opc_event = [listAddSprON_EX[1][-1:]][0] if on_ex else listAddSprOF_EX[1]
                        type_sprint_new = st.selectbox('Tipo', opc_event, len(opc_event) - 1 if opc_event[len(opc_event) - 1] != 'ENTREGA FINAL' else opc_event.index(opc_event[opc_event.index('ENTREGA FINAL')-1]), disabled=disabledON)
                    
                    with col0:
                        number_sprt =listAddSprOF_EX[0] + 1 if type_sprint_new not in ('MVP', 'ENTREGA FINAL', 'MARCO 1', 'MARCO 2', 'MARCO 3', 'MARCO 4', 'MARCO 5', 'MARCO 6', 'MARCO 7', 'MARCO 8') else None
                        number_sprint_new = st.text_input('Sprint', listAddSprON_EX[0][-1:][0] if on_ex else number_sprt, disabled=True)

                    with col2:
                        dat_inc_new = st.date_input('Início', value=listAddSprON_EX[2][-1:][0] if on_ex else listAddSprOF_EX[2], disabled=disabledON)
                    with col3:
                        dat_fim_new = st.date_input('Fim', value=dat_inc_new + timedelta(days=14), disabled=True)
                    
                    colAdd, colExc = st.columns([1,7])
                    with colAdd:
                        button_addSprint = st.button('Adcionar Sprint', disabled=disabledON)
                    with colExc:
                        button_exSprint = st.button('Excluir Sprint', disabled=disabledOF)

                    if button_addSprint:
                        mycursor = conexao.cursor()
                        columns = 'id_proj_fgkey, status_sprint, date_inic_sp, date_fim_sp'
                        values = f'''{dadosOrigin[0][0]}, '{type_sprint_new}', STR_TO_DATE('{dat_inc_new}', '%Y-%m-%d'), STR_TO_DATE('{dat_fim_new}', '%Y-%m-%d')'''
                        
                        if number_sprint_new != None:
                            columns += ', number_sprint'
                            values += f', {number_sprint_new}'

                        cmd_addSprint = f'''INSERT INTO projeu_sprints({columns}) 
                        VALUES ({values});'''
                        
                        mycursor.execute(cmd_addSprint)
                        conexao.commit()
                        
                        if number_sprint_new == str(1):
                            cmdUP_stt_proj = f'UPDATE projeu_projetos SET status_proj = "Em Andamento" WHERE id_proj = {dadosOrigin[0][0]};'
                            mycursor.execute(cmdUP_stt_proj)
                            conexao.commit()
                            
                        mycursor.close()
                        st.toast('Sucesso na adição da sprint!', icon='✅')
                        st.text(' ')
                        sleep(0.1)
                        st.rerun()

                    if button_exSprint:
                        NotEntrg = False
                        if on_ex:
                            mycursor = conexao.cursor()

                            if str(listAddSprOF_EX[0]) not in [str(str(dadosOrigin[0][11]).split("/>")[x]).strip() for x in range(len(str(dadosOrigin[0][27]).split("/>"))) if str(str(dadosOrigin[0][43]).split("~/>")[x]).strip() == '1']:
                                
                                #CHECANDO SE HÁ ENTREGAS VINCULADAS A SPRINT
                                if len(EntregasBD) == 0:
                                    NotEntrg = True
                                else:
                                    NotEntrg = True if number_sprint_new not in list(set([x[0] for x in EntregasBD])) else False
                                
                                if NotEntrg:
                                    cmdDEL = f'''DELETE FROM projeu_sprints 
                                                WHERE number_sprint = {number_sprint_new} 
                                                AND id_proj_fgkey = {dadosOrigin[0][0]} 
                                                AND status_sprint = '{type_sprint_new}'
                                                AND date_inic_sp = STR_TO_DATE('{dat_inc_new}', '%Y-%m-%d')
                                                AND date_fim_sp = STR_TO_DATE('{dat_fim_new}', '%Y-%m-%d');'''                
                                    
                                    mycursor.execute(cmdDEL)
                                    conexao.commit()

                                    st.toast('Excluido!', icon='✅') 
                                    sleep(0.1)
                                    st.rerun()
                                else:
                                    st.toast('Primeiramente, é necessário excluir todas as atividades dessa sprint.', icon='❌')
                            else:
                                st.toast('Sprint já homologada, calculo de bonificação do projeto realizado.', icon='❌')
                            mycursor.close()
                        else:
                            st.toast('Primeiramente, ative a opção de excluir sprint.', icon='❌')
        
                if func_split(dadosOrigin[0][11])[0] != None:
                    
                    # ----> DADOS [NUMBER_SPRINT, STATUS_SPRINT,  DATA INC SPRINT, DATA FIM SPRINT]
                    sprints = [[func_split(dadosOrigin[0][11])[x], param_sprint.index(func_split(dadosOrigin[0][12])[x]), func_split(dadosOrigin[0][13])[x], func_split(dadosOrigin[0][14])[x], func_split(dadosOrigin[0][27])[x], func_split(dadosOrigin[0][34])[x]] for x in range(len(func_split(dadosOrigin[0][11])))]
                    
                    for idx_parm in range(len(param_sprint)):
                        ddSprint = [sprints[x] for x in range(len(sprints)) if str(sprints[x][1]) == str(idx_parm)] #DESCOBRINDO QUAL A SPRINT DAQUELE STATUS
                        
                        #FUNÇÃO PARA LIMPAR AS ENTREGAS DAQUELA SPRINT 
                        # ----> DADOS [NUMBER_SPRINT, NOME_ENTREGA, EXECUTOR, HORAS, COMPLEXIDADE, STATUS]
                        SpritNotEntreg = [[int(sprt), None, None, 0 , '---', '🟨 Backlog', None] for sprt in [i[0] for i in ddSprint] if sprt not in list(set([ab_x[0] for ab_x in EntregasBD]))]
                        
                        SprintsEntregs = [list(x) for x in EntregasBD if str(x[0]) in [str(i[0]) for i in ddSprint]]
                        
                        SprintsEntregs.extend(SpritNotEntreg)
                        if len(ddSprint)> 0:
                            font_TITLE(f'{param_sprint[idx_parm]}', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')

                            for idx_spr in [int(x[0]) for x in ddSprint]:

                                
                                listDadosAux = []

                                def aux_name(name_expader):
                                    name = str(name_expader).strip()
                                    aux = {'MVP': 'Evento - MVP',
                                        'ENTREGA FINAL': 'Evento - ENTREGA FINAL'}
                                    
                                    if name in list(aux.keys()):
                                        retorno = aux[name]
                                    else:
                                        retorno = name

                                    return retorno

                                name_evento = f'Sprint {int(ddSprint[[x[0] for x in ddSprint].index(str(idx_spr))][0])}' if str(param_sprint[idx_parm]).strip() not in ('MVP', 'ENTREGA FINAL', 'MARCO 1','MARCO 2','MARCO 3','MARCO 4','MARCO 5','MARCO 6','MARCO 7','MARCO 8') else aux_name(param_sprint[idx_parm])
                                with st.expander(name_evento):

                                    id_sprint = [x[4] for x in ddSprint if str(x[0]).strip() == str(idx_spr).strip()][0]
                                    
                                    #FILTRANDO ENTREGAS DAQUELA SPRINT
                                    spEntregas = [x for x in SprintsEntregs if x[0] == idx_spr]

                                    numSprint = dadosOrigin[0][11].split("~/>")
                                    sprintAtual = numSprint.index(str(idx_spr))

                                    checkSprint = dadosOrigin[0][34].split("~/>")
                                    checkGovern = dadosOrigin[0][44].split("~/>")
                                    checkHomolog = dadosOrigin[0][43].split("~/>")
                                    
                                    #PREPARANDO OS DADOS PARA APRESENTAR NO CARD DA SPRINT
                                    contagem_dif = Counter([x[4] for x in spEntregas])                
                                    dif_comum = contagem_dif.most_common(1)

                                    block_sprint = True if str(ddSprint[list(x[4] for x in ddSprint).index(id_sprint)][5]) == str(0) else False

                                    porc_avan = f'{int((len([x for x in spEntregas if str(x[5]).strip() == "🟩 Concluído"]) / len([x for x in spEntregas if x[1] != None])) * 100) if len([x for x in spEntregas if x[1] != None]) > 0 else 0}%'           
                                    cardGRANDE(['Colaboradores', 'Atividades', 'Entregues', 'Avanço', 'Horas', 'Complexidade'], [len(list(set([x[2] for x in spEntregas if x[2] != None]))), len([x for x in spEntregas if x[1] != None]), len([x for x in spEntregas if str(x[5]).strip() == '🟩 Concluído']), porc_avan, sum([x[3] for x in spEntregas]), mapear_dificuldade(dif_comum[0][0])])
                            
                                    st.text(' ')
                                    colPROJ1, colPROJ2, colPROJ3, colPROJ4 = st.columns([4, 2, 0.8, 0.8])
                                    with colPROJ1:
                                        font_TITLE('ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                                    with colPROJ2:
                                        if str(checkSprint[sprintAtual]) == "1":
                                            font_TITLE('STATUS DA SPRINT - EM ANDAMENTO', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                                        elif str(checkSprint[sprintAtual]) == "0" and str(checkGovern[sprintAtual]) == "0" and str(checkHomolog[sprintAtual]) == "0":
                                            font_TITLE('STATUS DA SPRINT - AGUARDANDO GOVERNANÇA', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                                        elif str(checkHomolog[sprintAtual]) == "1":
                                            font_TITLE('STATUS DA SPRINT - HOMOLOGADO', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                                        elif str(checkGovern[sprintAtual]) == "1":
                                            font_TITLE('STATUS DA SPRINT - AGUARDANDO HOMOLOGAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                                    with colPROJ3:
                                        
                                        font_TITLE(f'{date_americ_by_brasil(str(ddSprint[[x[4] for x in ddSprint].index(str(id_sprint))][2]))}', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                                    with colPROJ4:
                                        font_TITLE(f'{date_americ_by_brasil(str(ddSprint[[x[4] for x in ddSprint].index(str(id_sprint))][3]))}', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')

                                    especialistBD_sprint = [x for x in especialist_by_proj if str(x[1]) == str(id_sprint)]  #ESPECIALISTAS ATIVOS E NÃO ATIVOS VINCULADOS A SPRINT                        
                            
                                    especialist_proj = [list(func_split(dadosOrigin[0][21]))[x] for x in range(len(func_split(dadosOrigin[0][22]))) if str(list(func_split(dadosOrigin[0][22]))[x]).upper() == 'ESPECIALISTA']
                                    
                                    especialist_opc = especialist_proj if len(especialistBD_sprint) == 0 else [str(x[5]).strip() for x in especialistBD_sprint if str(x[6]).strip() == 'A']
                    
                                    especialist_sprint = st.multiselect('Especialistas', list(set(especialist_proj)), list(set(especialist_opc)), key=f'especialista multi{id_sprint}')
                                    
                                    def tratamento_especialist():
                                        for espec_bd in especialist_proj:
                                            espec_bd = str(espec_bd).strip()
                                            dd_espec = {matric: lista for matric, lista in dict(equipe_atual).items() if str(lista[1]).strip() == str(espec_bd)} 
                                            
                                            matricula_especil = str(list(dict(dd_espec).keys())[0]).strip()

                                            cmd_aux = None
                                            matric_all_espc = [str(x[4]) for x in especialistBD_sprint] #MATRICULA DE TODOS OS ESPECIALISTAS VINCULADOS A SPRINT
                                            
                                            if matricula_especil not in matric_all_espc and espec_bd in [str(x).strip() for x in especialist_sprint]: #SE SIM, NOVO ESPECIALISTA
                                                cmd_aux = f'''
                                                        INSERT INTO projeu_especialist_sprint (
                                                            id_sprt_fgkey, 
                                                            id_colab_fgkey
                                                        ) VALUES (
                                                            {id_sprint}, 
                                                            (SELECT id_user FROM projeu_users WHERE Matricula = {matricula_especil}));'''
                                                                    
                                            else: #ESTÁ VINCULADO A SPRINT DO PROJETO
                                                if espec_bd in [str(x).strip() for x in especialist_sprint] and especialistBD_sprint[0][6] == 'I': #FOI SELECIONADO
                                                    cmd_aux = f'''
                                                                UPDATE 
                                                                    projeu_especialist_sprint SET status_sp = "A" 
                                                                WHERE 
                                                                    id_colab_fgkey = (SELECT id_user FROM projeu_users WHERE Matricula = {matricula_especil}) 
                                                                        AND id_sprt_fgkey = {id_sprint};'''
                                                
                                                elif espec_bd not in [str(x).strip() for x in especialist_sprint] and especialistBD_sprint[0][6] == 'A': #FOI RETIRADO
                                                    cmd_aux = f'''
                                                                UPDATE 
                                                                    projeu_especialist_sprint SET status_sp = "I" 
                                                                WHERE 
                                                                    id_colab_fgkey = (SELECT id_user FROM projeu_users WHERE Matricula = {matricula_especil}) 
                                                                        AND id_sprt_fgkey = {id_sprint};'''
                                            #cmd_aux=''
                                            return cmd_aux
                                    
                                    st.text(' ')
                                    spEntregas = [x for x in spEntregas if x[1] != None and x[2] != None and x[3] != None]
                                    
                                    tab1, tab2 = st.tabs(['Atualizar Entregas', 'Excluir Entregas'])
                                    with tab1:
                                        #FORMULÁRIO APRESENTANDO AS ENTREGAS
                                        col1, col2, col3 = st.columns([3,1,1])
                                        qnt_att = st.number_input('Adcionar Atividade', min_value=0, step=1, key=f'add{id_sprint} - {idx_parm}')
                                        
                                        spEntregas.extend([[id_sprint, None, None, 0 , '---', '🟨 Backlog', None] for x in range(qnt_att)])

                                        if len(spEntregas) > 0:
                                            with st.form(f'Formulário Entregas {idx_parm} - {id_sprint}'):
                                                st.text(' ')
                                                
                                                for ativIDX in range(len(spEntregas)): 
                                                    col1, col2, col4 = st.columns([0.6, 0.3, 0.12])
                                                    with col1:
                                                        st.caption(f'Entrega {ativIDX+1}')
                                                    with col2:
                                                        st.caption('Status | Executor')
                                                    with col4:
                                                        st.caption('Hr | Compl')
                                                    with col1:
                                                        name_entreg = st.text_area('Atividade', spEntregas[ativIDX][1] if spEntregas[ativIDX][1] != None else '', key=f'atividade{id_sprint} - {ativIDX} - {idx_parm}', disabled=False, label_visibility="collapsed")
                                                    with col4:
                                                        horas_entreg = st.number_input('Horas', value=spEntregas[ativIDX][3],min_value=0, step=1, key=f'horas{id_sprint} - {ativIDX} - {idx_parm}',disabled=block_sprint, label_visibility="collapsed")

                                                        opc_compl = ['Fácil', 'Médio', 'Difícil']

                                                        compl_entreg = st.selectbox('Compl.', opc_compl, opc_compl.index(spEntregas[ativIDX][4]) if spEntregas[ativIDX][4] != None and spEntregas[ativIDX][4] != '---' else 0, key=f'complex{id_sprint}  - {idx_parm}- {ativIDX}', disabled=block_sprint, label_visibility="collapsed")

                                                    with col2:
                                                        opc_stt = ['🟨 Backlog', '🟥 Impeditivo', '🟦 Executando',  '🟩 Concluído']
                                                        status_entreg = st.selectbox('Status', opc_stt, opc_stt.index(str(spEntregas[ativIDX][5]).strip()) if spEntregas[ativIDX][5] != None and spEntregas[ativIDX][5] != '' else 0, key=f'status{id_sprint}  - {idx_parm} - {ativIDX}', disabled=block_sprint, label_visibility="collapsed")
                                                        
                                                        opc_colb = func_split(dadosOrigin[0][21])
                                                        colab_entreg = st.selectbox('Colaborador', opc_colb, opc_colb.index(str(spEntregas[ativIDX][2]).strip()) if spEntregas[ativIDX][2] != None else None, key=f'colab{id_sprint} - {ativIDX} - {idx_parm}',disabled=block_sprint, label_visibility="collapsed")
                                            

                                                    listDadosAux.append([name_entreg, colab_entreg, horas_entreg, status_entreg, compl_entreg, spEntregas[ativIDX][6]]) 
                                                
                                                listDadosAux = [x for x in listDadosAux if x[0] != '' and x[0] != None]

                                                entrgasBD_by_sprint = [x for x in EntregasBD if str(x[8]).strip() == str(id_sprint).strip()]

                                                limp_entrg = lambda entr: str(entr).strip().replace('"', "'")
                                                if len(entrgasBD_by_sprint) > 0:
                                                    col1, col2, col3 = st.columns([1,3,7])
                                                    with col1:
                                                        button_atual = st.form_submit_button('Atualizar', disabled=block_sprint)        
                                                    
                                                    if str(matriUser).strip() == str(dadosOrigin[0][3]).strip():
                                                        with col2:
                                                            button_final = st.form_submit_button('Finalizar Sprint', disabled=block_sprint) 
                                                    
                                                            if button_final: 
                                                                mycursor = conexao.cursor()
                                                                columns_final = ['check_sprint', 'data_check']
                                                                values_final = [0, f'"{datetime.today()}"']

                                                                cmd_final = f'''UPDATE projeu_sprints SET {columns_final[0]} = {values_final[0]}, {columns_final[1]} = {values_final[1]} WHERE id_sprint = {int(id_sprint)};'''
                                                                mycursor.execute(cmd_final)
                                                                conexao.commit()

                                                                mycursor.close()
                                                                st.toast('Sprint Finalizada!', icon='✅')
                                                                sleep(0.1)
                                                                st.rerun()

                                                    if button_atual:
                                                        mycursor = conexao.cursor()

                                                        if len([x for x in listDadosAux if x[1] == None]) < 1:
                                                            for list_atual in listDadosAux:
                                                                if list_atual[5] != None: #SE A ENTREGA DA "list_atual" JÁ ESTIVER DENTRO DO BANCO DE DADOS SOMENTE VAI ATUALIZAR AS INFORMAÇÕES SOBRE A ENTREGA
                                                                    columnsUP = ['nome_Entrega', 'executor', 'hra_necess', 'stt_entrega', 'compl_entrega']

                                                                    for idxColum in range(len(columnsUP)):
                                                                        cmd_update = f'''UPDATE projeu_entregas SET {columnsUP[idxColum]} = {f'"{list_atual[idxColum]}"' if idxColum != 1 else f'(SELECT id_user FROM projeu_users WHERE Nome = "{list_atual[idxColum]}" LIMIT 1)'} WHERE id_entr = {list_atual[5]};'''
                                                                        mycursor.execute(cmd_update)
                                                                        conexao.commit()


                                                                else: #INSERT DA ENTREGA CASO ELA NÃO ESTEJA PRESENTE DENTRO DO BANCO DE DADOS
                                                                    if list_atual[0] != None and list_atual[0] != '': 
                                                                        tables = ['projeu_entregas', 'projeu_entregas_planejamento']

                                                                        for table_name in tables:
                                                                            cmd_insert = f'''
                                                                                INSERT INTO {table_name} (id_sprint, nome_Entrega, executor, hra_necess, stt_entrega, compl_entrega) 
                                                                                    values({id_sprint},
                                                                                            "{limp_entrg(list_atual[0])}", 
                                                                                            (SELECT id_user FROM projeu_users WHERE Nome = '{list_atual[1]}' LIMIT 1),
                                                                                            {list_atual[2]},
                                                                                            "{list_atual[3]}",
                                                                                            "{list_atual[4]}");'''
                                                                            
                                                                            mycursor.execute(cmd_insert)
                                                                            conexao.commit()

                                                                cmd_especialist = tratamento_especialist()
                                                                mycursor.execute(cmd_especialist)
                                                                conexao.commit()

                                                            mycursor.close()
                                                            st.toast('Dados Atualizados!', icon='✅')

                                                            sleep(0.1)
                                                            st.rerun()
                                                        else:
                                                            st.toast('Entregas com executor vazio no planejamento da sua sprint.', icon='❌')
                                                        
                                                        
                                                else:
                                                    button_inic_entreg = st.form_submit_button('Enviar')
                                                    if button_inic_entreg:

                                                        if len([x for x in listDadosAux if x[1] == None]) < 1:
                                                            mycursor = conexao.cursor()
                                                            tables = ['projeu_entregas', 'projeu_entregas_planejamento']

                                                            for table_name in tables:
                                                                for list_atual in listDadosAux:
                                                                    cmd_insert = f'''
                                                                        INSERT INTO {table_name} (id_sprint, nome_Entrega, executor, hra_necess, stt_entrega, compl_entrega) 
                                                                            values({id_sprint},
                                                                                    "{limp_entrg(list_atual[0])}", 
                                                                                    (SELECT id_user FROM projeu_users WHERE Nome LIKE "%{list_atual[1]}%" LIMIT 1),
                                                                                    {list_atual[2]},
                                                                                    "{list_atual[3]}",
                                                                                    "{list_atual[4]}");'''

                                                                    mycursor.execute(cmd_insert)
                                                                    conexao.commit()

                                                            for i in range(len(especialist_sprint)):
                                                                cmd_insert_espc = f"""INSERT INTO projeu_especialist_sprint (
                                                                                        id_sprt_fgkey, 
                                                                                        id_colab_fgkey
                                                                                    ) VALUES (
                                                                                        {id_sprint}, 
                                                                                        (SELECT id_user FROM projeu_users WHERE Nome LIKE '%{str(especialist_sprint[i]).strip()}%'));"""
                                                                
                                                                mycursor.execute(cmd_insert_espc)
                                                                conexao.commit()

                                                            st.toast('Entregas Enviadas!', icon='✅')
                                                            mycursor.close()
                                                        else:
                                                            st.toast('Entregas com executor vazio no planejamento da sua sprint.', icon='❌')
                                                    
                                                        sleep(0.1)
                                                        st.rerun()
                                    with tab2:
                                        if len(spEntregas) > 0:
                                            font_TITLE('EXCLUIR', fonte_Projeto,"'Bebas Neue', sans-serif", 23, 'left')  

                                            atvdd_exc = st.selectbox('Atividade', [x[1] for x in spEntregas if x[1] != None and x[1] != ' '], key=f'NameExAtivid {id_sprint} - {idx_parm}')

                                            col_sel0, col_sel1, col_sel2, col_sel3 = st.columns([3,1,1,1])
                                            with col_sel0:
                                                exec_exc = st.text_input('Executor', value=f'{[x[2] for x in spEntregas if x[1] == atvdd_exc][0]}', disabled=True, key=f'ExcutExAtivid {id_sprint} - {idx_parm}')
                                            with col_sel1:
                                                compl_exc = st.text_input('Complexidade', value=[x[4] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'ComplexidadeExAtivid {id_sprint} - {idx_parm}')
                                            with col_sel2:
                                                hrs_exc = st.text_input('Horas', value=[x[3] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'HorsExAtivid {id_sprint} - {idx_parm}')
                                            with col_sel3:
                                                stt_exc = st.text_input('Status', value=[x[5] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'StatusExAtivid {id_sprint} - {idx_parm}')
                                            buttonEX = st.button('Excluir', key=f'Excluir{id_sprint} - {idx_parm}')

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
                                                sleep(0.1)
                                                st.rerun()

                                        else:
                                            font_TITLE('AINDA NÃO HÁ ENTREGAS PARA SEREM EXCLUÍDAS!', fonte_Projeto,"'Bebas Neue', sans-serif", 23, 'left')  
                                            st.text(' ')

                    if str(matriUser).strip() == str(dadosOrigin[0][3]).strip():
                        if str(dadosOrigin[0][24]).strip() in ['Em Andamento'] and 'ENTREGA FINAL' in [str(x).strip().upper() for x in func_split(dadosOrigin[0][12])]:
                            button_final_proj = st.button('Finalizar Projeto', key='FINAL DO PROJETO')    
                        
                            if button_final_proj:
                                mycursor = conexao.cursor()

                                cmd_final_proj1 = f'UPDATE projeu_projetos SET check_proj = 1 WHERE id_proj = {dadosOrigin[0][0]};'           
                                mycursor.execute(cmd_final_proj1)
                                conexao.commit()

                                cmd_final_proj2 = f'UPDATE projeu_projetos SET status_proj = "Concluído" WHERE id_proj = {dadosOrigin[0][0]};'           
                                mycursor.execute(cmd_final_proj2)
                                conexao.commit()

                                st.toast('Projeto Finalizado!', icon='✅')
                                sleep(0.1)
                                mycursor.close()
                                st.rerun()
                        #else:
                        #    st.toast('Primeiramente, adcionar evento ENTREGA FINAL ao projeto.', icon='❌')
                                

        else:               
            st.text(' ')
            st.text(' ')
            font_TITLE(f'AINDA NÃO HÁ PROJETOS VINCULADOS A VOCÊ!! ⏳', fonte_Projeto,"'Bebas Neue', sans-serif", 22, 'center')
    
    with tabs2:
        font_TITLE('CADASTRO DE PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
    complix = ['SEGURO', 'ACESSÍVEL', 'ABSTRATO I', 'ABSTRATO II', 'ABSTRATO III', 'SINGULAR I', 'SINGULAR II',
            'SINGULAR III']

    nomeProjeto = st.text_input('Nome do Projeto')
    col1, col2 = st.columns(2)
    with col1:
        colaux1, colaux2 = st.columns([1.3, 2])    
        with colaux1:
            typ_proj = st.selectbox('Tipo Projeto', ['Estratégico', 'OKR', 'Implantação', 'Rápido'])
        with colaux2:
            MacroProjeto = st.selectbox('Macroprocesso', list(set([x[1] for x in prog_macro])))    

        colG1, colG2 = st.columns([1,3]) 
        with colG2:
            gestorProjeto = st.selectbox('Gestor do Projeto', list(set([x[1] for x in users])), 0)
        with colG1:
            matric_gestor = st.text_input('Matricula Gestor', [x[0] for x in users if x[1] == gestorProjeto][0], disabled=True)
        
        if typ_proj not in ("Rápido", "Implantação"):
            mvp_name = st.text_input('MVP')

        pdt_entrFinal = st.text_area('Produto Projeto', key='ProdutoEntrega')

    with col2:
        nomePrograma = st.selectbox('Programa', [x[0] for x in prog_macro if x[1] == MacroProjeto])

        colD1, colD2 = st.columns([2,1]) 
        with colD1:
            dat_inic = st.date_input('Início Projeto')
        with colD2:
            ivsProget = st.text_input('Investimento', placeholder='R$ 0,00')

        if typ_proj not in ("Rápido", "Implantação"):
            mvp_produt = st.text_input('Produto MVP')    

        result_esperd = st.text_area('Resultado Esperado')

    if typ_proj in ('Implantação'):
        #PARÂMETROS ESPECÍFICOS DOS PROJETOS DE IMPLANTAÇÃO
        font_TITLE('PARÂMETROS DE IMPLANTAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
        
        impl_stake = st.text_input('Stakeholders')
        impl_premi = st.text_input('Premissas')
        impl_risco = st.text_input('Riscos')
        impl_justific = st.text_area('Justificativa')
        col1, col2, col3 = st.columns(3)
        with col1:
            impl_obj = st.text_area('Objetivo Smart')
        with col2:
            impl_requis = st.text_area('Requisitos do Projeto')
        with col3:
            impl_restric = st.text_area('Restrições')
        

        ##### ADCIONANDO MARCOS NA LINHA DO TEMPO #####
        st.write('---')
        col1, col2 = st.columns([3,1])
        with col1:
            font_TITLE('LINHA DO TEMPO', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
        with col2:
            qntd_entr = st.number_input('Quantidade', min_value=1, step=1, key='Cadastrar linha do tempo')

        listMarcosTime = []
        st.caption('Principais etapas e marcos do projeto')
        for a_entr in range(qntd_entr):
            listMarcosTime.append(st.text_input('', label_visibility="collapsed", key=f'Cadastrar linha do tempo{a_entr}'))

    else:
        ##### ADCIONANDO MÉTRICAS #####
        st.write('---')
        col1, col2 = st.columns([3,1])
        with col1:
            font_TITLE('MÉTRICAS', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
        with col2:
            qntd_metric = st.number_input('Quantidade', min_value=1, step=1, key=f'Cadastrar Metricas')

        listMetric = []
        st.caption('Métricas')
        for a_metrc in range(qntd_metric):
            listMetric.append(st.text_input('', label_visibility="collapsed", key=f'Cadastrar Metricas{a_metrc}'))
            

    ##### ADCIONANDO AS PRÍNCIPAIS ENTREGAS #####
    st.write('---')
    col1, col2 = st.columns([3,1])
    with col1:
        font_TITLE('PRINCIPAIS ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
    with col2:
        qntd_entr = st.number_input('Quantidade', min_value=1, step=1, key='Cadastrar Entregas')

    listEntregas = []
    st.caption('Entregas')
    for a_entr in range(qntd_entr):
        listEntregas.append(st.text_input('', label_visibility="collapsed", key=f'Cadastrar Entreg{a_entr}'))

        
    ##### ADCIONANDO A EQUIPE #####
    st.write('---')
    col1, col2 = st.columns([3,1])
    with col1:
        font_TITLE('CADASTRO EQUIPE', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
    with col2:
        qntd_clb = st.number_input('Quantidade', min_value=1, step=1)

    col_equip1, col_equip2, col_equip3 = st.columns([0.3, 2, 1])
    with col_equip1:
        st.caption('Matricula')
    with col_equip2:
        st.caption('Colaboradores')
    with col_equip3:
        st.caption('Função')

    #A IDEIA É QUE OS USUÁRIOS SELECIONADOS DURANTE O PREENCHIMENTO DO FORMULÁRIO SEJAM PEGOS AS INFORMAÇÕES DO BANCO DE DADOS DE USUÁRIO
    list_colbs = [[matric_gestor, 'Gestor']]
    for colb_a in range(qntd_clb):
        with col_equip2:
            colb_name = st.selectbox('Colaboradores', [x[1] for x in users], label_visibility="collapsed", key=f'Cadastrar Nome Colab{colb_a}')        
        with col_equip1:
            colab_matric = st.text_input('Matricula', list(set([x[0] for x in users if x[1] == colb_name]))[0], label_visibility="collapsed", disabled=True, key=f'Cadastrar MatriculaColabs{colb_a}')
        with col_equip3:
            colb_funç = st.selectbox('Função', ['Especialista', 'Executor'],None, label_visibility="collapsed", key=f'Cadastrar funcaoColab{colb_a}')
        list_colbs.append([colab_matric, colb_funç])

    st.text(' ')
    st.text(' ')
    colb1,colb2,colb3 = st.columns([3,3,1])
    with colb3:
        st.text(' ')
        btt_criar_prj = st.button('Criar Projeto')

    if btt_criar_prj:
        if len([x for x in list_colbs if x[1] == None]) < 1:
            
            if str(nomeProjeto).strip() not in [str(x).strip() for x in dd_proj]:
                if typ_proj == "Estratégico":
                    parametros = [len(str(x).strip()) if type(x) in (date, str) else len(x) for x in [typ_proj, MacroProjeto, gestorProjeto, mvp_name, pdt_entrFinal, nomePrograma, dat_inic, mvp_produt, result_esperd, listEntregas, list_colbs]]
                elif typ_proj == 'Rápido':
                    parametros = [len(str(x).strip()) if type(x) in (date, str) else len(x) for x in [typ_proj, MacroProjeto, gestorProjeto, pdt_entrFinal, nomePrograma, dat_inic, result_esperd, listEntregas, list_colbs]]
                elif typ_proj == 'Implantação':
                    parametros = [len(str(x).strip()) if type(x) in (date, str) else len(x) for x in [typ_proj, MacroProjeto, gestorProjeto, pdt_entrFinal, nomePrograma, dat_inic, listEntregas, list_colbs, impl_stake, impl_premi, impl_risco, impl_obj, impl_requis, impl_restric, impl_justific]]

                if 0 not in parametros:

                    mycursor = conexao.cursor()
                    try:
                        ############# INSERINDO O PROJETO #############
                        if typ_proj == "Estratégico":
                            cmd_criar_project = f"""INSERT INTO projeu_projetos(
                                type_proj_fgkey, macroproc_fgkey, progrm_fgkey, name_proj, 
                                result_esperad, gestor_id_fgkey, nome_mvp,
                                produto_mvp, produto_entrega_final,  
                                ano, date_posse_gestor,  status_proj, investim_proj
                                ) VALUES (
                                (SELECT id_type FROM projeu_type_proj WHERE type_proj LIKE '%{str(typ_proj).strip()}%'), (SELECT id FROM projeu_macropr WHERE macroprocesso LIKE '%{str(MacroProjeto).strip()}%'), 
                                (SELECT id_prog FROM projeu_programas WHERE nome_prog LIKE '%{nomePrograma}%'), 
                                '{str(nomeProjeto).strip()}', '{str(result_esperd).strip()}', 
                                (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{str(mvp_name).strip()}', '{str(mvp_produt).strip()}', 
                                '{str(pdt_entrFinal).strip()}', {int(dat_inic.year)}, '{dat_inic}', 'Aguardando Início' , '{str(ivsProget).strip()}');"""
                        elif typ_proj == 'Rápido':
                            cmd_criar_project = f"""INSERT INTO projeu_projetos(
                                type_proj_fgkey, macroproc_fgkey, progrm_fgkey, name_proj, 
                                result_esperad, gestor_id_fgkey, produto_entrega_final,  
                                ano, date_posse_gestor,  status_proj, investim_proj
                                ) VALUES (
                                (SELECT id_type FROM projeu_type_proj WHERE type_proj LIKE '%{str(typ_proj).strip()}%'), (SELECT id FROM projeu_macropr WHERE macroprocesso LIKE '%{str(MacroProjeto).strip()}%'), 
                                (SELECT id_prog FROM projeu_programas WHERE nome_prog LIKE '%{nomePrograma}%'), 
                                '{str(nomeProjeto).strip()}', '{str(result_esperd).strip()}', 
                                (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{str(pdt_entrFinal).strip()}', {int(dat_inic.year)}, '{dat_inic}', 'Aguardando Início' , '{str(ivsProget).strip()}');"""
                        elif typ_proj == 'Implantação':
                            cmd_criar_project = f"""
                                INSERT INTO 
                                    projeu_projetos( 
                                        type_proj_fgkey, 
                                        macroproc_fgkey, 
                                        progrm_fgkey, 
                                        name_proj, 
                                        result_esperad, 
                                        gestor_id_fgkey, 
                                        produto_entrega_final,
                                        ano, 
                                        date_posse_gestor, 
                                        status_proj, 
                                        investim_proj,
                                        justific_impl_proj,
                                        stakeholders_impl_proj,
                                        premissas_impl_proj,
                                        riscos_impl_proj,
                                        restric_impl_proj,
                                        objSmart_impl_proj,
                                        requisitos_impl_proj 
                                ) VALUES (
                                (SELECT id_type FROM projeu_type_proj WHERE type_proj LIKE '%{str(typ_proj).strip()}%'), (SELECT id FROM projeu_macropr WHERE macroprocesso LIKE '%{str(MacroProjeto).strip()}%'), 
                                (SELECT id_prog FROM projeu_programas WHERE nome_prog LIKE '%{nomePrograma}%'), 
                                '{str(nomeProjeto).strip()}', '{str(result_esperd).strip()}', 
                                (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{str(pdt_entrFinal).strip()}', {int(dat_inic.year)}, '{dat_inic}', 'Aguardando Início' , '{str(ivsProget).strip()}', '{impl_justific}', '{impl_stake}', '{impl_premi}', '{impl_risco}', '{impl_restric}', '{impl_obj}', '{impl_requis}');"""

                        st.error(cmd_criar_project)
                        mycursor.execute(cmd_criar_project)
                        conexao.commit()
                        print('PROJETO CRIADO!')
                        print('---'*30)
                        print('VINCULANDO COLABORADORES AO PROJETO')
                        sleep(0.2)

                        if typ_proj not in ('Implantação'):
                            ############# INSERINDO MÉTRICAS DO PROJETO #############
                            dd_metric = ''
                            for metric_name in listMetric:
                                dd_metric += f"((SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1), '{metric_name}'),"
                            dd_metric = dd_metric[:len(dd_metric)-1]

                            cmd_metric = f"""INSERT INTO projeu_metricas(id_prj_fgkey, name_metric) 
                                                VALUES {dd_metric};"""
                            
                            st.info(cmd_metric)
                            mycursor.execute(cmd_metric)
                            conexao.commit()
                            sleep(0.2)

                        #else:
                        #    ############# INSERINDO MARCOS DO PROJETO #############
                        #    values_line = ''
                        #    for marco_time in listMarcosTime:
                        #        
                        #        if len(str(marco_time).strip()) > 0: 
                        #            cmd_line_tempo = f"""('{marco_time}', (SELECT * FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%')),"""
                        #            values_line += cmd_line_tempo
                        #    
                        #    values_line = values_line[:-1]
                        #
                        #    if len(str(values_line).strip()) > 0:
                        #        cmd_insert_marcos = f"""
                        #        INSERT INTO projeu_impl_linhaTempo (marco_line_tempo, id_proj_fgkey)
                        #            VALUES {values_line};"""
                        #


                        ############# INSERINDO COMPLEXIDADE #############
                        if typ_proj != "Rápido":
                            cmd_insert_complx = f'''INSERT INTO projeu_complexidade (proj_fgkey, date_edic) 
                            VALUES (
                            (SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1),
                            '{date.today()}'
                            );'''
                        else:
                            cmd_insert_complx = f'''INSERT INTO projeu_complexidade (proj_fgkey, date_edic, complxdd, check_lider, check_govern, check_avaliado) 
                            VALUES (
                            (SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1),
                            '{date.today()}', 'Rápido', 1, 1, 1
                            );'''

                        st.success(cmd_insert_complx)
                        mycursor.execute(cmd_insert_complx)
                        conexao.commit()
                        print('LINHA DE COMPLEXIDADE VINCULADO AO BANCO DE DADOS!')
                        sleep(0.2)

                        
                        ############# INSERINDO EQUIPE #############
                        values_ie = [f"""((SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1), (SELECT id_user FROM projeu_users WHERE Matricula = {list_colb[0]} limit 1), '{list_colb[1]}')""" for list_colb in list_colbs]
                        comand_insert_colabs = f"""INSERT INTO projeu_registroequipe(id_projeto, id_colab, papel) VALUES {str(values_ie).replace('[', '').replace(']', '').replace('"', '')} ;"""
                        
                        st.info(comand_insert_colabs)
                        mycursor.execute(comand_insert_colabs)
                        conexao.commit()

                        print('COLABORADORES VINCULADOS')
                        sleep(0.2)
                        
                        ############# INSERINDO PRINCIPAIS ENTREGAS #############
                        if len(listEntregas) > 0:
                            values_pe = list([f"""('{name_entr}',(SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1))""" 
                                            for name_entr in listEntregas])
                            
                            cmd_insert_princp = f'''INSERT INTO projeu_princEntregas (
                            entreg, 
                            id_proj_fgkey
                            )
                            values {str(values_pe).replace('[', '').replace(']', '').replace('"', '')};'''
                            
                            st.error(cmd_insert_princp)
                            mycursor.execute(cmd_insert_princp)
                            conexao.commit()

                        st.toast('Sucesso na criação do Projeto!', icon='✅')
                        
                    except:
                        st.toast('Erro ao cadastrar projeto na base de dados.', icon='❌')
                    mycursor.close()
                else:
                    st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')
            else:
                st.toast('Já existe um projeto com esse nome.', icon='❌')
        else:
            st.toast('Por gentileza, ajustar corretamente todas as funções da equipe selecionada.', icon='❌')
