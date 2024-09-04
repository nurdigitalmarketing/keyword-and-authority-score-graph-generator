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
    
    # Mostra l'editor interattivo del DataFrame per modifiche dinamiche
    df = st.data_editor(df)

    # Dropdown per selezionare il cliente e i competitor dalle colonne del CSV
    cliente = st.selectbox("Seleziona il cliente", df.columns[1:], index=0)
    
    # Selezione dei competitor con checkbox per includere o escludere
    st.write("Seleziona i competitor da includere:")
    competitor_1 = st.checkbox(df.columns[2], value=True)
    competitor_2 = st.checkbox(df.columns[3], value=True)
    competitor_3 = st.checkbox(df.columns[4], value=True)
    
    # Prepara la lista dei competitor selezionati
    selected_competitors = []
    if competitor_1:
        selected_competitors.append(df.columns[2])
    if competitor_2:
        selected_competitors.append(df.columns[3])
    if competitor_3:
        selected_competitors.append(df.columns[4])

    # Definisci i colori
    colors = {
        cliente: '#2BB3FF',
        df.columns[2]: '#59DDAA',
        df.columns[3]: '#FF8D43',
        df.columns[4]: '#AB6CFE'
    }

    # Prepara i dati per il grafico, includendo solo il cliente e i competitor selezionati
    df.set_index(df.columns[0], inplace=True)
    df_clean = df[[cliente] + selected_competitors].dropna()

    # Calcolo della variazione percentuale
    percentage_change = df_clean.pct_change() * 100

    # Definizione delle dimensioni del grafico in base alla metrica selezionata
    if metrica == "Authority Score":
        plt.figure(figsize=(18, 8))  # Dimensione normale per Authority Score
        plt.title("Andamento dell'Authority Score", fontsize=16)
        plt.ylim(0, 100)  # L'Authority Score è tipicamente tra 0 e 100
        plt.ylabel('Authority Score', fontsize=14)
    else:
        plt.figure(figsize=(8, 6))  # Riduce la larghezza e l'altezza per le Keyword
        plt.title("Andamento del Numero di Keyword Posizionate", fontsize=16)
        plt.ylim(0, df_clean.max().max() * 1.1)  # Imposta un limite superiore dinamico per le keyword
        plt.ylabel('Numero di Keyword Posizionate', fontsize=14)

    # Plot delle linee per ciascuna azienda con i pallini sui punti
    for column in df_clean.columns:
        plt.plot(df_clean.index, df_clean[column], label=column, color=colors[column], 
                 linewidth=3 if column == cliente else 2, alpha=1 if column == cliente else 0.6,
                 marker='o', markersize=8)  # Aggiungi marker per i pallini

        # Annotazioni con la variazione percentuale (con maggiore visibilità)
        for i in range(1, len(df_clean)):
            # Modifica la dimensione del font, aggiungi uno sfondo e un bordo per maggiore leggibilità
            plt.text(df_clean.index[i], df_clean[column].iloc[i], f"{percentage_change[column].iloc[i]:.1f}%", 
                     fontsize=12, ha='center', va='bottom', color=colors[column],
                     bbox=dict(facecolor='white', edgecolor=colors[column], boxstyle='round,pad=0.3'))

    # Personalizzazione dell'asse X
    plt.xlabel('Quarter', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Visualizza il grafico
    st.pyplot(plt)
