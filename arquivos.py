import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu


def peak_shaving_app():
    st.header("Simulação de Aplicação: Peak Shaving")
    st.markdown("""
    O **Peak Shaving** (redução de picos de demanda) é uma das principais aplicações de um BESS. O objetivo é utilizar a energia armazenada nas baterias para alimentar as cargas durante os horários em que a demanda de energia da rede elétrica atinge seu pico, geralmente entre **18:00 e 21:00**.
    
    Isso reduz os custos com tarifas de demanda e alivia a sobrecarga na rede elétrica.
    
    O gráfico abaixo simula este cenário:
    - **Azul (Rede):** Potência fornecida pela rede elétrica.
    - **Vermelho (BESS):** Potência fornecida pelo BESS.
    
    Observe como a potência da rede é "achatada" durante o horário de pico, enquanto o BESS assume a responsabilidade.
    """)

    # --- GERAÇÃO DE DADOS PARA A SIMULAÇÃO ---
    horas = list(range(24))
    
    # Demanda de carga típica ao longo do dia, com um pico acentuado à noite
    demanda_total = [
        80, 75, 70, 65, 68, 80, 100, 110, 120, 130, 135, 140, 
        138, 142, 150, 160, 180, 250, 255, 252, 248, 180, 150, 110
    ]
    
    # Operação do BESS e da Rede
    potencia_bess = []
    potencia_rede = []
    
    # Potência que o BESS vai fornecer no pico
    potencia_pico_bess = 150 # MW

    for hora, demanda in zip(horas, demanda_total):
        # Horário de pico (18:00 às 21:00) -> BESS descarrega
        if 18 <= hora <= 21:
            # BESS fornece a maior parte da energia
            bess_fornece = min(demanda, potencia_pico_bess)
            potencia_bess.append(bess_fornece)
            # A rede fornece apenas o restante, "achatando" o pico
            potencia_rede.append(demanda - bess_fornece)
        # Horário de carga (madrugada, 00:00 às 04:00) -> BESS carrega
        elif 0 <= hora <= 4:
            # BESS consome energia da rede para carregar
            potencia_bess.append(-50) # Carregando com 50 MW
            # A rede fornece a demanda da carga + a carga do BESS
            potencia_rede.append(demanda - (-50)) 
        # Demais horários -> BESS fica em espera
        else:
            potencia_bess.append(0)
            potencia_rede.append(demanda)

    # Criando o DataFrame
    df_simulacao = pd.DataFrame({
        'Hora': horas,
        'Demanda Total (MW)': demanda_total,
        'Potência da Rede (MW)': potencia_rede,
        'Potência do BESS (MW)': potencia_bess
    })
    
    # --- CRIAÇÃO DO GRÁFICO ---
    
    # Para o gráfico de área empilhada, precisamos "derreter" (melt) o dataframe
    # para ter uma coluna para a fonte de energia e outra para o valor.
    df_plot = df_simulacao.melt(
        id_vars='Hora', 
        value_vars=['Potência da Rede (MW)', 'Potência do BESS (MW)'],
        var_name='Fonte de Potência', 
        value_name='Potência (MW)'
    )
    
    # Removemos os valores negativos do BESS para não poluir o gráfico de fornecimento
    df_plot['Potência (MW)'] = df_plot['Potência (MW)'].clip(lower=0)

    # Gráfico de área empilhada
    fig = px.area(
        df_plot, 
        x='Hora', 
        y='Potência (MW)', 
        color='Fonte de Potência',
        title='Simulação de Peak Shaving: Fornecimento de Potência (Rede vs. BESS)',
        labels={'Hora': 'Hora do Dia', 'Potência (MW)': 'Potência Fornecida (MW)'},
        color_discrete_map={
            'Potência da Rede (MW)': 'royalblue',
            'Potência do BESS (MW)': 'firebrick'
        }
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis=dict(tickmode='linear', dtick=2),
        yaxis_title="Potência (MW)",
        legend_title_text='Fonte de Energia'
    )

    # --- PÁGINA: BMS - BALANCEAMENTO ---
    st.header("BMS: Métodos de Balanceamento de Células")
    st.markdown("O balanceamento é uma função crítica do BMS para garantir um Estado de Carga (SoC) uniforme entre todas as células, o que maximiza a capacidade utilizável e a vida útil da bateria. Existem duas abordagens principais: **Passiva** e **Ativa**.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Balanceamento Passivo")
        st.markdown("Este método **dissipa o excesso de energia** das células com maior SoC na forma de calor, geralmente através de resistores. ")
        
        st.info("**Tipos Comuns:**")
        st.markdown("""
        - Resistores fixos 
        - Resistores com Diodo Zener
        - Resistores com chaves controladas pelo BMS 
        """)

        st.write(" ")
        st.dataframe(pd.DataFrame({
            "Vantagens 👍": ["Simplicidade do circuito", "Menor custo", "Fácil de projetar"],
            "Desvantagens 👎": ["Desperdício de energia (calor)", "Pode afetar células vizinhas com o calor gerado", "Menos eficiente"]
        }), use_container_width=True)
        st.caption("Baseado na tabela da pág. 35 do documento. ")
        
    with col2:
        st.subheader("Balanceamento Ativo")
        st.markdown("Este método **transfere a carga** de células com SoC mais alto para aquelas com SoC mais baixo, sem dissipar a energia como calor.")

        st.info("**Tipos Comuns:**")
        st.markdown("""
        - Baseado em capacitores 
        - Baseado em indutores/transformadores 
        - Baseado em conversores DC-DC 
        """)

        st.write(" ")
        st.dataframe(pd.DataFrame({
        "Vantagens 👍": ["Alta eficiência energética", "Maximiza o uso da capacidade", "Balanceamento mais rápido", "Melhora a vida útil"],
        "Desvantagens 👎": ["Circuitos mais complexos", "Custo de fabricação mais alto", "Maior dificuldade na construção", ""] # <-- Adicionado item vazio para igualar o tamanho
        }), use_container_width=True)
        st.caption("Baseado na tabela da pág. 75 do documento. ")


    # --- PÁGINA: BMS - ESTIMAÇÃO DE ESTADOS ---
    st.header("BMS: Estimação de Estados da Bateria")
    st.markdown("Além do controle e segurança, o BMS é crucial para estimar parâmetros que indicam a condição atual da bateria. ")

    tab_soc, tab_soh, tab_sop = st.tabs(["**Estado de Carga (SoC)**", "**Estado de Saúde (SoH)**", "**Estado de Potência (SoP)**"])

    with tab_soc:
        st.subheader("Estimação do SoC (State of Charge)")
        st.markdown("Indica a capacidade disponível em uma bateria como uma porcentagem de sua capacidade nominal.")
        st.markdown("**Principais Métodos de Estimação:**")
        st.markdown("""
        - **Método Baseado em Tensão:** O mais simples, correlaciona a tensão terminal com o SoC, mas é pouco preciso devido a efeitos de temperatura, envelhecimento e corrente.""")
        st.markdown("---")
        st.markdown("""
        - **Contagem de Coulomb:** Monitora a corrente de entrada e saída para calcular a carga restante. É mais preciso, mas propenso a erros cumulativos.""")
        st.markdown("""
            Uma das equações mais importantes para um BESS é a que descreve seu estado de carga. A forma mais simples (desconsiderando perdas complexas) é a integração da potência ao longo do tempo.
            
            """)
            # Usando st.latex para renderizar equações matemáticas
        st.latex(r'''
            SoC(t) = SoC(t_0) + \frac{1}{C_{rated}} \int_{t_0}^{t} I_{bateria}(\tau) d\tau
            ''')
        st.markdown(r'''
            Onde:
            - $SoC(t)$ é o estado de carga no tempo $t$.
            - $C_{rated}$ é a capacidade nominal da bateria (ex: em MWh).
            - $I_{bateria}(\tau)$ é a corrente que alimenta as baterias no instante $\tau$ (positiva para carga, negativa para descarga).
            ''')

        st.markdown("---")
        st.markdown("""
        - **Filtro de Kalman:** Usa um modelo da bateria para prever o SoC, sendo mais robusto a ruídos e incertezas de medição.
        - **Redes Neurais:** Aprende com os ciclos de carga/descarga anteriores para estimar o SoC, com tendência a maior precisão ao longo do tempo.
        - **Espectroscopia de Impedância (EIS):** Um dos mais precisos, mas sua complexidade e custo o tornam pouco usual para a maioria das aplicações de BMS.
        """)

    with tab_soh:
        st.subheader("Estimação do SoH (State of Health)")
        st.markdown("Indica a capacidade atual de uma bateria em comparação com sua capacidade nominal quando nova. Um SoH de 100% significa que a bateria não teve perda de capacidade. Ajuda a prever a vida útil restante.")
        st.markdown("**Principais Métodos de Estimação:**")
        st.markdown("""
        - **Comparação de Capacidade:** Compara a capacidade máxima atual (obtida com um ciclo completo) com a capacidade original.
        - **Estimativa Baseada em Modelo:** Usa modelos matemáticos que representam o comportamento da bateria e os ajusta com dados reais. 
        - **Aprendizado de Máquina:** Utiliza algoritmos (como SVM ou Redes Neurais) para prever o SoH a partir de dados históricos.
        - **Medição de Impedância:** O SoH é determinado medindo a impedância interna da bateria, que aumenta com o envelhecimento. 
        """)

    with tab_sop:
        st.subheader("Estimação do SoP (State of Power)")
        st.markdown("Indica a capacidade da bateria de fornecer ou absorver uma determinada quantidade de energia em um instante. É crucial para o gerenciamento de energia em aplicações com rápidas variações de potência, como veículos elétricos e BESS.")
        st.markdown("A equação para o SoP é definida como:")
        st.latex(r'''
        SoP(t) = \frac{P_{max}(t)}{P_{nominal}(t)} \times 100 \ [\%] 
        ''')
        st.caption("Onde $P_{max}(t)$ é a potência de pico e $P_{nominal}(t)$ é a potência nominal.")

