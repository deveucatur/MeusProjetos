import streamlit as st

fonte = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Passion+One&display=swap" rel="stylesheet">'''

fonte2 = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Koulen&family=Passion+One&display=swap" rel="stylesheet">'''

fonte3 = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bungee+Inline&family=Koulen&family=Passion+One&display=swap" rel="stylesheet">'''

fonte4 = '''@import url('https://fonts.googleapis.com/css2?family=Bungee+Inline&family=Koulen&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''

def font_TITLE(texto, fonte, fonte1, tam_font, text_alinham = None, cor = 'gray11'):
#FONTE = URL DA FONTE
#FONTE1 = NOME DA FONTE DA QUE ESTÁ SENDO IMPORTADA
    css1 = f"""
        <style>
            {fonte} 
            .gold-text{tam_font} {{
                font-size: {tam_font}px;
                color: {cor};
                text-align: {text_alinham};
                margin-bottom: 0px;
            }}
            .custom-font{tam_font} {{
                font-family: {fonte1} 
            }}
        </style>"""

    st.markdown(css1, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text{tam_font} custom-font{tam_font}">{texto}</p>', unsafe_allow_html=True)


def card_traspent():
    html ="""<div class="cardContainer">
    <div class="card">
    <p class="city">PINK CITY</p>
    <p class="weather">PARTILY CLOUDY</p>
    <svg xml:space="preserve" viewBox="0 0 100 100" height="50px" width="50px" y="0px" x="0px" id="Layer_1" version="1.1" class="weather">  <image href="data:image/png;base64,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" y="0" x="0" height="100" width="100" id="image0"></image>
        </svg>
        <p class="temp">32°</p>
        <div class="minmaxContainer">
        <div class="min">
            <p class="minHeading">Min</p>
            <p class="minTemp">30°</p>
        </div>
        <div class="max"><p class="maxHeading">Max</p>
            <p class="maxTemp">32°</p></div>
        </div>
        
    </div>
    </div>""" 

    css=""".cardContainer {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    }

    .card {
    position: relative;
    width: 220px;
    height: 170px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 20px 10px;
    border-radius: 10px;
    backdrop-filter: blur(30px);
    background-color: rgba(65, 65, 65, 0.308);
    border: 1px solid rgba(255, 255, 255, 0.089);
    cursor: pointer;
    }

    .city {
    font-weight: 700;
    font-size: 0.9em;
    letter-spacing: 1.2px;
    color: white;
    }

    .weather {
    font-weight: 500;
    font-size: 0.7em;
    letter-spacing: 1.2px;
    color: rgb(197, 197, 197);
    }

    .temp {
    font-size: 1.8em;
    color: white;
    }

    .minmaxContainer {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    }

    .min,.max {
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    padding: 0px 20px;
    gap: 4px;
    }

    .max {
    align-items: flex-start;
    border-left: 2px solid white;
    }

    .maxHeading,.minHeading {
    font-size: 0.7em;
    font-weight: 600;
    color: white;
    }

    .maxTemp,.minTemp {
    font-size: 0.6em;
    font-weight: 500;
    color: rgb(197, 197, 197);
    }

    """

    st.write(f"<style>{css}<style>", unsafe_allow_html=True)
    st.write(f"{html}", unsafe_allow_html=True)

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

def displayInd(title, valor, min_val, max_val):
    max_val = float(max_val)
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card2 {
        padding: 0.6rem;
        background-color: #fff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%;
        border-radius: 20px;
        text-align: center;
    }

    .title2 {
        align-items: center;
    }

    .title2-text {
    color: #374151;
    font-size: 18px;
    font-family: 'Poppins', sans-serif;
    }

    .data2 {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .data2 p {
        color: #1F2937;
        font-size: 2.25rem;
        line-height: 2.5rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }

    '''

    # HTML da janela
    htmlJanela = f'''
                    <div class="card2">
                        <div class="title2">
                            <p class="title2-text">{title}</p>
                                </div>
                                <div class="data2">
                            <p>{int(valor)}</p>
                        </div>
                    </div>
                '''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'<div>{htmlJanela}</div>', unsafe_allow_html=True)


def cardProject(listProject):
    var_css = """ 
    <style>
    .card {
        background-color: #ffffff;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1), 0px 8px 16px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 20px;
        font-family: 'Poppins', sans-serif;
    }

    .card-content {
        margin-bottom: 10px;
        color: #374151;
        font-size: 18px;
    }
    </style>"""

    var_html = '<div class="card">'
    for a in listProject:
        var_html += f'''<div class="card-content">
                        <p>{a}</p>
                    </div>'''
    var_html += '</div>'

    st.write(var_css, unsafe_allow_html=True)
    st.write(f'<body>{var_html}</body>', unsafe_allow_html=True)


def cardGRANDE(title, valor):
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .container {
        display: flex;
        justify-content: space-between;
    }

    .cardG {
        padding: 2.3rem;
        background-color: transparent;
        flex: 1;
        border-radius: 20px;
        box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-bottom: 2px solid #000;
    }

    .Allcolumms {
        display: flex; 
        justify-content: space-between;
        flex-wrap: wrap;
    }
    
    .titleG {
        align-items: center;
    }

    .titleG-text {
        color: #374151;
        font-size: 12px;
        font-family: 'Poppins', sans-serif;
    }

    .dataG {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .dataG p {
        color: #1F2937;
        font-size: 50px;
        line-height: 2.5rem;
        font-weight: 450;
        font-family: 'Poppins', sans-serif;
    }
    '''


    # HTML da janela
    htmlJanelaText = f'''
    <div class="cardG">
        <div class="Allcolumms">'''
            
    for a in range(len(title)):
        htmlJanelaText += f'''<div style="flex-basis: 105px;">
                                    <div class="titleG">
                                        <p class="titleG-text">{title[a]}</p>
                                    </div>
                                    <div class="dataG">
                                        <p>{valor[a]}</p>
                                    </div>
                                </div>'''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'{htmlJanelaText}</div></div>', unsafe_allow_html=True)


def cardMyProject(nome_user, dados_user):
    param = ['Atividades', 'Entregues', 'Horas Total', 'Complexidade']
    css = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    
    .card {
        color: #1F2937;
        font-family: Poppins, sans-serif;
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        width: 100%;
        margin: 20px auto;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%; 
    }

    .linha1 {
        font-size: 27px;
        font-weight: 450; 
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
        flex-wrap: wrap;
    }

    .coluna {
        flex: 1;
        background-color:#ffffff;
        padding: 0%;
        flex-basis: 130px;
    }
    .coluna p{
        font-size: 2.5rem;
        line-height: 2.5rem;
        font-weight: 450;
    }    
    '''

    html = f'''
    <body>
        <div class="card">
            <div class="linha1">
                <p style="font-size: 12px; opacity: 60%;">Name</p>
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