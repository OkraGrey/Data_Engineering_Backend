import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config("📊 DE-FSP Dashboard", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <h1 style='text-align: left; padding-top: 10px; font-size: 2.5rem; color: #2c3e50;'>
       Dashboard
    </h1>
""", unsafe_allow_html=True)
# --- DATABASE CONNECTION ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="DE-FSP"
    )

@st.cache_data(ttl=300, show_spinner="Fetching data...")
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as total FROM amenities")
        amenities = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM counties")
        counties = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM osm_keys")
        osm_keys = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM queries")
        queries = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM records")
        records = cursor.fetchone()['total']

        cursor.execute("SELECT county, COUNT(*) as count FROM queries GROUP BY county ORDER BY count DESC LIMIT 8")
        top_counties = pd.DataFrame(cursor.fetchall())

        cursor.execute("SELECT key_name, count_all FROM osm_keys ORDER BY count_all DESC LIMIT 8")
        osm_keys_data = pd.DataFrame(cursor.fetchall())

        cursor.execute("SELECT * FROM queries ORDER BY timestamp DESC LIMIT 10")
        recent_queries = pd.DataFrame(cursor.fetchall())

        cursor.execute("""
            SELECT name, brand, operator, latitude, longitude 
            FROM records 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
            LIMIT 300
        """)
        locations = pd.DataFrame(cursor.fetchall())

        cursor.execute("""
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM queries
            WHERE timestamp >= CURDATE() - INTERVAL 30 DAY
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        """)
        queries_over_time = pd.DataFrame(cursor.fetchall())

        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM amenities 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 8
        """)
        amenities_by_cat = pd.DataFrame(cursor.fetchall())

        return {
            "amenities": amenities,
            "counties": counties,
            "osm_keys": osm_keys,
            "queries": queries,
            "records": records,
            "top_counties": top_counties,
            "osm_keys_data": osm_keys_data,
            "recent_queries": recent_queries,
            "locations": locations,
            "queries_over_time": queries_over_time,
            "amenities_by_cat": amenities_by_cat
        }
    finally:
        cursor.close()
        conn.close()

# --- HEADER WITH NAVIGATION ---

st.markdown("---")

# --- PAGE LOGIC ---
current_page = st.query_params.get("page", ["dashboard"])[0]


if current_page == "records":
    st.title("📋 Records Page")
    st.write("This is the Records page where you can manage or view records.")
    # You can add records page content here
else:
    # --- FETCH DATA ---
    data = fetch_data()

    # --- KPI CARDS ---
    metric_cols = st.columns(5)
    metric_data = {
        "Amenities": data["amenities"],
        "Counties": data["counties"],
        "OSM Keys": data["osm_keys"],
        "Queries": data["queries"],
        "Records": data["records"]
    }

    card_style = """
        background: #f0f2f6;
        border-radius: 12px;
        padding: 20px 0;
        box-shadow: 0 2px 5px rgb(0 0 0 / 0.1);
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    """
    number_style = "font-size: 2.5rem; font-weight: 700; color: #34495e; margin: 0;"
    label_style = "font-size: 1rem; font-weight: 600; color: #7f8c8d; margin: 0;"

    for col, (label, value) in zip(metric_cols, metric_data.items()):
        col.markdown(
            f"""
            <div style="{card_style}">
                <p style="{number_style}">{value}</p>
                <p style="{label_style}">{label}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # --- MAIN VISUALIZATION LAYOUT ---
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.subheader("Top Queried Counties")
        if not data["top_counties"].empty:
            fig = px.bar(data["top_counties"], x="county", y="count", color="count",
                         color_continuous_scale=px.colors.sequential.Blues,
                         labels={"county": "County", "count": "Queries"},
                         template="simple_white", height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No county data available")

        st.subheader("Amenities by Category")
        if not data["amenities_by_cat"].empty:
            fig = px.bar(data["amenities_by_cat"], x="category", y="count", color="count",
                         color_continuous_scale=px.colors.sequential.Teal,
                         labels={"category": "Category", "count": "Count"},
                         template="simple_white", height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")

        st.subheader("Queries Over Last 30 Days")
        if not data["queries_over_time"].empty:
            fig = px.line(data["queries_over_time"], x="date", y="count", markers=True,
                          labels={"date": "Date", "count": "Queries"},
                          template="simple_white", height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent query data")

    with right_col:
        st.subheader("Top OSM Keys Usage")
        if not data["osm_keys_data"].empty:
            fig = px.pie(data["osm_keys_data"], names="key_name", values="count_all",
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         template="simple_white", height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No OSM key data")

        st.subheader("Records Location Map")
        if not data["locations"].empty:
            fig = px.scatter_mapbox(data["locations"], lat="latitude", lon="longitude",
                                    hover_name="name", hover_data=["brand", "operator"],
                                    zoom=4, height=350, mapbox_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No location data")

        st.subheader("Recent Queries")
        if not data["recent_queries"].empty:
            st.dataframe(
                data["recent_queries"].head(5),
                use_container_width=True,
                height=300,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("Timestamp"),
                    "county": "County",
                    "key": "Key"
                }
            )
        else:
            st.info("No recent queries data")

    st.markdown("---")
    st.caption(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
