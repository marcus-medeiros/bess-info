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