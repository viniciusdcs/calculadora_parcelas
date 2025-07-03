import numpy as np

dic_imposto = {
    180: 0.225,    # Até 180 dias: 22,5%
    360: 0.20,     # De 181 a 360 dias: 20%
    720: 0.175,    # De 361 a 720 dias: 17,5%
    float('inf'): 0.15  # Acima de 720 dias: 15%
}

def calcular_aliquota_imposto(dias_investimento):
    """
    Calcula a alíquota de imposto baseada no tempo de investimento.
    
    Parâmetros:
        dias_investimento (int): Número de dias de investimento.
    
    Retorna:
        aliquota (float): Alíquota de imposto (0 a 1).
    """
    for dias_limite, aliquota in sorted(dic_imposto.items()):
        if dias_investimento <= dias_limite:
            return aliquota
    return 0.15  # Fallback

# ===============================
# Função 1: Economia ao parcelar e aplicar o valor
# ===============================
def economia_parcelado(valor_total, parcelas, taxa_juros_mensal):
    """
    Calcula quanto você ganharia ao investir o valor total da compra
    e pagar as parcelas mês a mês, considerando a tributação no último mês.

    Parâmetros:
        valor_total (float): Valor total da compra.
        parcelas (int): Número de parcelas mensais.
        taxa_juros_mensal (float): Taxa de juros mensal (ex: 0.00797 para 10% a.a.).

    Retorna:
        ganho (float): Valor restante após aplicar, pagar as parcelas e tributar.
    """
    valor_aplicado = valor_total  # valor aplicado inicialmente
    valor_inicial = valor_total
    
    for i in range(1, parcelas + 1):
        valor_aplicado *= (1 + taxa_juros_mensal)  # rende por mais um mês
        valor_aplicado -= valor_total / parcelas   # paga uma parcela mensalmente
    
    # Calcula o ganho bruto (sem imposto)
    ganho_bruto = valor_aplicado
    
    # Calcula o rendimento total (valor final - valor inicial)
    rendimento_total = ganho_bruto - valor_inicial
    
    # Se houve ganho, aplica a tributação
    if rendimento_total > 0:
        # Calcula os dias de investimento (aproximadamente parcelas * 30)
        dias_investimento = parcelas * 30
        aliquota_imposto = calcular_aliquota_imposto(dias_investimento)
        
        # Calcula o imposto sobre o rendimento
        imposto = rendimento_total * aliquota_imposto
        
        # Ganho líquido após imposto
        ganho_liquido = ganho_bruto - imposto
    else:
        ganho_liquido = ganho_bruto
    
    return ganho_liquido


# ===============================
# Função 2: Qual desconto à vista "quebra" o parcelamento
# ===============================
def desconto_quebra_taxa(valor_total, parcelas, taxa_juros_mensal):
    """
    Calcula qual seria o desconto mínimo necessário no pagamento à vista
    para que ele seja mais vantajoso do que parcelar e investir o dinheiro.

    Parâmetros:
        valor_total (float): Valor cheio da compra.
        parcelas (int): Número de parcelas.
        taxa_juros_mensal (float): Taxa de juros mensal.

    Retorna:
        desconto_percentual (float): Desconto mínimo necessário (%).
        valor_minimo_avista (float): Valor que seria pago com esse desconto.
    """
    ganho = economia_parcelado(valor_total, parcelas, taxa_juros_mensal)
    valor_minimo_avista = valor_total - ganho
    desconto_percentual = 100 * (1 - valor_minimo_avista / valor_total)
    return desconto_percentual, valor_minimo_avista


# ===============================
# Função 3: Quantas parcelas eu preciso para superar o desconto à vista
# ===============================
def parcelas_quebra_desconto(valor_total, desconto_percentual, taxa_juros_mensal, max_parcelas=60):
    """
    Dado um desconto no pagamento à vista e uma taxa de juros,
    calcula quantas parcelas são necessárias para que o parcelamento
    supere o valor do desconto.

    Parâmetros:
        valor_total (float): Valor cheio da compra.
        desconto_percentual (float): Desconto dado no PIX (%).
        taxa_juros_mensal (float): Taxa de juros mensal da aplicação.
        max_parcelas (int): Máximo de parcelas que deseja considerar.

    Retorna:
        n (int): Número mínimo de parcelas para que parcelar seja vantajoso.
        ganho (float): Ganho obtido ao parcelar e aplicar o dinheiro.
    """
    valor_avista = valor_total * (1 - desconto_percentual / 100)

    for n in range(1, max_parcelas + 1):
        ganho = economia_parcelado(valor_total, n, taxa_juros_mensal)
        if ganho >= valor_total - valor_avista:
            return n, ganho
    return None, None  # Caso nenhuma quantidade de parcelas seja vantajosa



# Simulação com os parâmetros fornecidos
valor_compra = 1200
parcelas = 12
taxa_juros_anual = 0.10
taxa_juros_mensal = (1 + taxa_juros_anual) ** (1/12) - 1  # conversão para taxa mensal

# Cálculo do desconto necessário
desconto_necessario, valor_pix_equivalente = desconto_quebra_taxa(valor_compra, parcelas, taxa_juros_mensal)
desconto_necessario, valor_pix_equivalente
