import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import requests

# Fetch AMFI data
@st.cache_data
def fetch_amfi_nav():
    """Fetch the latest NAV data from AMFI."""
    url = "https://www.amfiindia.com/spages/NAVAll.txt"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        nav_data = []
        for line in data.split("\n"):
            if not line.strip():
                continue
            
            fields = line.strip().split(";")
            if len(fields) < 5:
                continue
            
            try:
                nav_data.append({
                    "Fund ID": fields[0].strip(),
                    "Fund Code": fields[1].strip(),
                    "Fund Name": fields[3].strip(),
                    "NAV": float(fields[4].strip())
                })
            except ValueError:
                continue
        
        return pd.DataFrame(nav_data)
    else:
        st.error("Failed to fetch AMFI NAV data")
        return pd.DataFrame()

# Streamlit App
st.title("Mutual Fund NAV Finder")

# Load AMFI data
amfi_data = fetch_amfi_nav()

if amfi_data.empty:
    st.write("Unable to load mutual fund data. Please try again later.")
else:
    # Dropdown for fund name search
    fund_names = amfi_data["Fund Name"].tolist()
    selected_fund = st.selectbox(
        "Select a Mutual Fund:", 
        fund_names, 
        format_func=lambda x: x if x else "Search for a fund"
    )

    if selected_fund:
        # Display NAV details for the selected fund
        fund_details = amfi_data[amfi_data["Fund Name"] == selected_fund].iloc[0]
        st.subheader("Fund Details")
        st.write(f"**Fund Name:** {fund_details['Fund Name']}")
        st.write(f"**Fund ID:** {fund_details['Fund ID']}")
        st.write(f"**Fund Code:** {fund_details['Fund Code']}")
        st.write(f"**NAV:** {fund_details['NAV']:.2f}")

        # Additional interaction: input units and calculate total value
        units_owned = st.number_input("Enter Units Owned:", min_value=0.0, step=0.1, value=0.0)
        if units_owned > 0:
            total_value = units_owned * fund_details["NAV"]
            st.write(f"**Total Value of Investment:** ₹{total_value:.2f}")
