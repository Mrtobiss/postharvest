import streamlit as st
import pandas as pd
import altair as alt

# ======================
# DSS KNOWLEDGE BASE
# ======================
CROP_RISK_RULES = {
    "maize": {
        "open sack": {"risk": "High", "reason": "Prone to mold in humidity", "recommendation": "Use hermetic bags"},
        "crib": {"risk": "Medium", "reason": "Rodent/pest exposure", "recommendation": "Treat with neem powder"},
        "silo": {"risk": "Low", "reason": "Controlled conditions", "recommendation": "Monitor moisture levels"}
    },
    "onion": {
        "open field": {"risk": "High", "reason": "Sunscald and sprouting", "recommendation": "Cure before storage"},
        "mesh bags": {"risk": "Medium", "reason": "Limited airflow", "recommendation": "Hang in ventilated shed"},
        "cold room": {"risk": "Low", "reason": "Dormancy preservation", "recommendation": "Maintain 0-4°C"}
    },
    "plantain": {
        "bunch hanging": {"risk": "Medium", "reason": "Even ripening", "recommendation": "Harvest at 75% maturity"},
        "cardboard box": {"risk": "High", "reason": "Bruising and compression", "recommendation": "Use separators"},
        "ripening room": {"risk": "Low", "reason": "Ethylene control", "recommendation": "Monitor daily"}
    },
    "yam": {
        "barn": {"risk": "Medium", "reason": "Sprouting after 3 months", "recommendation": "Treat with wood ash"},
        "pit": {"risk": "High", "reason": "Rot in rainy season", "recommendation": "Line with straw"},
        "cold storage": {"risk": "Low", "reason": "12-month shelf life", "recommendation": "Maintain 12°C"}
    },
    "cassava": {
        "open pile": {"risk": "High", "reason": "48-hour spoilage window", "recommendation": "Process immediately"},
        "trench": {"risk": "Medium", "reason": "Partial protection", "recommendation": "Cover with moist soil"},
        "processed flour": {"risk": "Low", "reason": "Stable shelf life", "recommendation": "Package when fully dry"}
    },
    "tomato": {
        "open basket": {"risk": "High", "reason": "Bruising and decay", "recommendation": "Use plastic crates"},
        "shaded shed": {"risk": "Medium", "reason": "Limited shelf life", "recommendation": "Sell within 2 days"},
        "cold chain": {"risk": "Low", "reason": "14-day freshness", "recommendation": "Pre-cool before storage"}
    }
}

LOGISTICS_OPTIONS = {
    "maize": ["Direct to market", "Grain silo", "Industrial buyer"],
    "onion": ["Local markets", "Export channels", "Processing plants"],
    "plantain": ["Roadside sales", "Urban markets", "Chips processors"],
    "yam": ["Village markets", "Interstate trade", "Export"],
    "cassava": ["Local processors", "Industrial starch", "Gari markets"],
    "tomato": ["Fresh markets", "Ketchup factories", "Supermarkets"]
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
                f"Logistics options: {', '.join(LOGISTICS_OPTIONS[crop])}"
            ],
            "storage_method": storage_method
        }
    except KeyError:
        return {
            "risk_level": "Unknown",
            "risk_reason": "No data available",
            "action_items": ["Consult agricultural officer"],
            "storage_method": storage_method
        }

def calculate_economic_impact(crop, risk_level):
    """DSS financial impact projection"""
    baseline = {
        "maize": {"high": 0.35, "medium": 0.2, "low": 0.1},
        "onion": {"high": 0.4, "medium": 0.25, "low": 0.15},
        "plantain": {"high": 0.45, "medium": 0.3, "low": 0.15},
        "yam": {"high": 0.3, "medium": 0.2, "low": 0.1},
        "cassava": {"high": 0.5, "medium": 0.3, "low": 0.15},
        "tomato": {"high": 0.4, "medium": 0.25, "low": 0.1}
    }
    reduction = {"High": 0.15, "Medium": 0.3, "Low": 0.5}
    
    loss_rate = baseline.get(crop, {}).get(risk_level.lower(), 0.3)
    improved_rate = loss_rate * (1 - reduction.get(risk_level, 0.2))
    
    return {
        "current_loss": f"{loss_rate*100:.0f}%",
        "projected_loss": f"{improved_rate*100:.0f}%",
        "value_saved": f"₦{(loss_rate - improved_rate)*75000:,.0f} per ton"
    }

