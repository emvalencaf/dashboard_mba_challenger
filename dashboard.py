import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="Employee Analytics", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stMetric {background-color: white; border-radius: 10px; padding: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Employee Growth & Performance Dashboard")

uploaded_file = st.sidebar.file_uploader("📁 Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Visão Geral", "🏆 Performance", "💰 Salário", "📅 Admissões", "🧠 Treinamento & Performance", "🎯 Top Talentos"])

    with tab1:
        st.header("📊 Visão Geral do Dataset")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👥 Total de Funcionários", df.shape[0])
        with col2:
            st.metric("💸 Salário Médio (R$)", f"{df['Salary'].mean():,.2f}")
        with col3:
            st.metric("⏳ Horas de Treinamento Média", f"{df['Training_Hours'].mean():.1f} h")

        st.subheader("🔍 Amostra dos Dados")
        st.dataframe(df.head(), use_container_width=True, height=250)

    with tab2:
        st.header("🏆 Performance e Desenvolvimento")
        col4, col5 = st.columns(2)
        with col4:
            perf_dept = df.groupby("Department")["Performance_Score"].mean().sort_values()
            fig, ax = plt.subplots(figsize=(8,5))
            sns.barplot(x=perf_dept.values, y=perf_dept.index, palette="Blues_r", ax=ax)
            ax.set_title("Performance Média por Departamento", fontsize=14, weight='bold')
            ax.set_xlabel("Performance Score Médio")
            ax.set_ylabel("")
            st.pyplot(fig)

        with col5:
            train_dept = df.groupby("Department")["Training_Hours"].mean().sort_values()
            fig, ax = plt.subplots(figsize=(8,5))
            sns.barplot(x=train_dept.values, y=train_dept.index, palette="Purples_r", ax=ax)
            ax.set_title("Horas de Treinamento Médias por Departamento", fontsize=14, weight='bold')
            ax.set_xlabel("Horas")
            ax.set_ylabel("")
            st.pyplot(fig)

    with tab3:
        st.header("💰 Salário por Departamento")
        salary_dept = df.groupby("Department")["Salary"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(x=salary_dept.values, y=salary_dept.index, palette="RdBu", ax=ax)
        ax.set_title("Salário Médio por Departamento", fontsize=14, weight='bold')
        ax.set_xlabel("Salário Médio (R$)")
        ax.set_ylabel("")
        st.pyplot(fig)

    with tab4:
        st.header("📅 Evolução de Admissões")
        df['Date_of_Joining'] = pd.to_datetime(df['Date_of_Joining'])
        df['Ano'] = df['Date_of_Joining'].dt.year
        hires_per_year = df['Ano'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10,5))
        sns.lineplot(x=hires_per_year.index, y=hires_per_year.values, marker='o', color='#636EFA', ax=ax)
        ax.set_title("Contratações por Ano", fontsize=14, weight='bold')
        ax.set_ylabel("Número de Contratações")
        ax.set_xlabel("Ano")
        st.pyplot(fig)

    with tab5:
        st.header("🧠 Treinamento & Performance")
        st.write("Como o investimento em treinamento impacta a performance?")
        fig, ax = plt.subplots(figsize=(8,6))
        sns.scatterplot(data=df, x="Training_Hours", y="Performance_Score", hue="Department", palette="tab10", ax=ax)
        ax.set_title("Relação entre Horas de Treinamento e Performance", fontsize=14, weight='bold')
        ax.set_xlabel("Horas de Treinamento")
        ax.set_ylabel("Score de Performance")
        st.pyplot(fig)

    with tab6:
        st.header("🎯 Top Talentos")
        st.write("Quais são nossos funcionários de alta performance?")

        threshold = st.slider("Selecione a performance mínima para considerar 'Top Talento'", min_value=int(df['Performance_Score'].min()), max_value=int(df['Performance_Score'].max()), value=int(df['Performance_Score'].quantile(0.90)))

        top_performers = df[df['Performance_Score'] >= threshold]

        st.metric("🌟 Número de Top Talentos", top_performers.shape[0])

        st.dataframe(top_performers[['Employee_ID', 'Department', 'Performance_Score', 'Training_Hours', 'Salary']], use_container_width=True)

else:
    st.info("👆 Por favor, envie um arquivo CSV para visualizar o dashboard.")