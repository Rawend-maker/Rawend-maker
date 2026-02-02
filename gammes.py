import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Analyse stratégique des gammes",
    layout="wide"
)


# =====================
# DONNÉES
# =====================
np.random.seed(42)

data = {
    'Mois': list(range(1, 13)) * 3,
    'Gamme': ['Gamme A (Best-Seller)'] * 12
            + ['Gamme B (Innovation)'] * 12
            + ['Gamme C (Classique)'] * 12,
    'CA_Mensuel': [
        50000, 52000, 48000, 49000, 51000, 47000,
        46000, 45000, 44000, 43000, 42000, 40000
    ] + [
        5000, 6000, 8000, 10000, 12000, 15000,
        18000, 20000, 22000, 25000, 28000, 30000
    ] + [
        20000, 20000, 20500, 19500, 20000, 20000,
        20000, 20100, 19900, 20000, 20000, 20000
    ],
    'Cout_Production': [35000] * 12 + [4000] * 12 + [10000] * 12,
    'Budget_Marketing': [5000] * 12 + [15000] * 12 + [1000] * 12,
    'Taux_Retour_SAV': [0.25] * 12 + [0.05] * 12 + [0.02] * 12
}

df = pd.DataFrame(data)
df['CA_Mensuel'] += np.random.randint(-500, 500, df.shape[0])

# =====================
# KPIs
# =====================
df['Marge'] = df['CA_Mensuel'] - df['Cout_Production'] - df['Budget_Marketing']

df_agg = df.groupby('Gamme').agg(
    CA_Annuel=('CA_Mensuel', 'sum'),
    Marge_Annuelle=('Marge', 'sum'),
    Budget_Marketing=('Budget_Marketing', 'sum'),
    Taux_SAV=('Taux_Retour_SAV', 'mean')
).reset_index()

df_agg['ROI'] = df_agg['Marge_Annuelle'] / df_agg['Budget_Marketing']

# =====================
# NAVIGATION (SLIDES)
# =====================
slide = st.radio(
    "Navigation",
    ["Décisions", "Analyse temporelle", "Marketing & SAV", "Matrice stratégique"],
    horizontal=True
)

# =====================
# SLIDE 1 — DÉCISIONS
# =====================
if slide == "Décisions":
    st.title("Décisions stratégiques")

    st.success("✅ **Gamme C (Classique) → INVESTIR / ACCÉLÉRER**")
    st.write("""
    - Marge annuelle la plus élevée  
    - ROI marketing très fort (~9)  
    - Faible budget, faible SAV  
    👉 Création de valeur maximale
    """)

    st.warning("⚠️ **Gamme A (Best-Seller) → OPTIMISER**")
    st.write("""
    - Très gros CA  
    - ROI faible (~1,2)  
    - SAV élevé  
    👉 Optimisation coûts / qualité / pricing
    """)

    st.error("❌ **Gamme B (Innovation) → ABANDONNER / STOPPER**")
    st.write("""
    - Marge négative  
    - ROI marketing négatif  
    - Budget marketing inefficace  
    👉 Destruction de valeur
    """)

# =====================
# SLIDE 2 — ÉVOLUTION CA
# =====================
elif slide == "Analyse temporelle":
    st.title("Évolution du chiffre d’affaires")

    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(
        data=df,
        x='Mois',
        y='CA_Mensuel',
        hue='Gamme',
        marker='o',
        ax=ax
    )
    ax.set_title("Évolution du CA mensuel par gamme")
    ax.set_xlabel("Mois")
    ax.set_ylabel("CA mensuel (€)")
    ax.set_xticks(range(1,13))

    st.pyplot(fig)

# =====================
# SLIDE 3 — MARKETING & SAV
# =====================
elif slide == "Marketing & SAV":
    st.title("Marketing et qualité")

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(6,5))
        sns.barplot(
            data=df,
            x='Gamme',
            y='Budget_Marketing',
            estimator=sum,
            ax=ax1
        )
        ax1.set_title("Budget marketing total par gamme")
        ax1.set_ylabel("Budget (€)")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6,5))
        sns.barplot(
            data=df,
            x='Gamme',
            y='Taux_Retour_SAV',
            ax=ax2
        )
        ax2.set_title("Taux de retour SAV")
        ax2.set_ylabel("Taux")
        st.pyplot(fig2)

# =====================
# SLIDE 4 — MATRICE STRATÉGIQUE
# =====================
# =====================
# SLIDE 4 — MATRICE STRATÉGIQUE (IDENTIQUE MATPLOTLIB)
# =====================
else:
    st.title("Matrice stratégique : CA vs Marge")

    fig, ax = plt.subplots(figsize=(9,6))

    sc = ax.scatter(
        df_agg['CA_Annuel'],
        df_agg['Marge_Annuelle'],
        c=df_agg['ROI'],                       # ✅ couleur = ROI
        s=df_agg['Budget_Marketing'] / 300,   # ✅ taille = budget
        alpha=0.75,
        cmap='viridis'
    )

    # Seuils
    ax.axhline(0, linestyle='--')
    ax.axvline(df_agg['CA_Annuel'].mean(), linestyle='--')

    # Colorbar
    plt.colorbar(sc, ax=ax, label="ROI marketing")

    # Annotations
    for _, r in df_agg.iterrows():
        ax.annotate(
            r['Gamme'],
            (r['CA_Annuel'], r['Marge_Annuelle']),
            textcoords="offset points",
            xytext=(8, 6),
            ha='left'
        )

    ax.set_title("Matrice stratégique : CA vs Marge (couleur = ROI)")
    ax.set_xlabel("Chiffre d'affaires annuel (€)")
    ax.set_ylabel("Marge annuelle (€)")

    plt.tight_layout()
    st.pyplot(fig)
