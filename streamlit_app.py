import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu


# =============================================================================
# BIBLIOTECAS DE ASSUNTOS


# =============================================================================

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# st.set_page_config deve ser o primeiro comando Streamlit a ser executado
# =============================================================================
st.set_page_config(
    page_title="Relatório BESS",
    page_icon="🔋",
    layout="wide", # 'wide' ou 'centered'
    initial_sidebar_state="expanded" # 'auto', 'expanded', 'collapsed'
)

# =============================================================================
# MENU LATERAL (SIDEBAR)
# Usando a biblioteca streamlit-option-menu
# =============================================================================
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",  # Obrigatório
        options=["Página Inicial", "BMS", "PCS", "EMS", "Aplicações e Gráficos", "Equações e Código"],  # Obrigatório
        icons=["house", "folder", "folder", "folder", "question-circle", "bar-chart-line", "code-slash"],  # Opcional (ícones do Bootstrap)
        menu_icon="cloud",  # Opcional
        default_index=0,  # Opcional
        orientation="vertical", # "horizontal" ou "vertical"
    )

# =============================================================================
# CONTEÚDO DAS PÁGINAS
# A lógica para exibir a página selecionada no menu
# =============================================================================

# --- PÁGINA INICIAL ---
if selected == "Página Inicial":
    st.title("🔋 Análise e Informações sobre BESS")
    st.markdown("---")
    st.markdown("""
    Bem-vindo ao seu painel de informações sobre **Sistemas de Armazenamento de Energia por Baterias (BESS)**.
    
    Este é um ambiente interativo criado com Streamlit para consolidar conhecimentos, análises e dados sobre BESS.
    
    **Navegue pelo menu à esquerda para explorar as seções:**
    - **O que é BESS?:** Uma introdução conceitual.
    - **Aplicações e Gráficos:** Veja casos de uso e analise dados interativos.
    - **Equações e Código:** Explore os modelos matemáticos e códigos de simulação por trás da tecnologia.
    """)
    st.image("https://via.placeholder.com/800x300.png?text=Imagem+Conceitual+de+um+BESS", caption="Substitua por uma imagem real de um BESS.")


# --- PÁGINA: O QUE É BESS? ---
if selected == "O que é BESS?":
    st.header("O que é um Sistema de Armazenamento de Energia por Baterias (BESS)?")
    st.markdown("""
    Um BESS é uma solução tecnológica que utiliza baterias recarregáveis para armazenar energia elétrica e disponibilizá-la posteriormente. 
    Ele é composto por três componentes principais:
    
    1.  **Baterias:** O coração do sistema, onde a energia é quimicamente armazenada.
    2.  **Sistema de Gerenciamento de Bateria (BMS - Battery Management System):** Garante a operação segura e eficiente das baterias, monitorando tensão, corrente e temperatura.
    3.  **Conversor de Potência (PCS - Power Conversion System):** Converte a corrente contínua (CC) das baterias em corrente alternada (CA) para a rede elétrica, e vice-versa.
    """)
    st.warning("Esta seção é ideal para textos explicativos, imagens e diagramas.")


