import streamlit as st


# streamlit run ./dashboard/homepage.py

# 1. Page Configuration
st.set_page_config(
    page_title="Pokémon & Berry Analytics Hub",
    page_icon="",
    layout="wide"
)

st.sidebar.success("Select a page above")


# 2. Hero Header Image
# Using a high-quality landscape banner to set the theme

st.title("🐼 Pokémon Research & Agricultural Portal")
st.markdown("""
Welcome to the central hub for our data analysis project. This dashboard integrates multiple 
datasets to explore the quantitative side of the Pokémon world—from combat efficiency 
to agricultural berry production.
""")

st.divider()

# 3. Core Analysis Concepts
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📈 The Science of Base Stats")
    st.write("""
    Every Pokémon is defined by a set of six primary attributes that determine its effectiveness in battle. 
    Our analysis focuses on identifying patterns within these stats:
    
    * **The Combat Core:** How `Attack` and `Defense` interact to create 'Tanks' or 'Glass Cannons'.
    * **Specialization:** Measuring the reliance on `Special` attributes versus physical ones.
    * **Strategic Priority:** Evaluating how `Speed` tiers influence the competitive landscape.
    * **BST (Base Stat Total):** The ultimate KPI representing a Pokémon's cumulative power.
    """)
    
    with st.expander("View Statistical Methodology"):
        st.write("""
        We use Radar Charts to visualize individual balance and Histograms to view global 
        distribution. This allows us to spot 'outliers'—Pokémon that break the standard 
        power curve.
        """)

with col2:
    # Adding a visual example of a radar chart for the explanatory section
    st.image("./data/photos/jaypee.jpeg", 
             caption="", use_container_width=True)

st.divider()

# 4. Secondary Dataset: Berries
col3, col4 = st.columns([1, 2])

with col3:
    # Visual context for the berry report
    st.image("./data/photos/lebron.jpeg", 
             caption="Standard Berry Varieties", use_container_width=True)

with col4:
    st.header("🍓 Agricultural Productivity")
    st.write("""
    Our secondary report focuses on the **Berry Economy**. By analyzing the attributes 
    stored in our JSON data, we can calculate the efficiency of different crops.
    
    **Key Metrics Analyzed:**
    * **Yield per Hour:** Calculated as `max_harvest` / `growth_time`.
    * **Potency Index:** Based on `natural_gift_power`.
    * **Maintenance Requirement:** Correlating `soil_dryness` with growth speed.
    """)

st.divider()

# 5. Dashboard Navigation Guide
st.header("🗺️ Report Navigation")
nav1, nav2, nav3 = st.columns(3)

with nav1:
    with st.container(border=True):
        st.subheader("📊 Global Analytics")
        st.info("Explore the big-picture distributions and correlations across all species.")

with nav2:
    with st.container(border=True):
        st.subheader("🔍 Pokémon Explorer")
        st.info("A paginated catalog to browse individual stats and official artwork.")

with nav3:
    with st.container(border=True):
        st.subheader("🍒 Berry Report")
        st.info("Deep dive into agricultural efficiency and technical berry potency.")

# 6. Footer
st.caption("Technical Report Framework | Created for Academic Data Analysis Assignment")