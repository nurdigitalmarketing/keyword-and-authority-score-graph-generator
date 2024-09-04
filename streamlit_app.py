import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Funzione per caricare i dati dal file CSV caricato dall'utente
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

# Titolo dell'app
st.title("Analisi dell'Authority Score o delle Keyword Posizionate")

# Selettore tra "Authority Score" e "Keyword"
metrica = st.selectbox("Seleziona la metrica", ["Authority Score", "Keyword Posizionate"])

# Carica il file CSV
uploaded_file = st.file_uploader("Carica il file CSV con i dati", type=["csv"])

if uploaded_file is not None:
    # Carica i dati dal CSV
    df = load_data(uploaded_file)
    
    st.write("Dati caricati:")
    st.write(df.head())  # Mostra i primi dati caricati
    
    # Dropdown per selezionare il cliente e i competitor dalle colonne del CSV
    cliente = st.selectbox("Seleziona il cliente", df.columns[1:], index=0)
    competitor_1 = st.selectbox("Seleziona il primo competitor", df.columns[1:])
    competitor_2 = st.selectbox("Seleziona il secondo competitor", df.columns[1:])
    competitor_3 = st.selectbox("Seleziona il terzo competitor", df.columns[1:])

    # Definisci i colori
    colors = {
        cliente: '#2BB3FF',
        competitor_1: '#59DDAA',
        competitor_2: '#FF8D43',
        competitor_3: '#AB6CFE'
    }

    # Prepara i dati per il grafico
    df.set_index(df.columns[0], inplace=True)
    df_clean = df[[cliente, competitor_1, competitor_2, competitor_3]].dropna()

    # Calcolo della variazione percentuale
    percentage_change = df_clean.pct_change() * 100

    # Creazione del grafico con Matplotlib
    plt.figure(figsize=(18, 8))

    # Impostazione del titolo e range dell'asse Y in base alla selezione della metrica
    if metrica == "Authority Score":
        plt.title("Andamento dell'Authority Score", fontsize=16)
        plt.ylim(0, 100)  # L'Authority Score è tipicamente tra 0 e 100
        plt.ylabel('Authority Score', fontsize=14)
    else:
        plt.title("Andamento del Numero di Keyword Posizionate", fontsize=16)
        plt.ylim(0, None)  # Le keyword possono andare da 0 a illimitato
        plt.ylabel('Numero di Keyword Posizionate', fontsize=14)

    # Plot delle linee per ciascuna azienda
    for column in df_clean.columns:
        plt.plot(df_clean.index, df_clean[column], label=column, color=colors[column], 
                 linewidth=3 if column == cliente else 2, alpha=1 if column == cliente else 0.6)

        # Annotazioni con la variazione percentuale
        for i in range(1, len(df_clean)):
            plt.text(df_clean.index[i], df_clean[column].iloc[i], f"{percentage_change[column].iloc[i]:.1f}%", 
                     fontsize=10, ha='center', va='bottom', color=colors[column])

    # Personalizzazione dell'asse X
    plt.xlabel('Quarter', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Visualizza il grafico
    st.pyplot(plt)
