import streamlit as st
import numpy as np
from calculadora import economia_parcelado, desconto_quebra_taxa, parcelas_quebra_desconto, calcular_aliquota_imposto

def get_faixa_tributacao(dias_investimento):
    """
    Retorna a descrição da faixa de tributação baseada nos dias de investimento.
    """
    if dias_investimento <= 180:
        return "Até 180 dias (22,5%)"
    elif dias_investimento <= 360:
        return "181 a 360 dias (20%)"
    elif dias_investimento <= 720:
        return "361 a 720 dias (17,5%)"
    else:
        return "Acima de 720 dias (15%)"

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Parcelas vs À Vista",
    page_icon="💰",
    layout="wide"
)

# Título e descrição
st.title("Calculadora de Parcelas vs À Vista")
st.markdown("""
Esta aplicação foi feita para ajudar você a decidir se é mais vantajoso pagar à vista ou parcelar uma compra,
considerando o rendimento que você poderia ter investindo o dinheiro.
""")

# Sidebar para configurações
st.sidebar.header("")

# Taxa de juros anual
taxa_juros_anual = st.sidebar.slider(
    "Rentabilidade Anual da sua Carteira",
    min_value=0.0,
    max_value=30.0,
    value=14.9,
    step=0.1,
    help="Taxa de juros anual que você conseguiria investindo o dinheiro"
)

# Conversão para taxa mensal
taxa_juros_mensal = (1 + taxa_juros_anual/100) ** (1/12) - 1

st.sidebar.info(f"Taxa mensal equivalente: {taxa_juros_mensal*100:.2f}%")

# Informações sobre tributação na sidebar
st.sidebar.header("Imposto de Renda")
st.sidebar.markdown("""
**Faixas:**
- Até 180 dias: **22,5%**
- 181 a 360 dias: **20%**
- 361 a 720 dias: **17,5%**
- Acima de 720 dias: **15%**
""")

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["Comparação Básica", "Desconto Mínimo", "Parcelas Necessárias"])