def pcs():
    # --- PÁGINA: PCS - CONVERSÃO DE POTÊNCIA ---
    st.header("PCS (Power Conversion System)")
    st.markdown("O PCS é o cérebro e a força do BESS, responsável por converter a energia entre Corrente Contínua (CC) das baterias e Corrente Alternada (CA) da rede elétrica, e por controlar ativamente o fluxo de potência.")

    st.subheader("Principais Funções e Topologias de Controle")
    st.markdown("A principal funcionalidade do controle do PCS é operar em diferentes modos, dependendo do estado da rede elétrica. A transição suave (*seamless*) entre esses modos é fundamental para a estabilidade do sistema.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.info("### Modo Seguidor de Rede (Grid-Following)")
        st.markdown("""
        - Também conhecido como **Grid-Tied** ou **Grid-Supporting**.
        - Opera quando a rede elétrica principal está **ativa e estável**.
        - O PCS **sincroniza** com a frequência e tensão da rede.
        - Atua como uma fonte de corrente, injetando ou absorvendo potência ativa (P) e reativa (Q) conforme os comandos recebidos.
        - Não consegue operar de forma independente (ilhado).
        """)

    with col2:
        st.info("### Modo Formador de Rede (Grid-Forming)")
        st.markdown("""
        - Essencial para a operação em **modo ilhado** (desconectado da rede principal).
        - O PCS **cria e estabelece** a referência de tensão e frequência da microrrede, atuando como uma fonte de tensão.
        - Permite o *black start*, ou seja, a capacidade de reenergizar uma parte da rede após um apagão.
        - Pelo menos uma fonte na microrrede (geralmente um BESS ou gerador síncrono) deve ter essa capacidade.
        """)

def ems():
    st.markdown("""Em produção""")