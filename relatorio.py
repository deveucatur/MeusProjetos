from PIL import Image

def complexidade_name(number):
    aux = {1: 'Fácil',
           2: 'Médio',
           3: 'Difícil',
           None: 'Gestor/Especialista'}
    
    return aux[number]

def funcao_premio(sigla):
    if sigla in ['G', 'E', 'EX']:
        aux = {'G': 'Gestor',
            'E': 'Especialista',
            'EX': 'Executor'}
        return aux[sigla]
    else:
        return None

def dadosRelatorio(entregas_list):
    htmlDados = ""

    # 1-SPRINT 2-FUNCAO 3-ENTREGA 4-HORAS 5-COMPLEXIDADE 6-VALOR
    for entreg in entregas_list:
        htmlDados += f"""<tr>
                <td>{entreg[1]}</td> 
                <td>{funcao_premio(entreg[6])}</td>
                <td>{entreg[3] if entreg[3] != None else ' '}</td>
                <td>{entreg[7] if entreg[7] != None else 0}</td>
                <td>{complexidade_name(entreg[9])}</td>
                <td>R${entreg[10]}</td>
            </tr>"""
        
    return htmlDados

def tabelaRelatorio(dadosAux = dict):
    
    htmlTabela = ""
    for nameProj, ddconsolid in dadosAux.items():
        dadosTABLE = dadosRelatorio(ddconsolid)
    
        htmlTabela += f"""<h3 class="projeto">{nameProj}</h3>
            <table>
                <tr>
                    <th>Sprint</th>
                    <th>Função</th>
                    <th>Entrega</th>
                    <th>Horas</th>
                    <th>Dificuldade</th>
                    <th>Valor</th>
                </tr>
                <div>{dadosTABLE}</div>
            </table>"""
    
    return htmlTabela

def escopoGeral(nome_colab, list_valores, txt_temporario, name_arquivo):
    tabela = tabelaRelatorio(list_valores)
    icone = Image.open('imagens/icone.png')
    
    sum_total = 0
    for proj, dd in list_valores.items():
        sum_total += sum([x[10] for x in dd])
        cpf = list(set([x[13] for x in dd]))[0]
        empresa = list(set([x[14] for x in dd]))[0]

    htmlGeral = f"""<head>
            <style>
                body, h1, h3, p, table{{
                    margin: 0;
                    padding: 0;
                }}

                body{{
                    font-family: Arial, sans-serif;
                    margin: 0 20px;
                    padding: 0;
                }}

                .header{{
                    text-align: center;
                }}

                .header img{{
                    min-width: 100px;
                    max-width: 100px;
                    height: auto;
                }}

                .inf{{
                    text-align: center;
                    margin: 0 20px;
                }}

                .inf h1{{
                    font-size: 36px;
                    width: 100%;
                }}

                .inf p{{
                    text-align: left;
                    font-size: 16px;
                    margin: 0 5px;
                }}

                .relatorio{{
                    margin: 0 20px;
                    text-align: center;
                }}

                .projeto{{
                    background-color: #87c772;
                    border-radius: 0 0 10px 10px;
                    width: 100%;
                    margin: auto;
                    margin-bottom: 20px;
                    text-align: center;
                }}

                table{{
                    width: 100%;
                    margin: 0 auto;
                    border-collapse: collapse;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    font-size: smaller;
                }}

                table th, table td{{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #145000;
                    text-align: center;
                }}

                table th{{
                    background-color: #99cb89;
                }}

                .total{{
                    background-color: #87c772;
                    padding: 5px;
                    width: 95%;
                    margin: auto;
                    margin-bottom: 5px;
                    text-align: right;
                    border-radius: 8px;
                }}

                hr{{
                    margin: 5px 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <img src="https://www.fag.edu.br/upload/galeria/551c0ac08125a.jpg" alt="Logo da Eucatur">
            </div>
            <div class="inf">
                <h1>Extrato de Prestação de Serviço</h1>
                <p>Nome: {nome_colab}</p>
                <p>CPF/CNPJ: {cpf}</p>
                <p>Empresa: {empresa}</p>
            </div>
            <hr>
            <div class="relatorio">{tabela}</div>
            <div class="total">
                <h3>Valor total: R${sum_total}</h3>
            </div>
        </body>"""
    
    return htmlGeral
