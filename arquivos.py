import streamlit as st
import pandas as pd
import plotly.express as px

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

def bess():
    # --- PÁGINA: BMS - GESTÃO E SEGURANÇA ---
    st.header("BMS: Gestão e Segurança da Bateria")
    st.markdown(
        "O **Battery Management System (BMS)** é um sistema eletrônico responsável por monitorar e gerenciar um sistema de baterias, garantindo seu desempenho, segurança e durabilidade. [cite: 22, 23] [cite_start]Ele pode atuar em diversos níveis, desde a célula individual até o rack completo de baterias. [cite: 22]"
    )

    st.subheader("Cuidados Essenciais: A Fuga Térmica (Thermal Runaway)")
    st.warning("A proteção do sistema de baterias é uma das principais funções de um BMS. [cite: 24] Um dos maiores riscos em baterias de Íon-Lítio é a **fuga térmica**.")

    with st.expander("Clique aqui para saber mais sobre a Fuga Térmica"):
        st.markdown(
            "A fuga térmica é uma condição de autoaquecimento rápido de uma célula, originada de uma reação química exotérmica entre os eletrodos. [cite: 44] [cite_start]Durante este evento, a célula libera sua energia armazenada de forma abrupta e descontrolada. [cite: 45]"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.error("Causas Principais:")
            st.markdown("""
            - Sobrecarga ou descarga excessiva [cite: 33]
            - Alta corrente de operação [cite: 33]
            - Operação fora da faixa de temperatura permitida [cite: 33]
            - O autoaquecimento pode iniciar-se a temperaturas entre 70°C e 90°C. [cite: 67]
            """)
        
        with col2:
            st.error("Consequências:")
            st.markdown("""
            - Rápido aumento da temperatura interna da célula, podendo atingir **600°C** [cite: 86]
            - Aumento da pressão interna devido à vaporização e decomposição do eletrólito [cite: 98, 103]
            - Risco de incêndio ou explosão da bateria [cite: 33]
            - Fusão de componentes internos como o separador e coletores de corrente [cite: 90]
            """)
        
        st.success(
            "O BMS monitora continuamente as condições da bateria e atua para interromper situações de risco, "
            "desligando a bateria ou ajustando as taxas de carga/descarga para prevenir a fuga térmica. [cite: 34]"
        )

    # --- PÁGINA: BMS - BALANCEAMENTO ---
    st.header("BMS: Métodos de Balanceamento de Células")
    st.markdown("O balanceamento é uma função crítica do BMS para garantir um Estado de Carga (SoC) uniforme entre todas as células, o que maximiza a capacidade utilizável e a vida útil da bateria. [cite: 263, 308] [cite_start]Existem duas abordagens principais: **Passiva** e **Ativa**. [cite: 265]")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Balanceamento Passivo")
        st.markdown("Este método **dissipa o excesso de energia** das células com maior SoC na forma de calor, geralmente através de resistores. [cite: 275]")
        
        st.info("**Tipos Comuns:**")
        st.markdown("""
        - Resistores fixos [cite: 319]
        - Resistores com Diodo Zener [cite: 320]
        - Resistores com chaves controladas pelo BMS [cite: 323]
        """)

        st.write(" ")
        st.dataframe(pd.DataFrame({
            "Vantagens 👍": ["Simplicidade do circuito", "Menor custo", "Fácil de projetar"],
            "Desvantagens 👎": ["Desperdício de energia (calor)", "Pode afetar células vizinhas com o calor gerado", "Menos eficiente"]
        }), use_container_width=True)
        st.caption("Baseado na tabela da pág. 35 do documento. [cite: 498]")
        
    with col2:
        st.subheader("Balanceamento Ativo")
        st.markdown("Este método **transfere a carga** de células com SoC mais alto para aquelas com SoC mais baixo, sem dissipar a energia como calor. [cite: 296]")

        st.info("**Tipos Comuns:**")
        st.markdown("""
        - Baseado em capacitores [cite: 318]
        - Baseado em indutores/transformadores [cite: 321, 322]
        - Baseado em conversores DC-DC [cite: 324, 325]
        """)

        st.write(" ")
        st.dataframe(pd.DataFrame({
            "Vantagens 👍": ["Alta eficiência energética", "Maximiza o uso da capacidade", "Balanceamento mais rápido", "Melhora a vida útil"],
            "Desvantagens 👎": ["Circuitos mais complexos", "Custo de fabricação mais alto", "Maior dificuldade na construção"]
        }), use_container_width=True)
        st.caption("Baseado na tabela da pág. 75 do documento. [cite: 2027]")


    # --- PÁGINA: BMS - ESTIMAÇÃO DE ESTADOS ---
    st.header("BMS: Estimação de Estados da Bateria")
    st.markdown("Além do controle e segurança, o BMS é crucial para estimar parâmetros que indicam a condição atual da bateria. [cite: 2032]")

    tab_soc, tab_soh, tab_sop = st.tabs(["**Estado de Carga (SoC)**", "**Estado de Saúde (SoH)**", "**Estado de Potência (SoP)**"])

    with tab_soc:
        st.subheader("Estimação do SoC (State of Charge)")
        st.markdown("Indica a capacidade disponível em uma bateria como uma porcentagem de sua capacidade nominal. [cite: 2045, 2048]")
        st.markdown("**Principais Métodos de Estimação:**")
        st.markdown("""
        - **Método Baseado em Tensão:** O mais simples, correlaciona a tensão terminal com o SoC, mas é pouco preciso devido a efeitos de temperatura, envelhecimento e corrente. [cite: 2049, 2050]
        - **Contagem de Coulomb:** Monitora a corrente de entrada e saída para calcular a carga restante. [cite_start]É mais preciso, mas propenso a erros cumulativos. [cite: 2058, 2059]
        - **Filtro de Kalman:** Usa um modelo da bateria para prever o SoC, sendo mais robusto a ruídos e incertezas de medição. [cite: 2060, 2070]
        - **Redes Neurais:** Aprende com os ciclos de carga/descarga anteriores para estimar o SoC, com tendência a maior precisão ao longo do tempo. [cite: 2072, 2073]
        - **Espectroscopia de Impedância (EIS):** Um dos mais precisos, mas sua complexidade e custo o tornam pouco usual para a maioria das aplicações de BMS. [cite: 2082, 2087]
        """)

    with tab_soh:
        st.subheader("Estimação do SoH (State of Health)")
        st.markdown("Indica a capacidade atual de uma bateria em comparação com sua capacidade nominal quando nova. [cite: 2106] [cite_start]Um SoH de 100% significa que a bateria não teve perda de capacidade. [cite: 2107] [cite_start]Ajuda a prever a vida útil restante. [cite: 2108]")
        st.markdown("**Principais Métodos de Estimação:**")
        st.markdown("""
        - **Comparação de Capacidade:** Compara a capacidade máxima atual (obtida com um ciclo completo) com a capacidade original. [cite: 2118, 2119]
        - **Estimativa Baseada em Modelo:** Usa modelos matemáticos que representam o comportamento da bateria e os ajusta com dados reais. [cite: 2120]
        - **Aprendizado de Máquina:** Utiliza algoritmos (como SVM ou Redes Neurais) para prever o SoH a partir de dados históricos. [cite: 2131]
        - **Medição de Impedância:** O SoH é determinado medindo a impedância interna da bateria, que aumenta com o envelhecimento. [cite: 2132]
        """)

    with tab_sop:
        st.subheader("Estimação do SoP (State of Power)")
        st.markdown("Indica a capacidade da bateria de fornecer ou absorver uma determinada quantidade de energia em um instante. [cite: 2143] [cite_start]É crucial para o gerenciamento de energia em aplicações com rápidas variações de potência, como veículos elétricos e BESS. [cite: 2156]")
        st.markdown("A equação para o SoP é definida como:")
        st.latex(r'''
        SoP(t) = \frac{P_{max}(t)}{P_{nominal}(t)} \times 100 \ [\%] 
        ''')
        st.caption("Onde $P_{max}(t)$ é a potência de pico e $P_{nominal}(t)$ é a potência nominal. [cite: 2147]")