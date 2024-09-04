import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# Função para calcular o saldo final com base em juros compostos e inflação
def calcular_saldo_final(idade_atual, idade_aposentadoria, contribuicao_mensal, taxa_retorno, taxa_inflacao):
    anos_contribuicao = idade_aposentadoria - idade_atual
    meses_contribuicao = anos_contribuicao * 12
    saldo = 0
    total_investido = 0
    
    for mes in range(meses_contribuicao):
        saldo += contribuicao_mensal
        saldo *= (1 + (taxa_retorno / 100) / 12)  # Taxa de retorno ajustada para meses
        total_investido += contribuicao_mensal  # Soma das contribuições mensais
        contribuicao_mensal *= (1 + (taxa_inflacao / 100) / 12)  # Ajusta contribuição pela inflação
    
    total_retorno = saldo - total_investido  # Retorno gerado
    return saldo, total_investido, total_retorno

# Simulação de cenários
def simular_cenarios(idade_atual, idade_aposentadoria, contribuicao_mensal, cenarios):
    resultados = {}
    for cenario in cenarios:
        taxa_retorno, taxa_inflacao = cenario
        saldo_final, total_investido, total_retorno = calcular_saldo_final(
            idade_atual, idade_aposentadoria, contribuicao_mensal, taxa_retorno, taxa_inflacao)
        resultados[f"Retorno {taxa_retorno}%, Inflação {taxa_inflacao}%"] = {
            'saldo_final': saldo_final, 
            'total_investido': total_investido,
            'total_retorno': total_retorno
        }
    return resultados

# Gerar gráficos comparativos
def gerar_graficos(resultados, anos_contribuicao):
    labels = list(resultados.keys())
    valores = [res['saldo_final'] for res in resultados.values()]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, valores, color='skyblue')
    plt.xlabel('Saldo Final (R$)')
    plt.title(f'Comparação de Cenários de Aposentadoria (Tempo total investindo: {anos_contribuicao} anos)')
    
    # Adicionar os valores exatos no gráfico de barras
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'R${bar.get_width():,.2f}', va='center')
    
    plt.tight_layout()
    plt.savefig('comparacao_cenarios.png')
    plt.show()

# Gráfico de pizza (Proporção do saldo final)
def gerar_grafico_pizza(total_investido, total_retorno, anos_contribuicao):
    labels = ['Total Investido', 'Total Gerado de Retorno']
    valores = [total_investido, total_retorno]
    cores = ['#ff9999','#66b3ff']

    plt.figure(figsize=(6, 6))
    plt.pie(valores, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)
    plt.title(f'Proporção do Saldo Final: Investido vs Retorno Gerado\nTempo total investindo: {anos_contribuicao} anos')
    plt.tight_layout()
    plt.savefig('grafico_pizza.png')
    plt.show()

# Gerar relatório em PDF
def gerar_relatorio_pdf(resultados, anos_contribuicao):
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Relatório de Simulação de Aposentadoria', ln=True, align='C')

    # Resultados com tempo de contribuição
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f'Tempo total investindo: {anos_contribuicao} anos', ln=True)
    
    for descricao, res in resultados.items():
        saldo_final = res['saldo_final']
        total_investido = res['total_investido']
        total_retorno = res['total_retorno']
        pdf.cell(200, 10, f'{descricao}:', ln=True)
        pdf.cell(200, 10, f'Saldo Final: R${saldo_final:,.2f}', ln=True)
        pdf.cell(200, 10, f'Total Investido: R${total_investido:,.2f}', ln=True)
        pdf.cell(200, 10, f'Retorno Gerado: R${total_retorno:,.2f}', ln=True)
        pdf.ln(5)

    # Adicionando gráfico ao PDF
    pdf.image('comparacao_cenarios.png', x=10, y=60, w=190)
    pdf.add_page()
    pdf.image('grafico_pizza.png', x=10, y=10, w=190)
    
    pdf.output('simulacao_aposentadoria.pdf')

# Entradas do usuário
idade_atual = int(input("Digite sua idade atual: "))
idade_aposentadoria = int(input("Digite a idade que deseja se aposentar: "))
contribuicao_mensal = float(input("Digite a contribuição mensal esperada (R$): "))
taxa_retorno_anual = float(input("Digite a taxa de retorno anual esperada (%): "))

# Definindo cenários alternativos (taxa de retorno, inflação)
cenarios = [
    (taxa_retorno_anual, 2.0),    # Cenário 1: Taxa de retorno do usuário, inflação de 2%
    (taxa_retorno_anual + 1, 3.0),  # Cenário 2: Taxa de retorno +1%, inflação de 3%
    (taxa_retorno_anual - 1, 1.5),  # Cenário 3: Taxa de retorno -1%, inflação de 1.5%
    (taxa_retorno_anual + 2, 2.5)   # Cenário 4: Taxa de retorno +2%, inflação de 2.5%
]

# Simulando cenários
anos_contribuicao = idade_aposentadoria - idade_atual
resultados = simular_cenarios(idade_atual, idade_aposentadoria, contribuicao_mensal, cenarios)

# Exibir resultado do cenário principal
cenario_principal = resultados[f"Retorno {taxa_retorno_anual}%, Inflação 2.0%"]
saldo_final = cenario_principal['saldo_final']
total_investido = cenario_principal['total_investido']
total_retorno = cenario_principal['total_retorno']

print(f"Total investido: R${total_investido:,.2f}")
print(f"Total de retorno gerado: R${total_retorno:,.2f}")
print(f"Saldo final: R${saldo_final:,.2f}")

# Gerar gráficos comparativos
gerar_graficos(resultados, anos_contribuicao)

# Gerar gráfico de pizza para o cenário principal
gerar_grafico_pizza(total_investido, total_retorno, anos_contribuicao)

# Gerar relatório em PDF
gerar_relatorio_pdf(resultados, anos_contribuicao)

print("Relatório gerado com sucesso: simulacao_aposentadoria.pdf")