# --- PÁGINA: APLICAÇÕES E GRÁFICOS ---
if selected == "Aplicações e Gráficos":
    st.header("Aplicações e Análise Gráfica")
    st.markdown("""
    BESS são usados em diversas aplicações, como *peak shaving*, regulação de frequência, integração de fontes renováveis e backup de energia.
    
    Abaixo, um exemplo de gráfico interativo que simula um ciclo de carga e descarga de um BESS para arbitragem de energia (comprar na baixa, vender na alta).
    """)

    # Criando dados de exemplo com Pandas
    data = {
        'Hora': list(range(24)),
        'Preço Energia (R$/MWh)': [120, 110, 105, 100, 115, 150, 200, 250, 280, 300, 290, 270, 260, 250, 280, 350, 450, 550, 600, 500, 400, 300, 200, 150],
        'Operação BESS (MW)': [-50, -50, -50, -50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 0, 0, 0, -25, -25] # Negativo = Carregando, Positivo = Descarregando
    }
    df = pd.DataFrame(data)

    # Gráfico de Preço da Energia
    fig_preco = px.line(df, x='Hora', y='Preço Energia (R$/MWh)', title='Preço Spot da Energia ao Longo do Dia', markers=True)
    fig_preco.update_layout(title_x=0.5)
    st.plotly_chart(fig_preco, use_container_width=True)

    # Gráfico de Operação do BESS
    fig_bess = px.bar(df, x='Hora', y='Operação BESS (MW)', title='Operação do BESS (Carga/Descarga)', color='Operação BESS (MW)',
                      color_continuous_scale=px.colors.diverging.RdYlBu_r)
    fig_bess.update_layout(title_x=0.5)
    st.plotly_chart(fig_bess, use_container_width=True)
    st.info("Passe o mouse sobre os gráficos para ver os valores detalhados.")


# --- PÁGINA: EQUAÇÕES E CÓDIGO ---
if selected == "Equações e Código":
    st.header("Equações Fundamentais e Códigos de Simulação")
    
    st.subheader("Equação do Estado de Carga (State of Charge - SoC)")
    st.markdown("""
    Uma das equações mais importantes para um BESS é a que descreve seu estado de carga. A forma mais simples (desconsiderando perdas complexas) é a integração da potência ao longo do tempo.
    
    Abaixo, a equação em formato LaTeX:
    """)
    # Usando st.latex para renderizar equações matemáticas
    st.latex(r'''
    SoC(t) = SoC(t_0) + \frac{1}{C_{rated}} \int_{t_0}^{t} \eta \cdot P_{bateria}(\tau) d\tau
    ''')
    st.markdown(r'''
    Onde:
    - $SoC(t)$ é o estado de carga no tempo $t$.
    - $C_{rated}$ é a capacidade nominal da bateria (ex: em MWh).
    - $P_{bateria}(\tau)$ é a potência da bateria no tempo $\tau$ (positiva para carga, negativa para descarga).
    - $\eta$ é a eficiência de carga/descarga.
    ''')

    st.markdown("---")
    
    st.subheader("Exemplo de Código Python")
    st.markdown("A seguir, um exemplo de uma função Python simples que poderia ser usada para simular a variação do SoC.")
    
    # Usando st.code para exibir um bloco de código
    codigo_python = """
def simular_soc(soc_inicial, potencia, duracao_horas, capacidade_mwh, eficiencia=0.9):
    '''
    Simula a variação do Estado de Carga de uma bateria.
    
    Args:
    - soc_inicial (float): Estado de carga inicial (entre 0 e 1).
    - potencia (float): Potência de carga (+) ou descarga (-) em MW.
    - duracao_horas (float): Duração da operação em horas.
    - capacidade_mwh (float): Capacidade total da bateria em MWh.
    - eficiencia (float): Eficiência de ida e volta.
    
    Returns:
    - float: Novo estado de carga.
    '''
    
    # Aplica eficiência (perdas)
    if potencia > 0: # Carregando
        potencia_efetiva = potencia * eficiencia
    else: # Descarregando
        potencia_efetiva = potencia / eficiencia
        
    energia_transacionada = potencia_efetiva * duracao_horas
    variacao_soc = energia_transacionada / capacidade_mwh
    
    soc_final = soc_inicial + variacao_soc
    
    # Garante que o SoC fique entre 0 e 1
    return max(0, min(1, soc_final))

# Exemplo de uso:
soc_novo = simular_soc(soc_inicial=0.5, potencia=-10, duracao_horas=2, capacidade_mwh=50)
print(f"O novo Estado de Carga é: {soc_novo*100:.2f}%")
    """
    st.code(codigo_python, language='python')
