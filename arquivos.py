import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu


def app ():
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

def bms():
    # --- PÁGINA: BMS - GESTÃO E SEGURANÇA ---
    st.header("BMS: Gestão e Segurança da Bateria")
    st.markdown(
        "O **Battery Management System (BMS)** é um sistema eletrônico responsável por monitorar e gerenciar um sistema de baterias, garantindo seu desempenho, segurança e durabilidade. [0: 22, 23] [0_start]Ele pode atuar em diversos níveis, desde a célula individual até o rack completo de baterias. [0: 22]"
    )

    st.subheader("Cuidados Essenciais: A Fuga Térmica (Thermal Runaway)")
    st.warning("A proteção do sistema de baterias é uma das principais funções de um BMS. Um dos maiores riscos em baterias de Íon-Lítio é a **fuga térmica**.")

    with st.expander("Clique aqui para saber mais sobre a Fuga Térmica"):
        st.markdown(
            "A fuga térmica é uma condição de autoaquecimento rápido de uma célula, originada de uma reação química exotérmica entre os eletrodos. [0: 44] [0_start]Durante este evento, a célula libera sua energia armazenada de forma abrupta e descontrolada. [0: 45]"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.error("Causas Principais:")
            st.markdown("""
            - Sobrecarga ou descarga excessiva
            - Alta corrente de operação 
            - Operação fora da faixa de temperatura permitida 
            - O autoaquecimento pode iniciar-se a temperaturas entre 70°C e 90°C. 
            """)
        
        with col2:
            st.error("Consequências:")
            st.markdown("""
            - Rápido aumento da temperatura interna da célula, podendo atingir **600°C** 
            - Aumento da pressão interna devido à vaporização e decomposição do eletrólito 
            - Risco de incêndio ou explosão da bateria 
            - Fusão de componentes internos como o separador e coletores de corrente 
            """)
        
        st.success(
            "O BMS monitora continuamente as condições da bateria e atua para interromper situações de risco, "
            "desligando a bateria ou ajustando as taxas de carga/descarga para prevenir a fuga térmica. "
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
            - $\eta$ é a eficiência de carga/descarga.
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