import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

def calcular_saldo_final(contribuicao_mensal, taxa_retorno, taxa_inflacao, anos):
    """
    Calcula o saldo final de um investimento considerando juros compostos e inflação.
    
    Parameters:
    - contribuicao_mensal: Valor investido mensalmente.
    - taxa_retorno: Taxa de retorno anual.
    - taxa_inflacao: Taxa de inflação anual.
    - anos: Duração do investimento em anos.
    
    Returns:
    - saldo: Saldo final do investimento.
    - total_investido: Total investido.
    - total_retorno: Retorno gerado.
    """
    meses = anos * 12  # Convertendo anos em meses
    saldo = 0
    total_investido = 0
    
    # Loop para cada mês do período de investimento
    for mes in range(meses):
        saldo += contribuicao_mensal  # Adiciona o valor investido no saldo
        saldo *= (1 + (taxa_retorno / 100) / 12)  # Aplica juros compostos mensalmente
        total_investido += contribuicao_mensal  # Atualiza o total investido
        contribuicao_mensal *= (1 + (taxa_inflacao / 100) / 12)  # Ajusta a contribuição mensal pela inflação
    
    total_retorno = saldo - total_investido  # Calcula o retorno gerado
    return saldo, total_investido, total_retorno

def simular_cenarios(taxa_retorno, taxa_inflacao):
    """
    Simula diferentes cenários de retorno e inflação para o investimento.
    
    Parameters:
    - taxa_retorno: Taxa de retorno inicial do investimento.
    - taxa_inflacao: Taxa de inflação inicial.
    
    Returns:
    - cenarios: Lista de cenários com diferentes taxas de retorno e inflação.
    """
    cenarios = [
        (taxa_retorno, taxa_inflacao),               # Cenário base
        (taxa_retorno + 1, taxa_inflacao + 1),       # Cenário com aumento na taxa de retorno e inflação
        (taxa_retorno - 1, taxa_inflacao - 1),       # Cenário com redução na taxa de retorno e inflação
        (taxa_retorno + 2, taxa_inflacao + 2)        # Cenário com maior aumento na taxa de retorno e inflação
    ]
    return cenarios

def gerar_graficos(resultados):
    """
    Gera gráficos comparativos para os investimentos.
    
    Parameters:
    - resultados: Lista de dicionários com os resultados dos investimentos.
    """
    # Preparar os rótulos e valores para os gráficos
    labels = [f'Investimento {i+1}' for i in range(len(resultados))]
    saldos = [res['saldo_final'] for res in resultados]
    totais_investidos = [res['total_investido'] for res in resultados]
    totais_retorno = [res['total_retorno'] for res in resultados]

    # Definindo cores para os gráficos
    colors = plt.get_cmap('tab10').colors
    fig, ax = plt.subplots(figsize=(14, 7))  # Cria uma figura e um eixo para o gráfico

    bar_width = 0.25  # Largura das barras
    x = np.arange(len(labels))  # Posições das barras
    
    # Adiciona barras para cada investimento
    for i, (total_investido, retorno, saldo_final) in enumerate(zip(totais_investidos, totais_retorno, saldos)):
        offset = i * bar_width  # Ajusta a posição da barra
        # Barra para o total investido
        bars1 = ax.bar(x + offset, total_investido, bar_width, label=f'Investimento {i+1} - Total Investido', color=colors[i][0:3])
        # Barra para o retorno gerado (acima da barra do total investido)
        bars2 = ax.bar(x + offset, retorno, bar_width, bottom=total_investido, label=f'Investimento {i+1} - Retorno Gerado', color=colors[i][0:3], alpha=0.7)
        # Barra para o saldo final (acima das barras do total investido e retorno gerado)
        bars3 = ax.bar(x + offset, saldo_final - (total_investido + retorno), bar_width, bottom=total_investido + retorno, label=f'Investimento {i+1} - Saldo Final', color=colors[i][0:3], alpha=0.5)

    # Configurações do gráfico
    ax.set_xlabel('Investimentos')
    ax.set_ylabel('Valor (R$)')
    ax.set_title('Comparação de Investimentos')
    ax.set_xticks(x + bar_width * (len(resultados) / 2))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.7)

    plt.tight_layout()  # Ajusta o layout para evitar sobreposição
    plt.savefig('comparacao_investimentos.png')  # Salva o gráfico como imagem
    plt.show()  # Exibe o gráfico

