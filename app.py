import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Restaurant Analytics",
    layout="wide"
)

# ------------------ DATABASE CONNECTION ------------------
@st.cache_resource
def get_engine():
    try:
        password = urllib.parse.quote_plus("27665431shanV#")
        user = "root"
        host = "127.0.0.1"
        database = "uber_db"

        conn_str = (
            f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        )

        engine = create_engine(conn_str)

        return engine

    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None


engine = get_engine()

# ------------------ TITLE ------------------
st.title("🍴 Restaurant Analytics System")
st.markdown("---")

# ------------------ SIDEBAR ------------------
page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "General Q&A", "Orders Analysis"]
)

# =========================================================
# 📊 DASHBOARD
# =========================================================
if page == "Dashboard":

    st.header("🔍 Filter Restaurants")

    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input(
            "Enter Location (Example: Koramangala)"
        )

    with col2:
        rating = st.slider(
            "Minimum Rating",
            0.0,
            5.0,
            3.0
        )

    query = """
        SELECT name, location, rate, votes
        FROM uber_data
        WHERE rate >= %s
    """

    params = (rating,)

    if location:
        query += " AND location LIKE %s"
        params += (f"%{location}%",)

    if engine:
        try:
            df = pd.read_sql(
                query,
                engine,
                params=params
            )

            st.subheader(f"Results Found: {len(df)}")
            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Query Error: {e}")

# =========================================================
# 📈 GENERAL Q&A
# =========================================================
elif page == "General Q&A":

    st.header("💡 Business Insights")

    questions = {

        "Total Restaurants":
        """
        SELECT COUNT(*) AS total_restaurants
        FROM uber_data
        """,

        "Top 5 Locations by Restaurant Count":
        """
        SELECT location,
               COUNT(*) AS total
        FROM uber_data
        GROUP BY location
        ORDER BY total DESC
        LIMIT 5
        """,

        "Average Rating":
        """
        SELECT ROUND(AVG(rate), 2) AS avg_rating
        FROM uber_data
        """,

        "Top 10 Highest Rated Restaurants":
        """
        SELECT name, rate
        FROM uber_data
        ORDER BY rate DESC
        LIMIT 10
        """,

        "Most Popular Restaurants (Votes)":
        """
        SELECT name, votes
        FROM uber_data
        ORDER BY votes DESC
        LIMIT 10
        """,

        "Average Cost for Two":
        """
        SELECT ROUND(
            AVG(`approx_cost(for two people)`),
            0
        ) AS avg_cost
        FROM uber_data
        """,

        "Online Order Availability":
        """
        SELECT online_order,
               COUNT(*) AS count
        FROM uber_data
        GROUP BY online_order
        """,

        "Table Booking Availability":
        """
        SELECT book_table,
               COUNT(*) AS count
        FROM uber_data
        GROUP BY book_table
        """,

        "Top 5 Expensive Restaurants":
        """
        SELECT name,
               `approx_cost(for two people)`
        FROM uber_data
        ORDER BY `approx_cost(for two people)` DESC
        LIMIT 5
        """,

        "Top 5 Locations by Average Rating":
        """
        SELECT location,
               ROUND(AVG(rate), 2) AS avg_rate
        FROM uber_data
        GROUP BY location
        ORDER BY avg_rate DESC
        LIMIT 5
        """
    }

    selected_q = st.selectbox(
        "Choose a Question",
        list(questions.keys())
    )

    if engine:
        try:
            df = pd.read_sql(
                questions[selected_q],
                engine
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Query Error: {e}")

# =========================================================
# 📦 ORDERS ANALYSIS
# =========================================================
elif page == "Orders Analysis":

    st.header("📦 Restaurant Orders Insights")

    order_queries = {

        "Restaurants with Online Orders":
        """
        SELECT online_order,
               COUNT(*) AS total
        FROM uber_data
        GROUP BY online_order
        """,

        "Top 10 Restaurants by Votes":
        """
        SELECT name, votes
        FROM uber_data
        ORDER BY votes DESC
        LIMIT 10
        """,

        "Top Rated Restaurants":
        """
        SELECT name, rate
        FROM uber_data
        ORDER BY rate DESC
        LIMIT 10
        """,

        "Average Cost by Location":
        """
        SELECT location,
               ROUND(
                   AVG(`approx_cost(for two people)`),
                   0
               ) AS avg_cost
        FROM uber_data
        GROUP BY location
        ORDER BY avg_cost DESC
        LIMIT 10
        """
    }

    selected_order_q = st.selectbox(
        "Select Analysis",
        list(order_queries.keys())
    )

    if engine:
        try:
            df = pd.read_sql(
                order_queries[selected_order_q],
                engine
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Query Error: {e}")