import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(page_title="Global Pokémon Analytics", layout="wide",page_icon="🤑")

# 2. Data Loading (Using your specific columns)
@st.cache_data
def load_data():
    # Replace 'pokemon.json' with your actual filename
    df = pd.read_csv("./data/pokemon_data.csv")
    
    # Calculate Total Base Stats (BST)
    stats_cols = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    df['total_stats'] = df[stats_cols].sum(axis=1)
    
    # Identify Archetypes (Simple Logic)
    df['Type'] = 'Balanced'
    df.loc[df['speed'] > 110, 'Type'] = 'Speedster'
    df.loc[df['hp'] > 110, 'Type'] = 'Tank'
    df.loc[df['attack'] > 110, 'Type'] = 'Physical Attacker'
    df.loc[df['special-attack'] > 110, 'Type'] = 'Special Attacker'
    
    return df, stats_cols

df, stats_cols = load_data()

st.title("📊 Global Pokémon Data Analysis")
st.markdown("An overview of power distribution and attribute correlations across the dataset.")

# 3. Top Row: Global Stats
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Total Pokémon", len(df))
col_b.metric("Avg Total Stats", int(df['total_stats'].mean()))
col_c.metric("Highest Attack", df['attack'].max())
col_d.metric("Highest Speed", df['speed'].max())

st.divider()

# 4. Middle Row: Distributions
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution of Total Power (BST)")
    # Histogram showing the "Power Tiers"
    fig_hist = px.histogram(
        df, x="total_stats", 
        nbins=30, 
        color_discrete_sequence=['#636EFA'],
        labels={'total_stats': 'Total Base Stats'},
        marginal="rug" # Shows individual points at the bottom
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("Stat Variances (Box Plot)")
    # Box plot shows which stats have the most extreme outliers
    fig_box = px.box(
        df, y=stats_cols, 
        points="all", 
        color_discrete_sequence=['#EF553B'],
        title="Range of Individual Attributes"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# 5. Bottom Row: Competitive Landscape
st.subheader("Offensive vs. Defensive Balance")
# Scatter plot comparing Physical vs Special capabilities
fig_scatter = px.scatter(
    df, 
    x="attack", 
    y="defense", 
    size="total_stats", 
    color="Type",
    hover_name="name",
    template="plotly_dark",
    title="Physical Attack vs. Physical Defense (Size = Total Power)"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# 6. Leaderboard Section
st.divider()
st.subheader("🏆 Top 10 Most Powerful Pokémon")
top_10 = df.nlargest(10, 'total_stats')[['name', 'total_stats'] + stats_cols]
st.table(top_10)