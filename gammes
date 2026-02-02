import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================
# CONFIG PAGE
# =====================
st.set_page_config(page_title="Analyse stratégique des gammes", layout="wide")

# =====================
# DONNÉES
# =====================
data = {
    'Gamme': ['Gamme A (Best-Seller)', 'Gamme B (Innovation)', 'Gamme C (Classique)'],
    'CA_Annuel': [554979, 198091, 238721],
    'Marge_Annuelle': [74979, -29909, 106721],
    'Budget_Marketing': [60000, 180000, 12000],
    'Taux_SAV': [0.25, 0.05, 0.02]
}

df = pd.DataFrame(data)
df['ROI'] = df['Marge_Annuelle'] / df['Budget_Marketing']

# =====================
# NAVIGATION
# =====================
slide = st.radio(
    "Navigation",
    ["Décisions stratégiques", "Analyse & justification"],
    horizontal=True
)

# =====================
# SLIDE 1 — DÉCISIONS
# =====================
if slide == "Décisions stratégiques":
    st.title("Décisions stratégiques")

    st.success("✅ **Gamme C (Classique) → INVESTIR / ACCÉLÉRER**")
    st.write("""
    - Marge annuelle la plus élevée  
    - ROI marketing très fort (~9)  
    - Faible budget, faible SAV  
    👉 **Création de valeur maximale**
    """)

    st.warning("⚠️ **Gamme A (Best-Seller) → OPTIMISER**")
    st.write("""
    - Très fort chiffre d’affaires  
    - ROI faible (~1,2)  
    - SAV élevé  
    👉 **Optimisation des coûts et de la qualité**
    """)

    st.error("❌ **Gamme B (Innovation) → ABANDONNER / STOPPER**")
    st.write("""
    - Marge négative  
    - ROI marketing négatif  
    - Budget marketing inefficace  
    👉 **Destruction de valeur**
    """)

# =====================
# SLIDE 2 — ANALYSE
# =====================
else:
    st.title("Analyse économique & marketing")

    fig = px.scatter(
        df,
        x="CA_Annuel",
        y="Marge_Annuelle",
        color="Gamme",
        size="Budget_Marketing",
        hover_data=["ROI", "Taux_SAV"],
        title="Matrice stratégique : CA vs Marge",
        labels={
            "CA_Annuel": "Chiffre d'affaires annuel (€)",
            "Marge_Annuelle": "Marge annuelle (€)"
        }
    )

    fig.add_hline(y=0, line_dash="dash")
    fig.add_vline(x=df["CA_Annuel"].mean(), line_dash="dash")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
### Lecture
- Axe Y > 0 → création de valeur  
- Couleur → gamme  
- Taille → budget marketing  
- ROI élevé = efficacité marketing  

👉 **La Gamme C est la plus performante économiquement**  
👉 **La Gamme B détruit de la valeur**
""")
