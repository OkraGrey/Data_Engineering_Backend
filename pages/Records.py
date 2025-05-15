import streamlit as st
import pandas as pd
import sys
import os
import mysql.connector
  
# Add backend path
sys.path.append(os.path.join(os.path.dirname(__file__), "../Data_Engineering_Backend"))
from Data_Engineering_Backend.App import amenity_wrapper




def get_db_connection():
    """Reusable function to get a DB connection."""
    return mysql.connector.connect(
        host="localhost",
        user="umar",
        password="lahoRe@123",
        database="DE_FSP"
    )


def get_all_counties():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT COUNTY_NAME FROM counties WHERE COUNTY_NAME IS NOT NULL ORDER BY COUNTY_NAME ASC;")
        rows = cursor.fetchall()
        counties = [row[0] for row in rows]
        cursor.close()
        conn.close()
        return counties
    except Exception as e:
        print(f"Error fetching counties: {e}")
        return []


def get_all_amenities():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM amenities ORDER BY name ASC;")
        rows = cursor.fetchall()
        amenities = [row[0] for row in rows]
        cursor.close()
        conn.close()
        return amenities
    except Exception as e:
        print(f"Error fetching amenities: {e}")
        return []

    
    
# Page config
st.set_page_config(
    page_title="🚀 Business Search",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS FOR PROFESSIONAL FUTURISTIC DESIGN ---
st.markdown("""
<style>
/* GLOBAL STYLING */
body, .main {
    background: #0f1117;
    color: #e3e6ef;
    font-family: 'Inter', sans-serif;
    padding: 1rem 2rem;
}

h1, h2, h3, .title {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    color: #dfe6f3;
}

.subtitle {
    font-size: 1.1rem;
    color: #a4accf;
    font-weight: 500;
    margin-top: -1rem;
    text-align: center;
    margin-bottom: 2.5rem;
}

/* CARD STYLING */
.input-card {
    background: #1a1d2b;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 0 30px rgba(100, 130, 200, 0.2);
    max-width: 950px;
    margin: 0 auto 2rem auto;
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
}

/* INPUTS */
div[data-baseweb="input"] > input {
    background: #222531 !important;
    border: 1px solid #3c4266 !important;
    border-radius: 10px !important;
    color: #f0f3ff !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 0.9rem 1.2rem !important;
}

div[data-baseweb="input"] > input::placeholder {
    color: #999fbb !important;
    font-weight: 500 !important;
}

/* BUTTON */
button[kind="primary"] {
    background: linear-gradient(to right, #5f77f3, #7896ff) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    color: white !important;
    padding: 0.8rem 2rem !important;
    box-shadow: 0 4px 14px rgba(95, 119, 243, 0.4);
    transition: all 0.2s ease-in-out;
}

button[kind="primary"]:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 22px rgba(120, 150, 255, 0.45);
}

/* TABLE STYLING */
.stDataFrame > div {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid #3c4266 !important;
    background-color: #1a1d2b !important;
}

.stDataFrame table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: 100% !important;
    background-color: #1a1d2b !important;
    font-size: 0.94rem;
    color: #e3e6ef;
}

.stDataFrame thead tr {
    background-color: #222534 !important;
    color: #c7cbdf !important;
    font-weight: 600;
}

.stDataFrame th {
    padding: 0.85rem 1rem;
    text-align: left;
    border-bottom: 1px solid #3c4266;
}

.stDataFrame td {
    padding: 0.8rem 1rem;
    border-bottom: 1px solid #2a2e45;
}

.stDataFrame tbody tr:hover {
    background-color: #2a2e45 !important;
}

/* ALERT BOXES */
.stAlert > div {
    border-radius: 12px !important;
    font-size: 1.05rem !important;
}

.stSuccess > div {
    background-color: #26393a !important;
    border-left: 6px solid #4ff5c4 !important;
    color: #d2ffef !important;
}

.stWarning > div {
    background-color: #3c2f1a !important;
    border-left: 6px solid #f5a623 !important;
    color: #ffe8bd !important;
}

.stError > div {
    background-color: #3d1c26 !important;
    border-left: 6px solid #ff4d6d !important;
    color: #ffdbe3 !important;
}

.stInfo > div {
    background-color: #202338 !important;
    border-left: 6px solid #5f77f3 !important;
    color: #dbe0ff !important;
}

/* MOBILE RESPONSIVENESS */
@media (max-width: 768px) {
    .input-card {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
    }
    button[kind="primary"] {
        width: 100%;
    }
}
</style>
""", unsafe_allow_html=True)

# --- TITLE AND SUBTITLE ---
st.markdown('<h1 class="title">Business Data Viewer</h1>', unsafe_allow_html=True)

# --- INPUTS IN CARD STYLE ---
with st.container():
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        counties = get_all_counties()
        # Set default value to "" (the first option)
        county = st.selectbox("County", [""] + counties, index=1)

    with col2:
        amenities = get_all_amenities()
        # Set default value to "" (the first option)
        keyword = st.selectbox("Amenity", [""] + amenities, index=1)

    with col3:
        search_clicked = st.button("Search")
        
        
        
        
# --- HANDLE SEARCH AND DISPLAY RESULTS ---
if search_clicked:
    county_stripped = county.strip() if county else ""
    keyword_stripped = keyword.strip() if keyword else ""

    if not county_stripped and not keyword_stripped:
        st.warning("Please enter at least one of County or Keyword to search.")
    else:
        with st.spinner("Fetching data from backend..."):
            try:
                data = amenity_wrapper(county_stripped, keyword_stripped)
                if data:
                    df = pd.DataFrame(data)
                    st.success(f"Fetched {len(df):,} records.")
                    st.dataframe(df, use_container_width=True, height=420)
                else:
                    st.warning("No data found for the given inputs.")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Enter county and keyword, then click Search.")