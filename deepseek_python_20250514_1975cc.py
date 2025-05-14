import streamlit as st
import pandas as pd
import altair as alt

# --- DSS Knowledge Base ---
CROP_RULES = {
    "maize": {
        "open sack": ("High", "Prone to mold in humidity", "Use hermetic bags"),
        "crib": ("Medium", "Rodent/pest exposure", "Treat with neem powder"),
        "silo": ("Low", "Controlled conditions", "Monitor moisture levels")
    },
    "onion": {
        "open field": ("High", "Sunscald and sprouting", "Cure before storage"),
        "mesh bags": ("Medium", "Limited airflow", "Hang in ventilated shed"),
        "cold room": ("Low", "Dormancy preservation", "Maintain 0-4°C")
    },
    "plantain": {
        "bunch hanging": ("Medium", "Even ripening", "Harvest at 75% maturity"),
        "cardboard box": ("High", "Bruising and compression", "Use separators"),
        "ripening room": ("Low", "Ethylene control", "Monitor daily")
    },
    "yam": {
        "barn": ("Medium", "Sprouting after 3 months", "Treat with wood ash"),
        "pit": ("High", "Rot in rainy season", "Line with straw"),
        "cold storage": ("Low", "12-month shelf life", "Maintain 12°C")
    },
    "cassava": {
        "open pile": ("High", "48-hour spoilage window", "Process immediately"),
        "trench": ("Medium", "Partial protection", "Cover with moist soil"),
        "processed": ("Low", "Stable shelf life", "Package when fully dry")
    },
    "tomato": {
        "open basket": ("High", "Bruising and decay", "Use plastic crates"),
        "shaded shed": ("Medium", "Limited shelf life", "Sell within 2 days"),
        "cold chain": ("Low", "14-day freshness", "Pre-cool before storage")
    }
}

# --- DSS Core Function ---
def get_recommendation(crop, method):
    try:
        return CROP_RULES[crop][method]
    except KeyError:
        return ("Unknown", "No data for this combination", "Consult agricultural officer")

# --- DSS Interface ---
st.set_page_config(page_title="FarmDSS", layout="centered")
st.title("🌾 FarmDSS: Post-Harvest Advisor")
st.markdown("**Data-driven decisions for Nigerian crops**")

# Inputs
col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("SELECT CROP", options=list(CROP_RULES.keys()))
with col2:
    method = st.selectbox("STORAGE METHOD", options=list(CROP_RULES[crop].keys()))

# Analysis
if st.button("GET RECOMMENDATION"):
    risk, reason, action = get_recommendation(crop, method)
    
    # Risk Display
    risk_color = {"High": "red", "Medium": "orange", "Low": "green"}.get(risk, "gray")
    st.markdown(f"""
    ### 📋 DSS Report
    **Crop**: {crop.capitalize()}  
    **Storage**: {method}  
    **Risk**: <span style='color:{risk_color}; font-weight:bold'>{risk}</span>  
    **Reason**: {reason}  
    **Action**: {action}
    """, unsafe_allow_html=True)
    
    # Economic Impact
    st.markdown("""
    ### 💰 Economic Impact
    | Scenario | Loss Rate | Profit per Ton |
    |----------|-----------|----------------|
    | Current  | 30-50%    | ₦150,000       |
    | Improved | 10-20%    | ₦250,000       |
    """)
    
    # Risk Comparison Chart
    chart_data = []
    for c in CROP_RULES:
        if method in CROP_RULES[c]:
            r, _, _ = CROP_RULES[c][method]
            chart_data.append({"Crop": c.capitalize(), "Risk": r})
    
    st.altair_chart(alt.Chart(pd.DataFrame(chart_data)).mark_bar().encode(
        x=alt.X("Crop:N", title="", sort="-y"),
        y=alt.X("Risk:N", title="Risk Level"),
        color=alt.Color("Risk:N", scale=alt.Scale(
            domain=["Low", "Medium", "High"],
            range=["green", "orange", "red"]
        ))
    ), use_container_width=True)

# Footer
st.markdown("---")
st.caption("""
**Competition Submission** | Data: FMARD, FAO  
Team: [YOUR TEAM NAME] | Streamlit App
""")
