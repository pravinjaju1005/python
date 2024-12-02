import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize data
if "franchise_data" not in st.session_state:
    st.session_state["franchise_data"] = pd.DataFrame(columns=["Franchise ID", "Name", "Location", "Manager", "Contact", "Sales"])

# Helper function to add franchise
def add_franchise(data):
    st.session_state["franchise_data"] = pd.concat([st.session_state["franchise_data"], pd.DataFrame([data])], ignore_index=True)

# Helper function to display the dashboard
def show_dashboard():
    st.title("Franchise Management System - Dashboard")
    data = st.session_state["franchise_data"]
    if not data.empty:
        # Display overall metrics
        total_franchises = data["Franchise ID"].nunique()
        total_sales = data["Sales"].sum()
        st.metric("Total Franchises", total_franchises)
        st.metric("Total Sales", f"${total_sales:,.2f}")

        # Sales analysis
        fig = px.bar(data, x="Name", y="Sales", title="Sales by Franchise", labels={"Name": "Franchise", "Sales": "Total Sales"})
        st.plotly_chart(fig)
    else:
        st.info("No data available. Please add franchises.")

# Helper function to manage franchises
def manage_franchises():
    st.title("Manage Franchises")
    with st.form("add_franchise_form"):
        franchise_id = st.text_input("Franchise ID")
        name = st.text_input("Name")
        location = st.text_input("Location")
        manager = st.text_input("Manager")
        contact = st.text_input("Contact")
        sales = st.number_input("Sales", min_value=0.0, value=0.0)
        submitted = st.form_submit_button("Add Franchise")
        
        if submitted:
            add_franchise({"Franchise ID": franchise_id, "Name": name, "Location": location, "Manager": manager, "Contact": contact, "Sales": sales})
            st.success("Franchise added successfully!")

    # Display franchise table
    st.subheader("Existing Franchises")
    data = st.session_state["franchise_data"]
    if not data.empty:
        st.dataframe(data)

# Streamlit app navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Manage Franchises"])

if menu == "Dashboard":
    show_dashboard()
elif menu == "Manage Franchises":
    manage_franchises()