with tab1:
    st.header("Compare o ganho ao parcelar vs pagar à vista")
    #st.markdown("Compare o ganho ao parcelar vs pagar à vista")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valor_total = st.number_input(
            "Valor Total da Compra (R$)",
            min_value=0.01,
            value=1200.0,
            step=10.0,
            format="%.2f"
        )
        
        num_parcelas = st.slider(
            "Número de Parcelas",
            min_value=1,
            max_value=24,
            value=3,
            step=1
        )
    
    with col2:
        # Cálculos
        ganho_parcelado = economia_parcelado(valor_total, num_parcelas, taxa_juros_mensal)
        valor_parcela = valor_total / num_parcelas
        
        # Cálculo da tributação
        dias_investimento = num_parcelas * 30
        aliquota_imposto = calcular_aliquota_imposto(dias_investimento)
        
        st.metric("Valor da Parcela", f"R$ {valor_parcela:.2f}")
        st.metric("Ganho Líquido", f"R$ {ganho_parcelado:.2f}")
        st.metric("Alíquota IR", f"{aliquota_imposto*100:.1f}%")
    
    # Resultado principal
    if ganho_parcelado > 0:
        st.success(f"Você ganharia R$ {ganho_parcelado:.2f} ao parcelar e investir o dinheiro.")
        #✅ **Vantajoso parcelar!**
    else:
        st.error(f"❌ **Melhor pagar à vista!** Você perderia R$ {abs(ganho_parcelado):.2f} ao parcelar.")
    
    # Informações sobre tributação
    #st.info(f"""
    #**📊 Informações sobre Tributação:**
    #- Tempo de investimento: **{dias_investimento} dias** ({num_parcelas} meses)
    #- Alíquota de IR: **{aliquota_imposto*100:.1f}%**
    #- Faixa de tributação: **{get_faixa_tributacao(dias_investimento)}**
    #""")
    
    # Gráfico de evolução do saldo
    st.subheader("📈 Evolução do Saldo Investido")
    
    # Simulação mês a mês
    meses = list(range(num_parcelas + 1))
    saldos = [valor_total]
    
    for i in range(1, num_parcelas + 1):
        saldo_anterior = saldos[-1]
        saldo_novo = saldo_anterior * (1 + taxa_juros_mensal) - valor_parcela
        saldos.append(saldo_novo)
    
    import plotly.graph_objects as go
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses,
        y=saldos,
        mode='lines+markers',
        name='Saldo Investido',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Evolução do Saldo ao Longo dos Meses",
        xaxis_title="Mês",
        yaxis_title="Saldo (R$)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Descubra qual desconto no pagamento à vista seria equivalente ao parcelamento")
    #st.markdown("Descubra qual desconto no pagamento à vista seria equivalente ao parcelamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valor_total_2 = st.number_input(
            "Valor Total da Compra (R$)",
            key="valor_total_2",
            min_value=0.01,
            value=1200.0,
            step=10.0,
            format="%.2f"
        )
        
        num_parcelas_2 = st.slider(
            "Número de Parcelas",
            key="num_parcelas_2",
            min_value=1,
            max_value=24,
            value=12,
            step=1
        )
    
    with col2:
        # Cálculo do desconto necessário
        desconto_necessario, valor_avista_equivalente = desconto_quebra_taxa(
            valor_total_2, num_parcelas_2, taxa_juros_mensal
        )
        
        st.metric("Desconto Necessário", f"{desconto_necessario:.2f}%")
        st.metric("Valor à Vista Equivalente", f"R$ {valor_avista_equivalente:.2f}")
        st.metric("Economia: R$", f"{valor_total_2 - valor_avista_equivalente:.2f}")
    
    # Resultado
    #st.info(f"""
    #**Para que o pagamento à vista seja equivalente ao parcelamento:**
    #- Desconto mínimo necessário: **{desconto_necessario:.2f}%**
    #- Valor à vista equivalente: **R$ {valor_avista_equivalente:.2f}**
    #- Economia: **R$ {valor_total_2 - valor_avista_equivalente:.2f}**
    #""")
    
    # Comparação visual
    #st.subheader("📊 Comparação Visual")
    
    #fig = go.Figure(data=[
    #    go.Bar(name='Valor Total', x=['Valor'], y=[valor_total_2], marker_color='red'),
    #    go.Bar(name='Valor à Vista Equivalente', x=['Valor'], y=[valor_avista_equivalente], marker_color='green')
    #])
    
    #fig.update_layout(
    #    title="Comparação: Valor Total vs Valor à Vista Equivalente",
    #    yaxis_title="Valor (R$)",
    #    barmode='group'
    #)
    
    #st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Descubra quantas parcelas são necessárias para superar um desconto à vista")
    #st.markdown("Descubra quantas parcelas são necessárias para superar um desconto à vista")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valor_total_3 = st.number_input(
            "Valor Total da Compra (R$)",
            key="valor_total_3",
            min_value=0.01,
            value=1200.0,
            step=10.0,
            format="%.2f"
        )
        
        desconto_dado = st.slider(
            "Desconto à Vista (%)",
            min_value=0.0,
            max_value=99.0,
            value=10.0,
            step=0.5
        )
    
    with col2:
        # Cálculo das parcelas necessárias
        parcelas_necessarias, ganho_obtido = parcelas_quebra_desconto(
            valor_total_3, desconto_dado, taxa_juros_mensal
        )
        
        if parcelas_necessarias:
            st.metric("Parcelas Necessárias", f"{parcelas_necessarias}")
            st.metric("Ganho ao Parcelar", f"R$ {ganho_obtido:.2f}")
        else:
            st.metric("Parcelas Necessárias", "Não viável")
            st.metric("Ganho ao Parcelar", "R$ 0.00")
    
    # Resultado
    valor_avista_desconto = valor_total_3 * (1 - desconto_dado/100)
    
    if parcelas_necessarias:
        st.success(f"""
        **✅ Parcelamento viável!**
        - Desconto à vista: **{desconto_dado}%** (R$ {valor_avista_desconto:.2f})
        - Parcelas necessárias: **{parcelas_necessarias}**
        - Ganho ao parcelar: **R$ {ganho_obtido:.2f}**
        """)
    else:
        st.error(f"""
        **❌ Parcelamento não viável**
        - Desconto à vista: **{desconto_dado}%** (R$ {valor_avista_desconto:.2f})
        - Mesmo com 60 parcelas, o parcelamento não supera o desconto
        """)
    
    # Análise de diferentes quantidades de parcelas
    st.subheader("Análise por Quantidade de Parcelas")
    
    parcelas_teste = list(range(1, 61))
    ganhos = []
    
    for p in parcelas_teste:
        ganho = economia_parcelado(valor_total_3, p, taxa_juros_mensal)
        ganhos.append(ganho)
    
    # Encontrar o ponto de equilíbrio
    economia_desconto = valor_total_3 - valor_avista_desconto
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=parcelas_teste,
        y=ganhos,
        mode='lines',
        name='Ganho ao Parcelar',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_hline(
        y=economia_desconto,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Economia do desconto ({desconto_dado}%)"
    )
    
    if parcelas_necessarias:
        fig.add_vline(
            x=parcelas_necessarias,
            line_dash="dot",
            line_color="green",
            annotation_text=f"Ponto de equilíbrio: {parcelas_necessarias} parcelas"
        )
    
    fig.update_layout(
        title="Ganho ao Parcelar vs Número de Parcelas",
        xaxis_title="Número de Parcelas",
        yaxis_title="Ganho (R$)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
#st.markdown("""
#<div style='text-align: center; color: #666;'>
#    <p>💡 <strong>Dica:</strong> Esta calculadora considera que você investiria o dinheiro total 
#    e pagaria as parcelas mensalmente com o rendimento. A tributação de IR é aplicada no final do período.</p>
#    <p>📊 <strong>Tributação IR:</strong> Até 180 dias (22,5%) | 181-360 dias (20%) | 361-720 dias (17,5%) | Acima de 720 dias (15%)</p>
#</div>
#""", unsafe_allow_html=True) 