def gerar_grafico_pizza(total_investido, total_retorno, saldo_final):
    """
    Gera gráfico de pizza para mostrar a proporção dos investimentos.
    
    Parameters:
    - total_investido: Total investido.
    - total_retorno: Total gerado de retorno.
    - saldo_final: Saldo final.
    """
    labels = ['Total Investido', 'Total Gerado de Retorno', 'Saldo Final']
    valores = [total_investido, total_retorno, saldo_final]
    cores = ['#ff9999', '#66b3ff', '#99ff99']  # Definindo cores para o gráfico de pizza

    plt.figure(figsize=(8, 8))  # Cria uma nova figura para o gráfico de pizza
    plt.pie(valores, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)  # Cria o gráfico de pizza
    plt.title('Proporção dos Investimentos')

    # Exibe os valores no gráfico
    plt.text(-1.25, 1.1, f'Total Investido: R${total_investido:,.2f}', fontsize=11)
    plt.text(-1.25, 1.0, f'Total Retorno: R${total_retorno:,.2f}', fontsize=11)
    plt.text(-1.25, 0.9, f'Saldo Final: R${saldo_final:,.2f}', fontsize=11)
    
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição
    plt.savefig('grafico_pizza.png')  # Salva o gráfico como imagem
    plt.show()  # Exibe o gráfico


def gerar_relatorio_pdf(resultados):
    """
    Gera um relatório em PDF com os resultados e gráficos dos investimentos.
    
    Parameters:
    - resultados: Lista de dicionários com os resultados dos investimentos.
    """
    pdf = FPDF()  # Cria um objeto PDF
    pdf.add_page()  # Adiciona uma página ao PDF
    
    # Configurações do título do relatório
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Relatório de Investimentos', ln=True, align='C')

    # Adiciona os resultados dos investimentos ao PDF
    pdf.set_font('Arial', '', 12)
    for i, res in enumerate(resultados):
        saldo_final = res['saldo_final']
        total_investido = res['total_investido']
        total_retorno = res['total_retorno']
        pdf.cell(200, 10, f'Investimento {i+1}:', ln=True)
        pdf.cell(200, 10, f'Saldo Final: R${saldo_final:,.2f}', ln=True)
        pdf.cell(200, 10, f'Total Investido: R${total_investido:,.2f}', ln=True)
        pdf.cell(200, 10, f'Retorno Gerado: R${total_retorno:,.2f}', ln=True)
        pdf.ln(5)  # Adiciona um espaço entre as seções

    # Adiciona os gráficos ao PDF
    pdf.image('comparacao_investimentos.png', x=10, y=60, w=190)
    pdf.add_page()  # Adiciona uma nova página para o gráfico de pizza
    pdf.image('grafico_pizza.png', x=10, y=10, w=190)
    
    pdf.output('relatorio_investimentos.pdf')  # Salva o PDF com o nome especificado

# Entrada do usuário
try:
    num_investimentos = int(input("Quantos investimentos você deseja fazer? "))  # Recebe o número de investimentos
    if num_investimentos <= 0:
        raise ValueError("O número de investimentos deve ser maior que zero.")
except ValueError as e:
    print(f"Erro: {e}")  # Exibe mensagem de erro e encerra o programa
    exit()

investimentos = []

# Coleta informações sobre cada investimento
for i in range(num_investimentos):
    print(f"\nInvestimento {i+1}:")
    try:
        taxa_retorno = float(input(f"Taxa de retorno anual esperada para o investimento {i+1} (%): "))
        contribuicao_mensal = float(input(f"Quanto você quer investir mensalmente nesse investimento (R$): "))
        if taxa_retorno < 0 or contribuicao_mensal < 0:
            raise ValueError("A taxa de retorno e a contribuição mensal devem ser valores positivos.")
        investimentos.append((taxa_retorno, contribuicao_mensal))
    except ValueError as e:
        print(f"Erro: {e}")  # Exibe mensagem de erro e encerra o programa
        exit()

tempo = int(input("\nPor quanto tempo você deseja fazer esses investimentos (anos)? "))  # Recebe o período de investimento em anos

resultados = []
# Calcula os resultados para cada investimento
for i, (taxa_retorno, contribuicao_mensal) in enumerate(investimentos):
    saldo_final, total_investido, total_retorno = calcular_saldo_final(contribuicao_mensal, taxa_retorno, 2.0, tempo)
    resultados.append({
        'saldo_final': saldo_final, 
        'total_investido': total_investido,
        'total_retorno': total_retorno
    })

# Exibe os resultados no console
for i, res in enumerate(resultados):
    print(f"\nInvestimento {i+1}:")
    print(f"Total investido: R${res['total_investido']:,.2f}")
    print(f"Total de retorno gerado: R${res['total_retorno']:,.2f}")
    print(f"Saldo final: R${res['saldo_final']:,.2f}")

# Gera os gráficos comparativos e o gráfico de pizza
gerar_graficos(resultados)
primeiro_investimento = resultados[0]
gerar_grafico_pizza(primeiro_investimento['total_investido'], primeiro_investimento['total_retorno'], primeiro_investimento['saldo_final'])

# Gera o relatório PDF com os resultados e gráficos
gerar_relatorio_pdf(resultados)

print("Relatório gerado com sucesso: relatorio_investimentos.pdf")
