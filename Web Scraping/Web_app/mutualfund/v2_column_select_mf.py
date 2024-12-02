import streamlit as st
import pandas as pd
import requests
import plotly.express as px

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
st.title("Mutual Fund Portfolio Analyzer")

# Load AMFI data
amfi_data = fetch_amfi_nav()

if amfi_data.empty:
    st.write("Unable to load mutual fund data. Please try again later.")
else:
    # Multi-select for mutual fund selection
    selected_funds = st.multiselect(
        "Select Mutual Funds:", 
        amfi_data["Fund Name"].tolist()
    )

    if selected_funds:
        # Create a DataFrame for selected funds
        selected_data = amfi_data[amfi_data["Fund Name"].isin(selected_funds)].reset_index(drop=True)

        # Add input columns for investment amount and display them side by side
        st.subheader("Enter Investment Amounts (₹)")

        investment_amounts = []

        for idx, row in selected_data.iterrows():
            # Create two columns: one for the fund name and one for the investment input
            col1, col2 = st.columns([3, 1])  # Ratio of 3:1 for labels and inputs

            # Fund name in the first column
            col1.write(f"{row['Fund Name']}")
            
            # Investment amount input in the second column (no label, just the input box)
            amount = col2.number_input(
                "",
                min_value=500, 
                step=500,
                format="%d",  # Use %d format to directly handle integers
                key=f"{row['Fund Name']}_{idx}"  # Unique key for each input
            )
            investment_amounts.append(amount)

        # Add the investment amounts as a new column
        selected_data["Investment Amount"] = investment_amounts

        # Calculate total investment and percentage distribution
        total_investment = selected_data["Investment Amount"].sum()
        if total_investment > 0:
            selected_data["Percentage"] = (
                selected_data["Investment Amount"] / total_investment * 100
            )

            # Display DataFrame
            st.subheader("Investment Summary")
            st.dataframe(selected_data)

            # Plot pie chart
            st.subheader("Portfolio Distribution")
            fig = px.pie(
                selected_data,
                names="Fund Name",
                values="Investment Amount",
                title="Percentage Distribution of Investments"
            )
            st.plotly_chart(fig)
        else:
            st.write("Please enter investment amounts to view the portfolio distribution.")
