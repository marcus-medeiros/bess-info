import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu


def peak_shaving_app():
    """
    Cria a página de simulação de Peak Shaving no Streamlit.
    """
    st.header("Simulação de Aplicação: Peak Shaving")
    st.markdown("""
    O **Peak Shaving** (redução de picos de demanda) é uma das principais aplicações de um BESS. O objetivo é utilizar a energia armazenada nas baterias para alimentar as cargas durante os horários em que a demanda de energia da rede elétrica atinge seu pico, geralmente entre **18:00 e 21:00**.
    
    Isso reduz os custos com tarifas de demanda e alivia a sobrecarga na rede elétrica.
    
    O gráfico abaixo simula este cenário:
    - **Azul (Rede):** Potência fornecida pela rede elétrica.
    - **Vermelho (BESS):** Potência fornecida pelo BESS.
    
    Observe como a potência da rede é "achatada" durante o horário de pico, enquanto o BESS assume a responsabilidade.
    """)

    # --- 1. GERAÇÃO DE DADOS PARA A SIMULAÇÃO ---
    horas = list(range(24))
    
    # Demanda de carga típica ao longo do dia, com um pico acentuado à noite
    demanda_total = [
        80, 75, 70, 65, 68, 80, 100, 110, 120, 130, 135, 140, 
        138, 142, 150, 160, 180, 250, 255, 252, 248, 180, 150, 110
    ]
    
    # Listas para armazenar os resultados da simulação
    potencia_bess = []
    potencia_rede = []
    
    potencia_pico_bess = 150 # Potência máxima que o BESS vai fornecer no pico (MW)

    for hora, demanda in zip(horas, demanda_total):
        # Horário de pico (18:00 às 21:00) -> BESS descarrega
        if 18 <= hora <= 21:
            bess_fornece = min(demanda, potencia_pico_bess)
            potencia_bess.append(bess_fornece)
            potencia_rede.append(demanda - bess_fornece)
        # Horário de carga (madrugada, 00:00 às 04:00) -> BESS carrega
        elif 0 <= hora <= 4:
            potencia_bess.append(-50) # Carregando com 50 MW (valor negativo)
            potencia_rede.append(demanda - (-50)) # Rede atende a demanda + carga do BESS
        # Demais horários -> BESS fica em espera
        else:
            potencia_bess.append(0)
            potencia_rede.append(demanda)

    # Criando o DataFrame com os dados da simulação
    df_simulacao = pd.DataFrame({
        'Hora': horas,
        'Demanda Total (MW)': demanda_total,
        'Potência da Rede (MW)': potencia_rede,
        'Potência do BESS (MW)': potencia_bess
    })
    
    # --- 2. PREPARAÇÃO DOS DADOS PARA O GRÁFICO ---
    
    # Para o gráfico de área empilhada, usamos o método "melt" do Pandas.
    # Isso transforma as colunas de potência em uma única coluna de "Fonte" e uma de "Valor".
    df_plot = df_simulacao.melt(
        id_vars='Hora', 
        value_vars=['Potência da Rede (MW)', 'Potência do BESS (MW)'],
        var_name='Fonte de Potência', 
        value_name='Potência (MW)'
    )
    
    # Removemos os valores negativos (carga do BESS) para não exibi-los no gráfico de FORNECIMENTO.
    # A função clip garante que qualquer valor abaixo de 0 se torne 0.
    df_plot['Potência (MW)'] = df_plot['Potência (MW)'].clip(lower=0)

    # --- 3. CRIAÇÃO E EXIBIÇÃO DO GRÁFICO ---
    
    # Usamos Plotly Express para criar o gráfico de área
    fig = px.area(
        df_plot, 
        x='Hora', 
        y='Potência (MW)', 
        color='Fonte de Potência',
        title='Peak Shaving: Fornecimento de Potência (Rede vs. BESS)',
        labels={'Hora': 'Hora do Dia', 'Potência (MW)': 'Potência Fornecida (MW)'},
        color_discrete_map={
            'Potência da Rede (MW)': 'royalblue',
            'Potência do BESS (MW)': 'firebrick'
        }
    )
    
    # Ajustes finos no layout do gráfico
    fig.update_layout(
        title_x=0.2,
        xaxis=dict(tickmode='linear', dtick=2, title_text='Hora do Dia'),
        yaxis_title="Potência (MW)",
        legend_title_text='Fonte de Energia'
    )
    
    st.plotly_chart(fig, use_container_width=True)



