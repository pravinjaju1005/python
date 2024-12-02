import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Nifty 50 Stock Symbols and their respective Company Names
nifty_50 = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank',
    'HINDUNILVR.NS': 'Hindustan Unilever',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank',
    'SBIN.NS': 'State Bank of India',
    'BAJFINANCE.NS': 'Bajaj Finance',
    'BHARTIARTL.NS': 'Bharti Airtel',
    'LARSEN.NS': 'Larsen & Toubro',
    'HCLTECH.NS': 'HCL Technologies',
    'ITC.NS': 'ITC Limited',
    'MARUTI.NS': 'Maruti Suzuki',
    'M&M.NS': 'Mahindra & Mahindra',
    'TITAN.NS': 'Titan Company',
    'ASIANPAINT.NS': 'Asian Paints',
    'ULTRACEMCO.NS': 'UltraTech Cement',
    'WIPRO.NS': 'Wipro',
    'HDFCLIFE.NS': 'HDFC Life Insurance',
    'NTPC.NS': 'NTPC Limited',
    'ADANIGREEN.NS': 'Adani Green Energy',
    'BPCL.NS': 'Bharat Petroleum',
    'SHREECEM.NS': 'Shree Cement',
    'SUNPHARMA.NS': 'Sun Pharmaceutical Industries',
    'DIVISLAB.NS': 'Divi’s Laboratories',
    'JSWSTEEL.NS': 'JSW Steel',
    'INDUSINDBK.NS': 'IndusInd Bank',
    'POWERGRID.NS': 'Power Grid Corporation of India',
    'TECHM.NS': 'Tech Mahindra',
    'ONGC.NS': 'Oil and Natural Gas Corporation',
    'TATAMOTORS.NS': 'Tata Motors',
    'NESTLEIND.NS': 'Nestle India',
    'CIPLA.NS': 'Cipla',
    'APOLLOHOSP.NS': 'Apollo Hospitals',
    'TATACONSUM.NS': 'Tata Consumer Products',
    'ZOMATO.NS': 'Zomato',
    'DRREDDY.NS': 'Dr. Reddy’s Laboratories',
    'MUTHOOTFIN.NS': 'Muthoot Finance',
    'GRASIM.NS': 'Grasim Industries',
    'INDHOTEL.NS': 'Indian Hotels Company',
    'M&MFIN.NS': 'M&M Financial Services',
    'BAJAJFINSV.NS': 'Bajaj Finserv',
    'RECLTD.NS': 'Rural Electrification Corporation',
    'EICHERMOT.NS': 'Eicher Motors',
    'BOSCHLTD.NS': 'Bosch Limited',
    'ICICIPRULI.NS': 'ICICI Prudential Life Insurance',
    'COALINDIA.NS': 'Coal India',
    'MINDTREE.NS': 'Mindtree',
    'PVR.NS': 'PVR Limited'
}

# Streamlit App
st.title("Equity Portfolio Analyzer")

# Map company names to stock symbols for user-friendly dropdown
company_names = list(nifty_50.values())

# Multi-select for company selection (display company names)
selected_companies = st.multiselect(
    "Select Equities from Nifty 50:", 
    company_names
)

# Retrieve the corresponding symbols for the selected companies
selected_symbols = [symbol for symbol, name in nifty_50.items() if name in selected_companies]

if selected_symbols:
    # Fetch stock data using yfinance
    stock_data = {}
    for symbol in selected_symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        stock_data[symbol] = {
            "Stock Name": nifty_50[symbol],
            "Current Price": data['Close'].iloc[-1]  # Most recent closing price
        }
    
    # Convert stock data into DataFrame
    stock_df = pd.DataFrame(stock_data).T.reset_index(drop=True)
    
    # Add input columns for quantity and display them side by side
    st.subheader("Enter Quantity of Shares to Buy")

    quantities = []
    
    for idx, row in stock_df.iterrows():
        # Create two columns: one for the stock name and one for the quantity input
        col1, col2 = st.columns([3, 1])  # Ratio of 3:1 for labels and inputs

        # Stock name in the first column
        col1.write(f"{row['Stock Name']}")
        
        # Quantity input in the second column (increment by 1)
        quantity = col2.number_input(
            "",
            min_value=1,  # Minimum value of 1 share
            step=1,  # Increment by 1
            format="%d",  # Use %d format to directly handle integers
            key=f"{row['Stock Name']}_{idx}"  # Unique key for each input
        )
        quantities.append(quantity)

    # Add the quantities as a new column
    stock_df["Quantity"] = quantities

    # Calculate the total investment and portfolio value
    stock_df["Total Value"] = stock_df["Quantity"] * stock_df["Current Price"]

    total_investment = stock_df["Total Value"].sum()
    if total_investment > 0:
        stock_df["Percentage"] = (
            stock_df["Total Value"] / total_investment * 100
        )

        # Display DataFrame
        st.subheader("Investment Summary")
        st.dataframe(stock_df)

        # Plot pie chart for portfolio distribution
        st.subheader("Portfolio Distribution")
        fig = px.pie(
            stock_df,
            names="Stock Name",
            values="Total Value",
            title="Percentage Distribution of Equity Portfolio"
        )
        st.plotly_chart(fig)
    else:
        st.write("Please enter quantities to view the portfolio distribution.")
