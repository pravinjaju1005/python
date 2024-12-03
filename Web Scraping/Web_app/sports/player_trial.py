import streamlit as st
import pandas as pd

# Sample player data (This can be expanded or replaced with a CSV)
player_data = {
    "Player": ["Virat Kohli", "Sachin Tendulkar", "MS Dhoni", "Rohit Sharma"],
    "Country": ["India", "India", "India", "India"],
    "Role": ["Batsman", "Batsman", "Wicketkeeper-Batsman", "Batsman"],
    "Batting Average": [59.07, 53.78, 40.83, 48.96],
    "Total Runs": [12040, 18426, 10773, 9205],
    "Centuries": [43, 49, 10, 29],
    "Matches Played": [254, 463, 350, 227],
}

# Convert to DataFrame
df = pd.DataFrame(player_data)

# Streamlit App Layout
st.title("Cricket Player Information")

# Dropdown to select player
player_name = st.selectbox("Select a Player:", df["Player"])

# Display player info
st.subheader(f"Details of {player_name}")
player_info = df[df["Player"] == player_name].iloc[0]

st.write(f"**Country**: {player_info['Country']}")
st.write(f"**Role**: {player_info['Role']}")
st.write(f"**Batting Average**: {player_info['Batting Average']}")
st.write(f"**Total Runs**: {player_info['Total Runs']}")
st.write(f"**Centuries**: {player_info['Centuries']}")
st.write(f"**Matches Played**: {player_info['Matches Played']}")

# Display a table of all players (optional)
st.subheader("All Players Stats")
st.dataframe(df)

# Add some styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f7f7;  /* Light gray background */
        color: #333;  /* Dark text color for better contrast */
    }
    .stTitle {
        font-size: 30px;
        color: #2c3e50;  /* Dark blue for title */
    }
    .stSubheader {
        font-size: 22px;
        color: #2c3e50;  /* Dark blue for subheaders */
    }
    .stText {
        color: #333;  /* Dark text for readability */
    }
    .stDataFrame {
        color: #333;  /* Ensure data is visible in table */
    }
    </style>
""", unsafe_allow_html=True)

