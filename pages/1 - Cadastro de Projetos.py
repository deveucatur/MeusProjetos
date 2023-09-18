import streamlit as st
from PIL import Image
from util import font_TITLE
import mysql.connector
from time import sleep

icone = Image.open('imagens/icone.png')
st.set_page_config(
    page_title="Cadastro de Projetos",
    page_icon=icone,
    layout="wide")


########CONECTANDO AO BANCO DE DADOS########
conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)


def formatar_numero_string(numero_str):

    #FUNÇÃO QUE INVERTE STRINGS
    def inverteString(string):
        StringInvert = ''
        for i in range(len(string) - 1, -1, -1):
            StringInvert += string[i]

        return StringInvert

    partes = numero_str.split(",")
    
    #INVERTENDO OS NUMEROS PARA CONTABILIZAR E ADCIONAR PONTOS ENTRE OS DIGITOS
    textInvertAUX = inverteString(partes[0])

    contDigits = 0
    stringAUX = ''
    for a in textInvertAUX:
        contDigits += 1
        stringAUX += a
        if contDigits == 3:
            stringAUX += '.'
            contDigits = 0

    #INVERTENDO NOVAMENTE E TRAZENDO OS DIGITOS PARA FORMATO ORIGINAL, PORÉM, AGORA COM OS PONTOS ENTRE ELES
    stringOFI = inverteString(stringAUX)
    
    if len(partes) > 1:
        return f"{stringOFI},{partes[1]}0"
    else:
        return stringOFI


#CONSUMINDO OS DADOS DO BANCO DE ADOS
mycursor = conexao.cursor()
mycursor.execute("""SELECT 
  p.nome_prog, 
  m.macroprocesso
FROM projeu_programas p
JOIN projeu_macropr m ON p.macroprocesso_fgkey = m.id;"""
)

dados_page = mycursor.fetchall()
dd_prog = list(set([x[0] for x in dados_page]))
dd_macr = list(set([x[1] for x in dados_page]))


mycursor.execute("""SELECT Matricula, 
                 Nome FROM projeu_users;"""
)
users = mycursor.fetchall()
mycursor.close()

#A IDEIA É QUE OS USUÁRIOS SELECIONADOS DURANTE O PREENCHIMENTO DO FORMULÁRIO SEJAM PEGOS AS INFORMAÇÕES DO BANCO DE DADOS DE USUÁRIO
fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
'''

font_TITLE('CADASTRO DE PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
complix = ['SEGURO', 'ACESSÍVEL', 'ABSTRATO I', 'ABSTRATO II', 'ABSTRATO III', 'SINGULAR I', 'SINGULAR II',
        'SINGULAR III']

nomeProjeto = st.text_input('Nome do Projeto')
col1, col2 = st.columns(2)
with col1:
    colaux1, colaux2 = st.columns([1.3, 2])    
    with colaux1:
        typ_proj = st.selectbox('Tipo Projeto', ['Estratégicos', 'OKR', 'Implantação'])
    with colaux2:
        MacroProjeto = st.selectbox('Macroprocesso', dd_macr)    

    colG1, colG2 = st.columns([1,3]) 
    with colG2:
        gestorProjeto = st.selectbox('Gestor do Projeto', list(set([x[1] for x in users])), 0)
    with colG1:
        matric_gestor = st.text_input('Matricula Gestor', [x[0] for x in users if x[1] == gestorProjeto][0], disabled=True)
    
    mvp_name = st.text_input('MVP')
    pdt_entrFinal = st.text_area('Produto Final')

with col2:
    nomePrograma = st.selectbox('Programa', dd_prog)

    colD1, colD2 = st.columns([2,1]) 
    with colD1:
        dat_inic = st.date_input('Início Projeto')
    with colD2:
        ivsProget = st.text_input('Investimento', placeholder='R$ 0,00')
    mvp_produt = st.text_input('Produto MVP')    

    obj_proj = st.text_area('Objetivo Projeto')

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

list_colbs = []
for colb_a in range(qntd_clb):
    with col_equip2:
        colb_name = st.selectbox('Colaboradores', [x[1] for x in users], 0, label_visibility="collapsed", key=f'Nome Colab{colb_a}')        
    with col_equip1:
        colab_matric = st.text_input('Matricula', list(set([x[0] for x in users if x[1] == colb_name]))[0], label_visibility="collapsed", disabled=True, key=f'MatriculaColabs{colb_a}')
    with col_equip3:
        colb_funç = st.selectbox('Função', ['Especialista', 'Executor'], label_visibility="collapsed", key=f'funcaoColab{colb_a}')
    list_colbs.append([colab_matric, colb_funç])

st.text(' ')
st.text(' ')
colb1,colb2,colb3 = st.columns([3,3,1])
with colb3:
    st.text(' ')
    btt_criar_prj = st.button('Criar Projeto')

if btt_criar_prj:
    mycursor = conexao.cursor()
    try:
        mycursor.execute(f"""INSERT INTO projeu_projetos(
            type_proj_fgkey, macroproc_fgkey, progrm_fgkey, name_proj, 
            objtv_projet, gestor_id_fgkey, nome_mvp,
            produto_mvp, produto_entrega_final,  
            ano, date_posse_gestor,  status_proj, investim_proj
            ) VALUES (
            (SELECT id_type FROM projeu_type_proj WHERE type_proj = '{typ_proj}'), (SELECT id FROM projeu_macropr WHERE macroprocesso = '{MacroProjeto}'), 
            (SELECT id_prog FROM projeu_programas WHERE nome_prog = '{nomePrograma}'), 
            '{nomeProjeto}', '{obj_proj}', 
            (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{mvp_name}', '{mvp_produt}', 
            '{pdt_entrFinal}', {int(dat_inic.year)}, '{dat_inic}', 'Backlog' , '{ivsProget}'); """)
        
        print('PROJETO CRIADO!')
        print('---'*30)
        print('VINCULANDO COLABORADORES AO PROJETO')
        sleep(1.5)
        conexao.commit()
        for list_colb in list_colbs:
            comand_insert_colabs = f"""INSERT INTO projeu_registroequipe(id_projeto, id_colab, papel) VALUES 
            ((SELECT id_proj FROM projeu_projetos WHERE name_proj = "{nomeProjeto}" AND gestor_id_fgkey = (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor} limit 1)), (SELECT id_user FROM projeu_users WHERE Matricula = {list_colb[0]} limit 1), '{list_colb[1]}')"""
            
            mycursor.execute(comand_insert_colabs)
            conexao.commit()
        print('COLABORADORES VINCULADOS')    
        st.toast('Sucesso na criação do Projeto!', icon='✅')
    except:
        st.toast('Erro na criação do projeto.', icon='❌')
    

    
