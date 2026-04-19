import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Berries",
    page_icon="🤑"
)


# 1. Page Config
st.set_page_config(page_title="Berry Agricultural Report", layout="wide")

# 2. Data Loading (Replace with your actual JSON loading logic)
@st.cache_data
def load_berry_data():
    df = pd.read_csv("./data/berries.csv")
    df["yield_efficiency"] = df["max_harvest"] / df["growth_time"]
    return df


df = load_berry_data()

st.title("🍓 Berry Agricultural & Potency Report")
st.markdown("Detailed analysis of berry growth cycles and technical attributes.")

# 3. Sidebar Filter
st.sidebar.header("Filter Berries")
min_power = st.sidebar.slider("Minimum Natural Gift Power", 0, 100, 60)
filtered_df = df[df['natural_gift_power'] >= min_power]

# 4. Top Row: KPIs
k1, k2, k3 = st.columns(3)
k1.metric("Fastest Grower", str.capitalize(df.loc[df['growth_time'].idxmin(), 'name']), f"{df['growth_time'].min()} hrs")
k2.metric("Highest Power", str.capitalize(df.loc[df['natural_gift_power'].idxmax(), 'name']), df['natural_gift_power'].max())
k3.metric("Avg Smoothness", f"{df['smoothness'].mean():.1f}")

st.divider()

# 5. Middle Row: Graphs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Growth vs. Harvest Efficiency")
    # A bubble chart showing growth time vs harvest, with size representing gift power
    fig_efficiency = px.scatter(
        filtered_df, 
        x="growth_time", 
        y="max_harvest",
        size="natural_gift_power", 
        color="name",
        hover_name="name",
        title="Growth Cycle vs. Yield Potential"
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)

with col2:
    st.subheader("Berry Size and Smoothness Distribution")
    # Box plot to show the physical variety of the berries
    fig_box = px.box(
        df, 
        y=["size", "smoothness"], 
        points="all",
        title="Physical Attribute Spread",
        color_discrete_sequence=["#FF4B4B"]
    )
    st.plotly_chart(fig_box, use_container_width=True)

# 6. Bottom Row: Soil and Power Correlation
st.subheader("Technical Attribute Correlation")
# Heatmap or Scatter showing Natural Gift Power vs Soil Dryness
fig_corr = px.density_heatmap(
    df, 
    x="natural_gift_power", 
    y="soil_dryness", 
    marginal_x="histogram", 
    marginal_y="histogram",
    title="Power vs. Maintenance (Soil Dryness)"
)
st.plotly_chart(fig_corr, use_container_width=True)

# 7. Raw Data Expander
with st.expander("View Complete Berry Database"):
    st.dataframe(df.sort_values("growth_time"))