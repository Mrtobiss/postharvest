import streamlit as st
import pandas as pd
import altair as alt

# --- Crop Sensitivity & Storage Risk Rules (Unchanged) ---
crop_sensitivity = {
    "tomato": "High",
    "cassava": "High",
    "yam": "Medium",
    "plantain": "High",
    "onion": "Low",
    "maize": "Medium"
}

storage_risk_rules = {
    "tomato": {
        "open shed": ("High", "Tomatoes degrade fast in open-air storage.", "Use evaporative cooling or cold storage."),
        "sack": ("High", "Sacks retain heat/moisture, accelerating spoilage.", "Use ventilated crates."),
        "evap. cooler": ("Medium", "Reduces temperature but needs maintenance.", "Ensure water supply."),
        "cold room": ("Low", "Preserves freshness effectively.", None),
    },
    # ... [Keep all other crop rules unchanged from your original]
}

# --- Risk Assessment Function (Simplified) ---
def assess_risk(crop_type, storage_method):
    try:
        risk, justification, recommendation = storage_risk_rules[crop_type][storage_method]
    except KeyError:
        risk = "Unknown"
        justification = "No data for this combination."
        recommendation = "Consult an agricultural expert."

    return {
        "Crop": crop_type.capitalize(),
        "Storage Method": storage_method,
        "Risk Level": risk,
        "Why?": justification,
        "Recommendation": recommendation or "No additional action needed."
    }

# --- Streamlit UI (Minimalist) ---
st.set_page_config(page_title="PostHarvest Loss Risk Tool", layout="centered")
st.title("🌱 PostHarvest Loss Risk Tool")
st.markdown("*Predict spoilage risk based on storage choices*")

# User inputs (only 2 fields!)
col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("Select Crop", list(storage_risk_rules.keys()))
with col2:
    storage = st.selectbox("Storage Method", list(storage_risk_rules[crop].keys()))

# Calculate and display
if st.button("Calculate Risk"):
    result = assess_risk(crop, storage)
    
    # Color-coded risk display
    risk_color = {
        "High": "red", 
        "Medium": "orange", 
        "Low": "green", 
        "Unknown": "gray"
    }.get(result["Risk Level"], "blue")
    
    st.markdown(f"""
    ### 📊 Results
    **{result['Crop']}** stored in **{result['Storage Method']}**:  
    <span style='color:{risk_color}; font-weight:bold'>{result['Risk Level']} Risk</span>  
    *{result['Why?']}*  
    **Recommendation:** {result['Recommendation']}
    """, unsafe_allow_html=True)

    # Optional visualization
    if st.checkbox("Compare All Crops for This Storage Method"):
        data = []
        for crop_name in storage_risk_rules:
            if storage in storage_risk_rules[crop_name]:
                risk = storage_risk_rules[crop_name][storage][0]
                data.append({"Crop": crop_name.capitalize(), "Risk": risk})
        
        chart = alt.Chart(pd.DataFrame(data)).mark_bar().encode(
            x=alt.X("Crop", sort="-y"),
            y="Risk",
            color=alt.Color("Risk", scale=alt.Scale(
                domain=["Low", "Medium", "High", "Unknown"],
                range=["green", "orange", "red", "gray"]))
        ).properties(title=f"Risk Across Crops for '{storage}'")
        st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.caption("MVP Prototype | Logic mirrors full solution with simplified inputs")