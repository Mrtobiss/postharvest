import streamlit as st
import pandas as pd
import altair as alt

# --- Crop Risk Rules (DSS Decision Engine) ---
storage_risk_rules = {
    "tomato": {
        "open shed": ("High", "Tomatoes degrade fast in open-air storage.", "Use evaporative cooling or cold storage."),
        "sack": ("High", "Sacks retain heat/moisture, accelerating spoilage.", "Use ventilated crates."),
        "evap. cooler": ("Medium", "Reduces temperature but needs maintenance.", "Ensure water supply."),
        "cold room": ("Low", "Preserves freshness effectively.", None),
    },
    "cassava": {
        "open shed": ("High", "Ferments within 2-3 days if not cooled.", "Process quickly or use evaporative cooling."),
        "sack": ("High", "Speeds up fermentation.", "Use ventilated containers."),
        "cold room": ("Low", "Slows microbial action.", None),
    },
    "yam": {
        "open shed": ("Medium", "Can sprout or rot in moist environments.", "Store on raised wooden racks."),
        "sack": ("Medium", "Risk of bruising and airflow restriction.", "Use ventilated stacks."),
        "warehouse": ("Low", "Lasts several weeks when properly stored.", None),
    }
}

# --- Risk Assessment (DSS Core Function) ---
def assess_risk(crop_type, storage_method):
    try:
        risk, justification, recommendation = storage_risk_rules[crop_type][storage_method]
    except KeyError:
        risk, justification, recommendation = "Unknown", "No data for this combination.", "Consult an agricultural expert."
    
    return {
        "Crop": crop_type.capitalize(),
        "Storage": storage_method,  # Changed from 'Storage Method' to 'Storage'
        "Risk Level": risk,
        "Why?": justification,
        "Recommendation": recommendation or "No additional action needed."
    }

# --- Streamlit UI (DSS Interface) ---
st.set_page_config(page_title="AgriGuard DSS", layout="centered")
st.title("🌱 AgriGuard: Post-Harvest Decision Support")
st.markdown("*Data-driven storage advice for Nigerian youth agripreneurs*")

# --- User Inputs (DSS Data Input Layer) ---
col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("Select Crop", list(storage_risk_rules.keys()))
with col2:
    storage = st.selectbox("Storage Method", list(storage_risk_rules[crop].keys()))

# --- DSS Output ---
if st.button("Get Recommendation"):
    result = assess_risk(crop, storage)
    
    # Color-coded risk display
    risk_color = {"High": "red", "Medium": "orange", "Low": "green"}.get(result["Risk Level"], "gray")
    st.markdown(f"""
    ### 📊 Decision Support Output
    **{result['Crop']}** stored in **{result['Storage']}**:  <!-- Fixed key here -->
    <span style='color:{risk_color}; font-weight:bold'>{result['Risk Level']} Risk</span>  
    *{result['Why?']}*  
    **Action:** {result['Recommendation']}
    """, unsafe_allow_html=True)

# ... [Rest of the code remains identical]