import streamlit as st
import pandas as pd
import altair as alt

# ======================
# DSS KNOWLEDGE BASE
# ======================
CROP_RISK_RULES = {
    "tomato": {
        "open shed": {
            "risk": "High",
            "reason": "Tomatoes degrade rapidly in open-air conditions",
            "recommendation": "Use evaporative cooling or cold storage"
        },
        "ventilated crate": {
            "risk": "Medium",
            "reason": "Provides airflow but limited temperature control",
            "recommendation": "Keep in shaded area and sell within 3 days"
        },
        "cold storage": {
            "risk": "Low",
            "reason": "Optimal temperature and humidity control",
            "recommendation": "Monitor for condensation buildup"
        }
    },
    "cassava": {
        "open pile": {
            "risk": "High",
            "reason": "Rapid fermentation and mold growth",
            "recommendation": "Process within 48 hours or use sealed storage"
        },
        "ventilated shed": {
            "risk": "Medium",
            "reason": "Reduces but doesn't eliminate fermentation",
            "recommendation": "Turn roots regularly to prevent hotspots"
        },
        "processed flour": {
            "risk": "Low",
            "reason": "Stable shelf life when properly dried",
            "recommendation": "Ensure moisture content <12% before storage"
        }
    }
}

LOGISTICS_OPTIONS = {
    "tomato": ["Direct to market", "Aggregation center", "Cold chain transport"],
    "cassava": ["Farm gate sale", "Processing center", "Industrial buyer"]
}

# ======================
# DSS CORE FUNCTIONS
# ======================
def generate_recommendation(crop, storage_method):
    """Core DSS analysis function"""
    try:
        result = CROP_RISK_RULES[crop][storage_method]
        return {
            "risk_level": result["risk"],
            "risk_reason": result["reason"],
            "action_items": [
                result["recommendation"],
                f"Consider these logistics options: {', '.join(LOGISTICS_OPTIONS[crop])}"
            ]
        }
    except KeyError:
        return {
            "risk_level": "Unknown",
            "risk_reason": "No data available for this combination",
            "action_items": ["Consult agricultural extension officer"]
        }

def calculate_economic_impact(crop, risk_level):
    """DSS financial impact projection"""
    baseline = {
        "tomato": {"high": 0.4, "medium": 0.25, "low": 0.1},
        "cassava": {"high": 0.5, "medium": 0.3, "low": 0.15}
    }
    reduction = {
        "High": 0.1,
        "Medium": 0.25,
        "Low": 0.4
    }
    
    loss_rate = baseline.get(crop, {}).get(risk_level.lower(), 0.3)
    improved_rate = loss_rate * (1 - reduction.get(risk_level, 0.2))
    
    return {
        "current_loss": f"{loss_rate*100:.0f}%",
        "projected_loss": f"{improved_rate*100:.0f}%",
        "value_saved": f"₦{(loss_rate - improved_rate)*50000:,.0f} per ton"
    }

# ======================
# DSS USER INTERFACE
# ======================
st.set_page_config(
    page_title="AgriDecide: Post-Harvest DSS",
    page_icon="🌾",
    layout="wide"
)

# Header
st.title("🌾 AgriDecide Decision Support System")
st.markdown("""
**Empowering youth agripreneurs with data-driven post-harvest solutions**  
*Developed for [Competition Name] - Team [Your Team Name]*
""")

# Main DSS Interface
with st.container():
    st.header("1. Enter Harvest Details")
    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox(
            "Select Crop",
            options=list(CROP_RISK_RULES.keys()),
            help="Choose your harvested crop"
        )
    with col2:
        storage = st.selectbox(
            "Current Storage Method",
            options=list(CROP_RISK_RULES[crop].keys()),
            help="How the crop is currently stored"
        )

# DSS Analysis
if st.button("Generate Recommendations", type="primary"):
    with st.spinner("Analyzing your post-harvest scenario..."):
        recommendation = generate_recommendation(crop, storage)
        impact = calculate_economic_impact(crop, recommendation["risk_level"])
        
        st.header("2. DSS Analysis Report")
        
        # Risk Assessment
        with st.expander("📊 Risk Evaluation", expanded=True):
            cols = st.columns(3)
            cols[0].metric("Risk Level", recommendation["risk_level"])
            cols[1].metric("Current Loss Rate", impact["current_loss"])
            cols[2].metric("Projected Loss Rate", impact["projected_loss"])
            
            st.write(f"**Key Concern:** {recommendation['risk_reason']}")
        
        # Recommendations
        with st.expander("✅ Action Plan", expanded=True):
            st.write("**Immediate Actions:**")
            for action in recommendation["action_items"]:
                st.write(f"- {action}")
            
            st.write("\n**Long-Term Strategies:**")
            st.write("- Connect with local storage cooperatives")
            st.write("- Explore contract farming opportunities")
            st.write("- Consider value-added processing")
        
        # Economic Impact
        with st.expander("💵 Economic Impact", expanded=True):
            st.plotly_chart(px.bar(
                x=["Current", "With DSS"],
                y=[float(impact["current_loss"].strip('%')), 
                   float(impact["projected_loss"].strip('%'))],
                labels={"x": "Scenario", "y": "Loss Rate (%)"},
                title="Projected Loss Reduction"
            ))
            
            st.write(f"**Potential Value Saved:** {impact['value_saved']}")

# DSS Knowledge Base
with st.container():
    st.header("3. DSS Knowledge Base")
    tab1, tab2 = st.tabs(["Crop Guidelines", "About This System"])
    
    with tab1:
        for crop_name, methods in CROP_RISK_RULES.items():
            with st.expander(f"{crop_name.capitalize()} Storage Guidelines"):
                df = pd.DataFrame.from_dict(methods, orient="index")
                st.dataframe(df)
    
    with tab2:
        st.write("""
        **About This Decision Support System**  
        This tool combines agricultural expertise with data analysis to:
        - Predict post-harvest loss risks
        - Recommend mitigation strategies
        - Project economic impacts
        
        **Development Roadmap:**
        1. Phase 1: Rule-based recommendations (current)
        2. Phase 2: Machine learning integration
        3. Phase 3: Real-time market linkage
        """)

# Footer
st.markdown("---")
st.caption("""
Developed for [Competition Name] | Data sources: FMARD, FAO, NARO  
Team Members: [Your Names] | Contact: [Your Email]
""")
