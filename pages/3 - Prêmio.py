import streamlit as st
from util import font_TITLE
from PIL import Image

icone = Image.open('imagens/icone.png')
st.set_page_config(
    page_title="Meus Prêmio",
    page_icon=icone,
    layout="wide")


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

#DADOS          #TAREFA, PROJETO, HORAS, SPRINT, HORAS, COMPLEXIDADE
tarefas_ex = [
    ['Analisar opções de melhorias', 'Projeto Desenvolvendo Melhorias', 'Sprint 10', 20, 'M', 25.78],
    ['Implementar funcionalidade X', 'Projeto Desenvolvendo Melhorias', 'Sprint 11', 15, 'F', 100.00],
    ['Testar integração com sistema Y', 'Projeto Novas Features', 'Sprint 5', 12, 'M', 78.89],
    ['Revisar código da feature Z', 'Projeto Novas Features', 'Sprint 8', 8, 'D', 65.99],
    ['Desenvolver interface de usuário', 'Projeto Novas Features', 'Sprint 7', 8, 'F', 233.90],
    ['Corrigir bugs prioritários', 'Projeto Desenvolvendo Melhorias', 'Sprint 15', 10, 'D', 99.0]]


fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
font_TITLE('MEUS PRÊMIOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')

with st.expander('Filtro'):
    user_project = st.selectbox('Projeto', ['Todos', 'Projeto1', 'Projeto2', 'Projeto3'])
    mes_project = st.selectbox('Período', ['15/07/2023 - 15/08/2023', '15/06/2023 - 15/07/2023', '15/05/2023 - 15/06/2023'])
        
st.text(' ')
col1, col2 = st.columns([1, 3])

with col1:
    font_TITLE('DESEMPENHO MENSAL', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')

    image_url=  r"https://th.bing.com/th/id/R.5bef3f83aa5b90c7913386dde6143553?rik=vpAUUjGY9Rl50w&riu=http%3a%2f%2finterpacificoltda.hostdataset.com%2fipexports%2fppa%2fimg%2fUsuario.png&ehk=7QiNoqM5sO%2fJhX8rNRTAoWxozQEWhPz8xCZ7L7evY9s%3d&risl=&pid=ImgRaw&r=0"
    cardImg(image_url)
    st.markdown(f'Rodrigo Vasconcelos do Carmo')

with col2:    
    st.text(' ')
    col1, col2, col3, col4, col5 = st.columns([0.6,1,1,1,1])
    with col2:
        font_TITLE('PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
        font_TITLE(f'{len(set([x[1] for x in tarefas_ex]))}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')
    with col3:
        font_TITLE('ATIVIDADES', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
        font_TITLE(f'{len(tarefas_ex)}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')
    with col4:
        font_TITLE('HORAS', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
        font_TITLE(f'{sum([x[3] for x in tarefas_ex])}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')
    with col5:
        font_TITLE('BONIFICAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 32, 'center')
        font_TITLE(f'R${round(sum([x[5] for x in tarefas_ex]), 2)}', fonte_Projeto,"'Bebas Neue', sans-serif", 44, 'center')

st.text(' ')
st.text(' ')
st.text(' ')
st.divider()
font_TITLE('RELATÓRIO TAREFAS MENSAIS', fonte_Projeto,"'Bebas Neue', sans-serif", 45, 'left')
for a in list(set([x[1] for x in tarefas_ex])):
    tarefas_do_project = [x for x in tarefas_ex if x[1] == a] 
    font_TITLE(f'{a}', fonte_Projeto,"'Bebas Neue', sans-serif", 22, 'left')
    
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

    for b in tarefas_do_project:
        with col1:
            st.text_input('Atividade', b[0], key=f'atividade{a} - {b}', label_visibility="collapsed")
        with col2:
            st.text_input('Sprint', b[2], key=f'sprint{a} - {b}', label_visibility="collapsed")
        with col3:
            st.text_input('Horas', f'{b[3]} hrs', key=f'horas{a} - {b}', label_visibility="collapsed")
        with col4:
            st.text_input('Compl.', b[4], key=f'complex{a} - {b}', label_visibility="collapsed")
        with col5:
            st.text_input('Valor', f'R$ {b[5]}', key=f'valor{a} - {b}', label_visibility="collapsed")
