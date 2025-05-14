import streamlit as st
import pandas as pd
import altair as alt

# ======================
# DSS KNOWLEDGE BASE
# ======================
CROP_DATA = {
    "maize": {
        "open sack": {"risk": "High", "reason": "Prone to mold in humidity", "action": "Use hermetic bags"},
        "crib": {"risk": "Medium", "reason": "Rodent/pest exposure", "action": "Treat with neem powder"},
        "silo": {"risk": "Low", "reason": "Controlled conditions", "action": "Monitor moisture levels"}
    },
    "onion": {
        "open field": {"risk": "High", "reason": "Sunscald and sprouting", "action": "Cure before storage"},
        "mesh bags": {"risk": "Medium", "reason": "Limited airflow", "action": "Hang in ventilated shed"},
        "cold room": {"risk": "Low", "reason": "Dormancy preservation", "action": "Maintain 0-4°C"}
    },
    "plantain": {
        "bunch hanging": {"risk": "Medium", "reason": "Even ripening", "action": "Harvest at 75% maturity"},
        "cardboard box": {"risk": "High", "reason": "Bruising and compression", "action": "Use separators"},
        "ripening room": {"risk": "Low", "reason": "Ethylene control", "action": "Monitor daily"}
    },
    "yam": {
        "barn": {"risk": "Medium", "reason": "Sprouting after 3 months", "action": "Treat with wood ash"},
        "pit": {"risk": "High", "reason": "Rot in rainy season", "action": "Line with straw"},
        "cold storage": {"risk": "Low", "reason": "12-month shelf life", "action": "Maintain 12°C"}
    },
    "cassava": {
        "open pile": {"risk": "High", "reason": "48-hour spoilage window", "action": "Process immediately"},
        "trench": {"risk": "Medium", "reason": "Partial protection", "action": "Cover with moist soil"},
        "processed": {"risk": "Low", "reason": "Stable shelf life", "action": "Package when fully dry"}
    },
    "tomato": {
        "open basket": {"risk": "High", "reason": "Bruising and decay", "action": "Use plastic crates"},
        "shaded shed": {"risk": "Medium", "reason": "Limited shelf life", "action": "Sell within 2 days"},
        "cold chain": {"risk": "Low", "reason": "14-day freshness", "action": "Pre-cool before storage"}
    }
}

# ======================
# DSS CORE FUNCTION
# ======================
def analyze_risk(crop, method):
    return CROP_DATA.get(crop, {}).get(method, {
        "risk": "Unknown", 
        "reason": "Data unavailable", 
        "action": "Consult extension officer"
    })

# ======================
# DSS INTERFACE
# ======================
st.set_page_config(page_title="FarmGuard DSS", layout="centered")
st.title("🌱 FarmGuard Decision Support System")
st.markdown("**Reduce post-harvest losses for Nigerian crops**")

# Input Section
col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("SELECT CROP", options=list(CROP_DATA.keys()))
with col2:
    method = st.selectbox("STORAGE METHOD", options=list(CROP_DATA[crop].keys()))

# Analysis Section
if st.button("GET DSS RECOMMENDATION"):
    result = analyze_risk(crop, method)
    
    # Risk Display
    risk_color = {"High": "red", "Medium": "orange", "Low": "green"}.get(result["risk"], "gray")
    st.markdown(f"""
    ### 📋 DSS Report: {crop.capitalize()}
    **Risk Level**: <span style='color:{risk_color}; font-weight:bold'>{result["risk"]}</span>  
    **Key Concern**: {result["reason"]}  
    **Recommended Action**: {result["action"]}
    """, unsafe_allow_html=True)
    
    # Economic Impact
    loss_rates = {"High": "35-50%", "Medium": "20-35%", "Low": "5-20%"}
    st.markdown(f"""
    ### 💰 Economic Impact
    - **Current loss range**: {loss_rates[result["risk"]]} of harvest value
    - **Potential savings**: ₦150,000-₦400,000 per ton with proper storage
    """)
    
    # Risk Comparison Chart
    st.altair_chart(alt.Chart(
        pd.DataFrame([{"crop": c, "risk": analyze_risk(c, method)["risk"]} 
                     for c in CROP_DATA if method in CROP_DATA[c]])
    ).mark_bar().encode(
        x=alt.X("crop:N", title="", sort="-y"),
        y=alt.Y("risk:N", title="Risk Level"),
        color=alt.Color("risk:N", scale=alt.Scale(
            domain=["Low", "Medium", "High"],
            range=["green", "orange", "red"]
        ))
    ), use_container_width=True)

# Footer
st.markdown("---")
st.caption("""
**Competition Submission** | Data: FMARD, FAO, NARO  
Team: [YOUR TEAM NAME] | Streamlit App
""")
