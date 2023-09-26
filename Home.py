import streamlit as st


st.title('Home')

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
            transition: background-color 0.6s ease;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            max-width: 100%;
            border-radius: 20px;
        }}
        .botao-estiloso:hover {{
            background-color: #228B22;
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


st.write("---")
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