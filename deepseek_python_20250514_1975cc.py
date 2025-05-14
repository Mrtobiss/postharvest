# SECTION 1: Project Setup & Imports

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random

# Page Config
st.set_page_config(page_title="AgroAccess Pro", layout="wide")

# Title
st.title("🚜 AgroAccess Pro - Empowering Smallholder Farmers")

# Subtitle
st.markdown(
    """
    Welcome to AgroAccess Pro — a data-powered profiling tool to improve access to finance, resources, and logistics for smallholder farmers.
    """
)

# Sidebar note
st.sidebar.markdown("👤 **User Settings**")

# Sample regions & crops (can expand later)
regions = ['North Central', 'North West', 'South West', 'South East', 'North East', 'South South']
crops = ['Maize', 'Rice', 'Cassava', 'Tomato', 'Yam', 'Groundnut', 'Soybean', 'Vegetables']

# SECTION 2: Sample Farmer Profile Generator

def generate_sample_farmer_data(n=200):
    data = []
    for i in range(n):
        region = random.choice(regions)
        crop = random.choice(crops)
        farm_size = round(np.random.uniform(0.5, 5), 2)  # hectares
        annual_yield = round(farm_size * random.uniform(1.5, 3.5), 2)  # tons
        logistics_access = random.choice(['None', 'Cold Truck Nearby', 'On-Demand Request'])
        needs_finance = random.choice([True, False])
        market_access = random.choice(['Low', 'Medium', 'High'])

        data.append({
            'Farmer ID': f'F{i+1:03d}',
            'Region': region,
            'Crop': crop,
            'Farm Size (ha)': farm_size,
            'Annual Yield (tons)': annual_yield,
            'Logistics': logistics_access,
            'Needs Finance': needs_finance,
            'Market Access': market_access
        })
    return pd.DataFrame(data)

# Create and cache sample dataset
@st.cache_data
def get_sample_data():
    return generate_sample_farmer_data()

df_farmers = get_sample_data()

# SECTION 3: Streamlit UI + Summary Dashboard

st.title("🌾 AgriAccess Insights Dashboard")
st.markdown("Supporting smallholder farmers with insights on logistics, finance, and market access.")

# Filters
with st.sidebar:
    st.header("🔎 Filter Options")
    selected_region = st.selectbox("Select Region", ["All"] + regions)
    selected_crop = st.selectbox("Select Crop", ["All"] + crops)

# Apply filters
filtered_df = df_farmers.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_crop != "All":
    filtered_df = filtered_df[filtered_df["Crop"] == selected_crop]

# Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("👩‍🌾 Total Farmers", len(filtered_df))
col2.metric("🚚 Logistics Gaps", filtered_df[filtered_df["Logistics"] == "None"].shape[0])
col3.metric("💰 Finance Needs", filtered_df[filtered_df["Needs Finance"]].shape[0])

st.markdown("---")

# Top Investment Opportunities
st.subheader("📊 Top Investment Opportunities")
inv_needs = {
    "Cold Storage Hubs": filtered_df[filtered_df["Logistics"] == "None"].shape[0],
    "Processing Plants": filtered_df[filtered_df["Market Access"] == "Low"].shape[0],
    "Credit Programs": filtered_df[filtered_df["Needs Finance"]].shape[0]
}
inv_df = pd.DataFrame(list(inv_needs.items()), columns=["Need", "Farmer Count"])
inv_df = inv_df.sort_values("Farmer Count", ascending=False)

st.dataframe(inv_df, use_container_width=True)

# SECTION 4: Cold Chain Logistics Matching System

st.subheader("🚚 Logistics Matching: Cold Storage Support")

# Get farmers with no logistics
no_logistics_df = filtered_df[filtered_df["Logistics"] == "None"]

# Simulated cold storage providers
cold_storage = pd.DataFrame({
    "Provider Name": ["CoolChain Ltd", "AgroChill Hub", "FreshLogistics NG"],
    "Region": ["North", "South", "East"],
    "Capacity (tons)": [50, 100, 80],
    "Specialty Crops": [["Tomatoes", "Pepper"], ["Cassava", "Maize"], ["Onion", "Pepper"]],
    "Contact": ["0802-111-0001", "0803-222-0002", "0804-333-0003"]
})

# Match logic: same region and crop
matches = []
for _, farmer in no_logistics_df.iterrows():
    for _, provider in cold_storage.iterrows():
        if provider["Region"] == farmer["Region"] and farmer["Crop"] in provider["Specialty Crops"]:
            matches.append({
                "Farmer ID": farmer["Farmer ID"],
                "Crop": farmer["Crop"],
                "Region": farmer["Region"],
                "Cold Storage Provider": provider["Provider Name"],
                "Contact": provider["Contact"]
            })

if matches:
    match_df = pd.DataFrame(matches)
    st.success(f"{len(match_df)} farmers matched with cold storage providers.")
    st.dataframe(match_df, use_container_width=True)
else:
    st.warning("No matches found. Consider expanding provider list or simulating more data.")

# SECTION 5: Investment Opportunity Dashboard

st.subheader("📊 Investment Opportunities Dashboard")

# Count missing resources by region
investment_needs = filtered_df.groupby("Region").agg({
    "Storage": lambda x: (x == "None").sum(),
    "Processing": lambda x: (x == "None").sum(),
    "Logistics": lambda x: (x == "None").sum()
}).reset_index()

investment_needs.columns = ["Region", "Lack of Storage", "Lack of Processing", "Lack of Logistics"]

# Sort by most underserved
sorted_investment = investment_needs.sort_values(by=["Lack of Storage", "Lack of Processing", "Lack of Logistics"], ascending=False)

st.markdown("### 🔍 Top Regions Lacking Infrastructure")
st.dataframe(sorted_investment, use_container_width=True)

# Highlight Top Priority Region
top_region = sorted_investment.iloc[0]
st.success(
    f"📍 **Top Priority Region**: {top_region['Region']}\n\n"
    f"- 🚫 Storage Gaps: {top_region['Lack of Storage']}\n"
    f"- ⚙️ Processing Gaps: {top_region['Lack of Processing']}\n"
    f"- 🚚 Logistics Gaps: {top_region['Lack of Logistics']}\n\n"
    "✅ Recommendation: Prioritize investment in storage hubs or mobile cold units in this area."
)

# SECTION 6: Footer & Optional Download

st.markdown("---")
st.markdown("### 📥 Download Filtered Dataset (Optional)")

# Optional CSV download
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_farmer_data.csv",
    mime="text/csv"
)

# Footer with team credit and hackathon note
st.markdown(
    """
    ---
    👩‍🌾 **AgroFinanceMatch**: Connecting farmers with finance and logistics for impact.  
    🚀 Built for the **Hackathon 2025** to improve access to affordable finance for youth agripreneurs in Nigeria.  
    💡 Powered by Streamlit and Python | 🔍 Data Source: [Sample/Uploaded CSV]
    """
)