# ======================
# DSS USER INTERFACE
# ======================
st.set_page_config(
    page_title="AgriSmart DSS",
    page_icon="🌱",
    layout="wide"
)

# Header
st.title("🌱 AgriSmart Decision Support System")
st.markdown("""
**Reducing Post-Harvest Losses for Nigerian Farmers**  
*Developed for [Competition Name] - Team [Your Team Name]*
""")

# Main DSS Interface
with st.container():
    st.header("1. Enter Harvest Details")
    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox(
            "SELECT CROP",
            options=list(CROP_RISK_RULES.keys()),
            help="Choose your harvested crop"
        )
    with col2:
        storage = st.selectbox(
            "STORAGE METHOD",
            options=list(CROP_RISK_RULES[crop].keys()),
            help="Current storage approach"
        )

# DSS Analysis
if st.button("GENERATE DSS REPORT", type="primary"):
    with st.spinner("Analyzing your post-harvest scenario..."):
        recommendation = generate_recommendation(crop, storage)
        impact = calculate_economic_impact(crop, recommendation["risk_level"])
        
        st.header("2. DSS Analysis Report")
        
        # Risk Assessment
        with st.expander("📊 RISK EVALUATION", expanded=True):
            cols = st.columns(3)
            cols[0].metric("RISK LEVEL", recommendation["risk_level"])
            cols[1].metric("CURRENT LOSS RATE", impact["current_loss"])
            cols[2].metric("PROJECTED LOSS RATE", impact["projected_loss"])
            
            st.markdown(f"""
            **CROP**: {crop.capitalize()}  
            **STORAGE METHOD**: {recommendation['storage_method']}  
            **KEY CONCERN**: {recommendation['risk_reason']}
            """)
        
        # Recommendations
        with st.expander("✅ ACTION PLAN", expanded=True):
            st.subheader("Immediate Actions")
            for action in recommendation["action_items"]:
                st.markdown(f"- {action}")
            
            st.subheader("Long-Term Strategies")
            st.markdown("""
            - Partner with storage cooperatives
            - Explore contract farming
            - Invest in value-addition
            """)
        
        # Economic Impact
        with st.expander("💵 ECONOMIC IMPACT", expanded=True):
            st.markdown(f"""
            | METRIC | BEFORE DSS | WITH DSS | IMPROVEMENT |
            |--------|------------|----------|-------------|
            | Loss Rate | {impact['current_loss']} | {impact['projected_loss']} | {float(impact['current_loss'].strip('%'))-float(impact['projected_loss'].strip('%'))}% |
            | Value Saved | - | {impact['value_saved']} | - |
            """)

# DSS Knowledge Base
with st.container():
    st.header("3. DSS Knowledge Base")
    tab1, tab2 = st.tabs(["📚 CROP GUIDELINES", "ℹ️ ABOUT THE SYSTEM"])
    
    with tab1:
        for crop_name, methods in CROP_RISK_RULES.items():
            with st.expander(f"{crop_name.upper()} STORAGE OPTIONS"):
                df = pd.DataFrame.from_dict(methods, orient="index")
                st.dataframe(df)
    
    with tab2:
        st.markdown("""
        ## About This DSS
        
        **Core Functions**:
        - Risk prediction for 6 major Nigerian crops
        - Storage and logistics recommendations
        - Economic impact projections
        
        **Development Roadmap**:
        1. Phase 1: Rule-based recommendations (current)
        2. Phase 2: Weather integration (Q3 2024)
        3. Phase 3: Market linkage (Q1 2025)
        
        **Data Sources**:
        - FMARD reports
        - FAO best practices
        - NARO field studies
        """)

# Footer
st.markdown("---")
st.caption("""
Developed for [Competition Name] | Data sources: FMARD, FAO, NARO  
Team Members: [Your Names] | Contact: [Your Email]  
Streamlit App | All rights reserved © 2024
""")
