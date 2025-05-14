import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure the page
st.set_page_config(
    page_title="Post-Harvest DSS",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Crop Sensitivity ---
crop_sensitivity = {
    "tomato": "High",
    "cassava": "High",
    "yam": "Medium",
    "plantain": "High",
    "onion": "Low",
    "maize": "Medium"
}

# --- Region to Season Mapping ---
region_season = {
    "north": "Dry",
    "south": "Wet",
    "middle-belt": "Transition"
}

# --- Storage Risk Rules ---
storage_risk_rules = {
    "tomato": {
        "open shed":     ("High", "Tomatoes are highly perishable and degrade fast in open-air storage.", "Use evaporative cooling or cold storage."),
        "sack":          ("High", "Sacks retain heat and moisture, accelerating spoilage for tomatoes.", "Use ventilated crates or shaded baskets."),
        "evap. cooler":  ("Medium", "Evaporative coolers reduce temperature but need constant water and shade.", "Ensure cooler is well-maintained."),
        "cold room":     ("Low", "Cold storage preserves tomato freshness and extends shelf life.", None),
    },
    "cassava": {
        "open shed":     ("High", "Cassava ferments within 2-3 days if not processed or cooled.", "Process quickly or use evaporative cooling."),
        "sack":          ("High", "Sacks speed up fermentation and limit airflow.", "Use ventilated containers or immediate processing."),
        "evap. cooler":  ("Medium", "Slows fermentation but doesn't stop it.", "Process as soon as possible."),
        "cold room":     ("Low", "Cold slows microbial action and keeps cassava usable longer.", None),
    },
    "yam": {
        "open shed":     ("Medium", "Yam is less sensitive but can sprout or rot in moist environments.", "Store on raised wooden racks."),
        "sack":          ("Medium", "Risk of physical bruising and airflow restriction.", "Use ventilated stacks."),
        "warehouse (well-ventilated)": ("Low", "Properly stored yam in ventilated warehouse lasts several weeks.", None),
    },
    "plantain": {
        "open shed":     ("High", "Ripens fast in heat and becomes mushy.", "Use cool ventilated area."),
        "sack":          ("High", "Promotes heat and bruising.", "Use shallow trays or hanging bunches."),
        "evap. cooler":  ("Medium", "Slows ripening but needs constant monitoring.", None),
        "cold room":     ("Low", "Best option to delay ripening significantly.", None),
    },
    "onion": {
        "open shed":     ("Medium", "Dry onion stores well in open shade but needs airflow.", "Hang in mesh bags."),
        "sack":          ("Medium", "Can trap moisture if not stored dry.", "Ensure proper ventilation."),
        "warehouse (well-ventilated)": ("Low", "Ideal for storing dry onions.", None),
    },
    "maize": {
        "open shed":     ("Medium", "Shelled maize risks mold if humidity is high.", "Ensure dry conditions."),
        "sack":          ("High", "Sacks retain moisture if maize is not well dried.", "Use hermetic bags."),
        "warehouse (well-ventilated)": ("Low", "Dry maize stores well in ventilated space.", None),
    }
}

# --- Risk Assessment Function ---
def assess_storage_risk(crop_type, storage_method, region=None):
    """
    Assesses the storage risk for a given crop and storage method.
    """
    season = region_season.get(region.lower(), "Dry") if region else "Dry"
    try:
        risk, justification, recommendation = storage_risk_rules[crop_type][storage_method]
    except KeyError:
        risk = "Unknown"
        justification = "No data available for this combination."
        recommendation = "Consider using cold storage or consult an extension agent."

    return {
        "Crop": crop_type.capitalize(),
        "Storage Method": storage_method,
        "Season (based on region)": season if region else "N/A",
        "Risk Level": risk,
        "Justification": justification,
        "Recommendation": recommendation or "No additional recommendation."
    }

# App header with custom styling
st.markdown("""
    <h1 style='text-align: center; color: #2E7D32;'>
        🌾 Decision Support System (DSS) for Reducing Post-Harvest Losses
    </h1>
""", unsafe_allow_html=True)

st.markdown("---")

# Sample test inputs for demonstration
test_inputs = [
    ("tomato", "sack"),
    ("cassava", "open shed"),
    ("yam", "warehouse (well-ventilated)"),
    ("plantain", "evap. cooler"),
    ("onion", "sack"),
    ("maize", "warehouse (well-ventilated)")
]

# Process all test inputs
results = []
for crop, storage in test_inputs:
    result = assess_storage_risk(crop, storage)
    results.append(result)

# Create DataFrame from results
df_results = pd.DataFrame(results)

# Display the DataFrame with results
st.subheader("📊 Assessment Results:")
st.dataframe(df_results, use_container_width=True)

# Create two columns for Risk visualization
col1, col2 = st.columns([3, 2])

with col1:
    # Risk level distribution chart
    risk_counts = df_results['Risk Level'].value_counts().reset_index()
    risk_counts.columns = ['Risk Level', 'Count']
    
    # Create a bar chart
    st.subheader("Risk Level Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Define color mapping and order
    colors = {"High": "red", "Medium": "orange", "Low": "green"}
    risk_order = ["High", "Medium", "Low"]
    
    # Filter and sort data
    plot_data = pd.DataFrame()
    for risk in risk_order:
        if risk in risk_counts['Risk Level'].values:
            plot_data = pd.concat([plot_data, risk_counts[risk_counts['Risk Level'] == risk]])
    
    # Create bar plot with custom colors
    bars = sns.barplot(x='Risk Level', y='Count', data=plot_data, ax=ax, 
                      order=risk_order, palette=colors)
    
    # Add counts on top of bars
    for i, bar in enumerate(bars.patches):
        bars.text(bar.get_x() + bar.get_width()/2, 
                 bar.get_height() + 0.1, 
                 str(int(bar.get_height())), 
                 ha='center')
    
    plt.title('Risk Level Distribution for Sample Crop Storage Methods')
    plt.xlabel('Risk Level')
    plt.ylabel('Count')
    plt.tight_layout()
    
    # Show the plot in Streamlit
    st.pyplot(fig)

with col2:
    # Display summary statistics
    st.subheader("Summary Statistics")
    total_assessments = len(df_results)
    high_risk = len(df_results[df_results['Risk Level'] == 'High'])
    medium_risk = len(df_results[df_results['Risk Level'] == 'Medium'])
    low_risk = len(df_results[df_results['Risk Level'] == 'Low'])
    
    # Create metrics with colorful indicators
    st.metric("Total Assessments", total_assessments)
    st.metric("High Risk Storage Methods", high_risk, 
              delta=f"{high_risk/total_assessments:.1%}", 
              delta_color="inverse")
    st.metric("Medium Risk Storage Methods", medium_risk, 
              delta=f"{medium_risk/total_assessments:.1%}", 
              delta_color="inverse")
    st.metric("Low Risk Storage Methods", low_risk, 
              delta=f"{low_risk/total_assessments:.1%}")

# Footer
st.markdown("---")
st.caption("This Decision Support System helps farmers and stakeholders assess storage risks and make informed decisions to reduce post-harvest losses.")