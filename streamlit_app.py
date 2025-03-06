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

    # Prepara i dati per il grafico
    df.set_index(df.columns[0], inplace=True)
    df_clean = df[[cliente] + selected_competitors].dropna()

    # Calcolo della variazione percentuale
    percentage_change = df_clean.pct_change() * 100

    # Definizione delle dimensioni del grafico
    plt.figure(figsize=(18, 8) if metrica == "Authority Score" else (12, 8))
    plt.title(f"Andamento dell'{'Authority Score' if metrica == 'Authority Score' else 'Numero di Keyword Posizionate'}", fontsize=16)

    # Imposta il limite superiore dell'asse Y con più spazio
    y_max = 100 if metrica == "Authority Score" else df_clean.max().max() * 1.2
    plt.ylim(0, y_max)

    plt.ylabel('Authority Score' if metrica == "Authority Score" else 'Numero di Keyword Posizionate', fontsize=14)

    # Sposta il grafico verso l'alto riducendo il margine superiore
    plt.subplots_adjust(top=0.85)

    # Plot delle linee
    for column in df_clean.columns:
        plt.plot(df_clean.index, df_clean[column], label=column, color=colors[column], 
                 linewidth=3 if column == cliente else 2, alpha=1 if column == cliente else 0.6,
                 marker='o', markersize=8)
        
        # Annotazioni con offset verticale maggiore per evitarne la sovrapposizione
        for i in range(1, len(df_clean)):
            value = df_clean[column].iloc[i]
            pct_change = percentage_change[column].iloc[i]
            offset = 8 if i % 2 == 0 else -8  # Alterna le altezze per evitare sovrapposizione
            plt.text(df_clean.index[i], value + offset, f"{pct_change:.1f}%", 
                     fontsize=12, ha='center', va='bottom', color=colors[column],
                     bbox=dict(facecolor='white', edgecolor=colors[column], boxstyle='round,pad=0.3'))

    # Personalizzazione asse X
    plt.xlabel('Quarter', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Visualizza il grafico
    st.pyplot(plt)
