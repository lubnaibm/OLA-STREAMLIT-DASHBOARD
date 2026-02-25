import streamlit as st
import mysql.connector
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("OLA Ride Analytics Dashboard")

# ----------------------------
# MySQL Connection
# ----------------------------

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="ola"
    )

# ----------------------------
# Function to Run Query
# ----------------------------

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ----------------------------
# SQL Queries Dictionary
# ----------------------------

queries = {

    "1️⃣ Total Successful Bookings by Vehicle Type":
    """
    SELECT Vehicle_Type,
           COUNT(*) AS Total_Successful_Bookings
    FROM ola
    WHERE Booking_Status = 'Success'
    GROUP BY Vehicle_Type;
    """,

    "2️⃣ Average Ride Distance by Vehicle Type":
    """
    SELECT Vehicle_Type,
           ROUND(AVG(Ride_Distance), 2) AS Avg_Ride_Distance
    FROM ola
    GROUP BY Vehicle_Type;
    """,

    "3️⃣ Rides Cancelled by Customer":
    """
    SELECT COUNT(*) AS Cancelled_By_Customer
    FROM ola
    WHERE Booking_Status = 'Canceled by Customer';
    """,

    "4️⃣ Top 5 Customers":
    """
    SELECT Customer_ID,
           COUNT(*) AS Total_Rides
    FROM ola
    GROUP BY Customer_ID
    ORDER BY Total_Rides DESC
    LIMIT 5;
    """,

    "5️⃣ Rides Cancelled by Driver":
    """
    SELECT COUNT(*) AS Cancelled_By_Driver
    FROM ola
    WHERE Booking_Status = 'Canceled by Driver'
    AND Canceled_Rides_By_Driver = 'Personal & Car related issue';
    """,

    "6️⃣ UPI Payments Count":
    """
    SELECT COUNT(*) AS UPI_Payments
    FROM ola
    WHERE Payment_Method = 'UPI';
    """,

    "7️⃣ Average Customer Rating per Vehicle Type":
    """
    SELECT Vehicle_Type,
           AVG(Customer_Rating) AS Avg_Customer_Rating
    FROM ola
    GROUP BY Vehicle_Type;
    """,

    "8️⃣ Total Successful Booking Value":
    """
    SELECT SUM(Booking_Value) AS Total_Success_Booking_Value
    FROM ola
    WHERE Booking_Status = 'Success';
    """,

    "9️⃣ Incomplete Ride Summary":
    """
    SELECT Booking_Status,
           COUNT(*) AS Total_Count
    FROM ola
    WHERE Booking_Status IN
        ('Canceled by Driver',
         'Canceled by Customer',
         'Driver Not Found')
    GROUP BY Booking_Status;
    """,

    "🔟 Incomplete Ride Reasons from Driver":
    """
    SELECT Incomplete_Rides_Reason,
           COUNT(*) AS Total_Count
    FROM ola
    WHERE Incomplete_Rides_Reason IN
        ('Customer Demand',
         'Vehicle Breakdown',
         'Other Issue')
    GROUP BY Incomplete_Rides_Reason;
    """,

    "11️⃣ Min & Max Ratings for Prime Sedan":
    """
    SELECT
        MIN(Driver_Ratings) AS Min_Rating,
        MAX(Driver_Ratings) AS Max_Rating
    FROM ola
    WHERE Vehicle_Type = 'Prime Sedan'
    AND Driver_Ratings > 0;
    """
}

# ----------------------------
# SQL SECTION
# ----------------------------

st.subheader("Run SQL Queries")

selected_query = st.selectbox("Select a Query", list(queries.keys()))

if st.button("Run Query"):
    result = run_query(queries[selected_query])
    st.dataframe(result, use_container_width=True)

# ----------------------------
# POWER BI EMBED SECTION
# ----------------------------

st.markdown("---")
st.subheader("Power BI Dashboard")

powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=ad38d71a-d398-41cd-92c8-1e5412ab0495&autoAuth=true&ctid=d33f5f7d-5a08-4f2c-8a18-850f1ffec9ac"

components.iframe(powerbi_url, width=1400, height=700)