def bms():
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


def introducao_armazenamento():
    # --- PÁGINA: INTRODUÇÃO AO ARMAZENAMENTO DE ENERGIA ---
    st.header("Tecnologias de Armazenamento de Energia")
    st.markdown("Esta seção aborda os conceitos fundamentais e as diversas tecnologias utilizadas para armazenar energia, um componente crucial para a estabilidade e eficiência das redes elétricas modernas.")

    # --- CONCEITOS FUNDAMENTAIS ---
    st.subheader("Conceitos Fundamentais")
    st.info("""
    - **Conceito:** Armazenamento de energia é a captura de energia em um dado momento para uso posterior.
    - **Objetivo Principal:** Manter o equilíbrio entre a demanda e a produção de energia.
    - **Acumulador:** É o dispositivo que efetivamente captura e mantém a energia.
    - **Fontes Primárias de Energia:** Radiação, química, potencial e cinética.
    """)

    st.markdown("A necessidade de armazenamento é evidenciada pela variabilidade da geração de fontes renováveis (como solar e eólica) e pelas flutuações do consumo ao longo do dia.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Evolução no Brasil**")
        st.write("Gráficos históricos demonstram períodos de baixa nos reservatórios, ressaltando a importância de novas formas de armazenamento para a segurança energética.")
        st.image("img/9int.png", caption="Gráfico da Evolução da energia armazenada no Brasil", width = 400)
    with col2:
        st.markdown("**Comportamento da Geração Diária**")
        st.write("A análise da geração diária mostra a intermitência de fontes como a solar, que produz apenas durante o dia, e a necessidade de outras fontes para suprir a demanda noturna.")
        st.image("img/10int.png", caption="Gráfico do Comportamento da geração diária de energia no Brasil", width = 400)

    # --- MERCADO GLOBAL ---
    st.subheader("Mercado Global de Armazenamento")
    st.markdown("""
    O mercado de armazenamento de energia está em franca expansão.
    - **Crescimento:** Previsão de adicionar 175,4 GWh em 2024 e atingir 221,9 GWh em 2025, um crescimento de 26,5%.
    - **Principais Mercados:** China, Américas e Europa concentram 90% da capacidade adicionada.
    - **Principais Integradores de Sistemas CA:** Empresas como Tesla, Sungrow e Fluence lideram o mercado.
    """)
    st.markdown("`[TABELA: Tabela dos Principais Fabricantes de Sistemas CA (BESS integrators) - Página 12]`")
    st.image("img/12int.png", caption="Tabela dos Principais Fabricantes de Sistemas CA (BESS integrators)", width = 500)


    # --- CLASSIFICAÇÃO DAS TECNOLOGIAS ---
    st.header("Classificação das Tecnologias de Armazenamento")
    st.markdown("As tecnologias de armazenamento de energia podem ser divididas em quatro classes principais, cada uma com diferentes subcategorias e princípios de funcionamento.")
    st.image("img/13int.png", caption="Diagrama das Classes de sistemas de armazenamento de energia", width = 500)
    

    # --- ARMAZENAMENTO MECÂNICO ---
    st.subheader("1. Armazenamento Mecânico")
    st.markdown("Esta classe armazena energia na forma de energia potencial ou cinética.")

    with st.expander("Usinas Hidrelétricas Reversíveis (UHER)", expanded=True):
        st.markdown("""
        As UHERs, também conhecidas como PHS (Pumped Hydro Storage), são uma das tecnologias mais maduras para armazenamento em larga escala (>100 MW). Elas representam a grande maioria da capacidade de armazenamento instalada no mundo.
        - **Princípio:** Utiliza dois reservatórios em diferentes altitudes. Em períodos de baixa demanda (e energia barata), a água é bombeada do reservatório inferior para o superior. Em períodos de alta demanda, a água é liberada para o reservatório inferior, passando por turbinas e gerando eletricidade.
        - **Vantagens:** Elevada capacidade de armazenamento (única tecnologia capaz de prover mais de 10 GWh em um mesmo local) e custo-benefício atrativo.
        - **Desvantagens:** Necessidade de grandes obras civis e potencial impacto ambiental.
        - **Eficiência Típica:** Em torno de 77-86%.

        """)
        st.image("img/49int.png", caption="Diagrama de perdas e eficiência típica de uma UHER", width = 500)
        st.markdown("#### Classificação e Arranjos")
        st.markdown("""
        - **Quanto ao Circuito:**
            - **Circuito Aberto:** Um ou ambos os reservatórios estão conectados a um curso de água natural.
            - **Circuito Fechado (Puro):** Os reservatórios são isolados de qualquer sistema fluvial.
        - **Quanto aos Arranjos de Máquinas:**
            - **Conjunto Binário:** O mais comum e de menor custo. Usa uma única turbo-bomba reversível que gira em um sentido para gerar e no sentido oposto para bombear.
            - **Conjunto Ternário:** Usa um motor/gerador, uma turbina e uma bomba em um único eixo. Permite transições mais rápidas e maior eficiência, mas tem custo mais elevado.
            - **Conjunto Quaternário:** Possui unidades de geração e bombeamento totalmente separadas e independentes, oferecendo máxima eficiência e flexibilidade, mas com o maior custo.
        """)
        st.markdown("#### Produtos e Serviços Oferecidos")
        st.markdown("""
        - **Nivelamento de Carga (Arbitragem):** Comprar energia barata para armazenar e vender na alta.
        - **Provimento de Inércia:** Ajuda a estabilizar a frequência da rede.
        - **Reserva de Potência e Controle de Frequência:** Atua rapidamente para corrigir desequilíbrios entre geração e carga.
        - **Autorrestabelecimento (Black-start):** Capacidade de religar uma parte da rede após um apagão.
        - **Redução de Congestionamento na Rede:** Otimiza o uso das linhas de transmissão.
        """)
        st.markdown("`[GRÁFICOS: Gráficos da capacidade instalada de UHER no mundo - Páginas 50, 51, 52]`")


    with st.expander("Armazenamento por Ar Comprimido (CAES)", expanded=True):
        st.markdown("""
        O CAES (Compressed Air Energy Storage) armazena energia na forma de energia potencial elástica em ar comprimido, geralmente em cavernas subterrâneas.
        - **Princípio:** Usa eletricidade para comprimir o ar e armazená-lo. Para gerar energia, o ar é liberado, aquecido e expandido através de uma turbina.
        """)
        st.image("img/17int.png", caption="Ilustração de um sistema CAES com armazenamento em caverna de sal", width = 500)

        st.markdown("#### Tipos de CAES")
        col1_caes, col2_caes, col3_caes = st.columns(3)
        with col1_caes:
            st.info("CAES Diabático (D-CAES)")
            st.markdown("""
            - O calor gerado durante a compressão é dissipado (perdido) para o ambiente.
            - Na geração, é necessário queimar um combustível (gás natural) para aquecer o ar antes da expansão.
            - **Vantagens:** Tecnologia comprovada (plantas de Huntorf e McIntosh).
            - **Desvantagens:** Dependência de combustível fóssil, restrições geológicas e menor eficiência (42-54%).
            """)
        with col2_caes:
            st.info("CAES Adiabático (A-CAES)")
            st.markdown("""
            - O calor da compressão é capturado e armazenado em um reservatório térmico (TES).
            - Esse calor armazenado é usado para reaquecer o ar durante a expansão, sem a necessidade de combustível externo.
            - **Vantagens:** Ambientalmente amigável, maior eficiência potencial (até 75%).
            - **Desvantagens:** Desafios técnicos com altas temperaturas (até 600°C) e pressões.
            """)
        with col3_caes:
            st.info("CAES Isotérmico (I-CAES)")
            st.markdown("""
            - Busca manter a temperatura do ar constante durante a compressão e expansão, trocando calor continuamente com o ambiente.
            - **Vantagens:** Eficiência teórica muito alta (próxima de 100%), pois minimiza perdas termodinâmicas.
            - **Desvantagens:** Requer trocadores de calor muito eficientes ou técnicas avançadas (como spray de líquido), sendo uma tecnologia ainda em desenvolvimento.
            """)
        st.markdown("`[TABELA: Tabela de vantagens e desvantagens dos sistemas CAES - Página 45]`")

    with st.expander("Volantes de Inércia (Flywheel)"):
        st.markdown("""
        Armazenam energia na forma de energia cinética rotacional.
        - **Princípio:** Um motor elétrico acelera um rotor massivo (volante) a altas velocidades, armazenando energia. Para descarregar, o rotor aciona o mesmo motor, que agora atua como gerador.
        - **Componentes:** Rotor, Motor/Gerador, Mancais (mecânicos ou magnéticos), Eletrônica de Potência e Carcaça (geralmente a vácuo para reduzir o atrito).
        - **Características:**
            - **Alta Eficiência:** 80-90%.
            - **Longa Vida Útil:** Mais de 100.000 ciclos de carga/descarga.
            - **Resposta Rápida:** Capaz de carregar e descarregar em segundos.
            - **Limitação:** Armazenam energia por períodos curtos (minutos).
        """)

    with st.expander("Bateria Gravitacional"):
        st.markdown("""
        Funciona com base no armazenamento de energia potencial gravitacional, similar a uma UHER, mas usando massas sólidas.
        - **Princípio:** Utiliza eletricidade para erguer blocos pesados. A energia é recuperada ao baixar os blocos de forma controlada, usando a força da gravidade para acionar geradores.
        - **Fornecedores e Métodos:**
            - **Energy Vault:** Usa guindastes para empilhar e desempilhar blocos de 35 toneladas em uma estrutura similar a um prédio.
            - **Gravitricity:** Propõe o uso de pesos suspensos em poços de minas desativados.
            - **ARES (Advanced Rail Energy Storage):** Utiliza vagões ferroviários pesados que são transportados para cima de uma colina para armazenar energia e descem para gerar.
        - **Características:** Longa vida útil (35 anos), eficiência > 80%.
        `[IMAGEM: Ilustração do sistema de bateria gravitacional da Energy Vault - Página 224]`
        """)

    # --- ARMAZENAMENTO ELETROQUÍMICO ---
    st.subheader("2. Armazenamento Eletroquímico")
    st.markdown("Esta classe armazena energia através de reações químicas.")

    with st.expander("Baterias", expanded=True):
        st.markdown("""
        Convertem energia química contida em seus materiais ativos diretamente em energia elétrica através de uma reação eletroquímica.
        - **Componentes básicos da Célula:**
            - **Ânodo (-):** Eletrodo que se oxida (perde elétrons) durante a descarga.
            - **Cátodo (+):** Eletrodo que se reduz (ganha elétrons) durante a descarga.
            - **Eletrólito:** Meio que permite o fluxo de íons (mas não de elétrons) entre o ânodo e o cátodo.
            - **Separador:** Material poroso que isola eletricamente o ânodo do cátodo para evitar curto-circuito, mas permite a passagem dos íons.
        - **Classificação:**
            - **Primárias:** Não recarregáveis.
            - **Secundárias:** Recarregáveis (a reação química é reversível).
        - **Parâmetros Chave:**
            - **Energia Específica (Wh/kg):** Capacidade de armazenamento por massa. Importante para aplicações móveis.
            - **Densidade de Energia (Wh/L):** Capacidade de armazenamento por volume. Importante para aplicações com espaço limitado.
            - **Profundidade de Descarga (DoD):** Percentual da capacidade total que pode ser descarregada.
            - **Tempo de Vida (Ciclos):** Número de ciclos de carga/descarga que a bateria suporta antes de sua capacidade degradar significativamente.
        
        `[IMAGEM: Gráfico comparativo de Energia Específica vs. Densidade de Energia para diferentes tecnologias de bateria - Página 190]`
        """)

        st.markdown("#### Tecnologias de Baterias")
        
        col1_bat, col2_bat = st.columns(2)
        with col1_bat:
            st.info("Chumbo-Ácido")
            st.markdown("""
            - **Vantagens:** Tecnologia madura, robusta e de baixo custo.
            - **Desvantagens:** Baixa densidade de energia, vida útil curta, sensível a descargas profundas (DoD típico de 20%, máximo de 80%).
            - **Avanço:** Baterias de **Chumbo-Carbono** adicionam materiais de carbono aos eletrodos para melhorar as correntes, a densidade e a vida útil.
            """)

            st.info("Baterias de Fluxo (REDOX)")
            st.markdown("""
            - **Princípio:** O eletrólito (que armazena a energia) fica em tanques externos e é bombeado através das células eletroquímicas para gerar energia.
            - **Vantagens:** Potência e energia são independentes e escaláveis, vida útil muito longa (>10.000 ciclos), ideal para armazenamento de longa duração e grande porte.
            - **Desvantagens:** Menor densidade de energia e complexidade do sistema (bombas, tanques).
            `[IMAGEM: Diagrama de funcionamento de uma Bateria de Fluxo - Página 213]`
            """)

        with col2_bat:
            st.info("Íon de Lítio (Li-ion)")
            st.markdown("""
            Tecnologia dominante em BESS e veículos elétricos.
            - **Vantagens:** Alta densidade de energia, maior vida útil em ciclos, baixo coeficiente de autodescarga e excelente custo-benefício.
            - **Desvantagens:** Requer um sistema de gerenciamento (BMS) para garantir a segurança, pois o eletrólito pode ser inflamável.
            - **Químicas Comuns:**
                - **NMC (Níquel Manganês Cobalto):** Bom equilíbrio entre energia, potência e custo. Muito usada em veículos elétricos e BESS.
                - **LFP (Fosfato de Ferro Lítio):** Excelente segurança (estabilidade térmica), vida útil muito longa e menor custo. Tornou-se o padrão para armazenamento estacionário.
                - **LTO (Titanato de Lítio):** Vida útil excepcional (>10.000 ciclos) e segurança, mas com menor densidade de energia.
            - **Futuro:** **Baterias de Estado Sólido**, que substituem o eletrólito líquido por um sólido, prometem maior segurança, durabilidade e densidade de energia.
            """)

    with st.expander("Hidrogênio (H₂) e Células de Combustível"):
        st.markdown("""
        Sistema de armazenamento de longo prazo que envolve dois processos:
        1.  **Eletrólise:** Usa eletricidade (preferencialmente de fontes renováveis, gerando **Hidrogênio Verde**) para separar a água (H₂O) em hidrogênio (H₂) e oxigênio (O₂).
        2.  **Célula de Combustível:** Recombina o hidrogênio armazenado com o oxigênio do ar para produzir eletricidade, com água como único subproduto.
        - **Vantagens:** Elemento abundante, pode ser produzido de forma limpa, alta densidade de energia por massa.
        - **Desvantagens:** Processo de produção ainda caro, desafios no armazenamento (alta pressão ou criogenia) e falta de infraestrutura.
        `[IMAGEM: Diagrama do ciclo completo do Hidrogênio (produção, armazenamento, uso) - Página 156]`
        """)

    # --- OUTRAS TECNOLOGIAS ---
    st.subheader("3. Armazenamento Termodinâmico e Eletromagnético")
    
    col1_outras, col2_outras = st.columns(2)
    with col1_outras:
        with st.container(border=True):
            st.markdown("#### Armazenamento Termodinâmico (Térmico - TES)")
            st.markdown("""
            Armazena energia na forma de calor em um meio líquido ou sólido.
            - **Calor Sensível:** A temperatura do meio (ex: sais fundidos em usinas solares CSP, rochas, água) é alterada para armazenar/liberar energia.
            - **Calor Latente:** Usa a energia absorvida/liberada durante a mudança de fase de um material (PCM - Phase Change Material), como de sólido para líquido.
            - **Termoquímico:** Utiliza reações químicas reversíveis para armazenar energia.
            """)
    with col2_outras:
        with st.container(border=True):
            st.markdown("#### Armazenamento Eletromagnético")
            st.markdown("""
            - **Supercapacitores (Ultracapacitores):** Armazenam energia em um campo elétrico. Possuem capacidade de armazenamento limitada, mas podem carregar/descarregar quase instantaneamente com altíssima potência e suportam milhões de ciclos. Ideais para aplicações de resposta rápida.
            - **Armazenamento Magnético Supercondutor (SMES):** Armazena energia em um campo magnético gerado por uma corrente em uma bobina supercondutora. Apresenta eficiência altíssima e resposta instantânea, mas requer resfriamento criogênico, o que consome energia e eleva o custo.
            """)
            