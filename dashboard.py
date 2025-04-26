import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Employee Dashboard", layout="wide")

st.title("📋 Employee Performance Dashboard")

# Upload do arquivo
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.header("📊 Informações do Dataset")
    st.write(f"**Shape:** {df.shape[0]} linhas e {df.shape[1]} colunas")

    st.subheader("Exemplo de dados")
    st.dataframe(df.head())

    st.subheader("Descrição estatística")
    st.dataframe(df.describe())

    st.subheader("Info detalhada do dataframe")
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Sidebar - selecao de grafico
    st.sidebar.header("Escolha o gráfico")
    option = st.sidebar.selectbox("Selecionar:", (
        "Performance Média por Departamento",
        "Horas de Treinamento Médias por Departamento",
        "Salário Médio por Departamento",
        "Quantidade de Funcionários por Departamento"
    ))

    st.header(f"🌍 {option}")

    if option == "Performance Média por Departamento":
        df_plot = df.groupby("Department")["Performance_Score"].mean().sort_values(ascending=False)
        ylabel = "Média de Score de Performance"
        title = "Média de Performance por Departamento"
    elif option == "Horas de Treinamento Médias por Departamento":
        df_plot = df.groupby("Department")["Training_Hours"].mean().sort_values(ascending=False)
        ylabel = "Média de Horas de Treinamento"
        title = "Média de Horas de Treinamento por Departamento"
    elif option == "Salário Médio por Departamento":
        df_plot = df.groupby("Department")["Salary"].mean().sort_values(ascending=False)
        ylabel = "Média Salarial (R$)"
        title = "Média Salarial por Departamento"
    elif option == "Quantidade de Funcionários por Departamento":
        df_plot = df.groupby("Department")["Employee_ID"].nunique().sort_values(ascending=False)
        ylabel = "Quantidade de Funcionários"
        title = "Quantidade de Funcionários por Departamento"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_plot.index, df_plot.values, color='skyblue')
    ax.set_title(title)
    ax.set_xlabel("Departamento")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

else:
    st.info("Por favor, envie um arquivo CSV para iniciar.")