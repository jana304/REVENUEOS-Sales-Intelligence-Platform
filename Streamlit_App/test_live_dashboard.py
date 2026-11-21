
import streamlit as st
from google_sheets_connection import load_live_sales_data

# Page configuration
st.set_page_config(
    page_title="REVENUEOS Live Sales Test",
    layout="wide"
)

# Page heading
st.title("REVENUEOS — Live Sales Data")

st.caption("Data source: Google Sheets — Sales_Analytics")

# Refresh button
if st.button("Refresh Live Data"):
    st.rerun()

# Load live sales data
try:
    df = load_live_sales_data()

    st.success("Google Sheets connected successfully!")

    st.write("Total Live Sales Records:", len(df))

    st.subheader("Live Sales Records")

    # Select columns to display
    display_columns = [
        "Opportunity ID",
        "Sales Agent",
        "Customer Account",
        "Product",
        "Deal Stage",
        "Deal Value",
        "Regional Office",
        "Sales Priority"
    ]

    if df.empty:
        st.info("No live sales records available.")

    else:
        # Display sales data as an HTML table
        table_html = df[display_columns].to_html(
            index=False,
            escape=True
        )

        st.markdown(
            table_html,
            unsafe_allow_html=True
        )

except Exception as error:
    st.error("Unable to load Google Sheets data.")
    st.error(str(error))
