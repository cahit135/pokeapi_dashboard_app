import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Pokémon Explorer", layout="wide")

# 2. Direct Data Loading (Since it's not pulling from a Home page)
@st.cache_data
def get_data():
    # Replace with your actual JSON filename
    df = pd.read_csv("./data/pokemon_data.csv")
    stats_cols = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    df['bst'] = df[stats_cols].sum(axis=1)
    return df, stats_cols

df, stats_cols = get_data()

# 3. Sidebar Search & Controls
st.sidebar.header("Navigation Controls")
search_query = st.sidebar.text_input("Search Pokémon Name", "").lower()

# 2. Use .str.contains with case=False and na=False
display_df = df[df['name'].str.contains(search_query, case=False, na=False)] if search_query else df
# 4. Pagination Setup
items_per_page = 10
total_items = len(display_df)
max_pages = max(0, (total_items - 1) // items_per_page)

# Initialize page number
if 'explorer_page' not in st.session_state:
    st.session_state.explorer_page = 0

# 5. Header & Navigation Buttons
st.title("🐾 Pokémon Explorer")
st.caption(f"Showing {total_items} Pokémon results")

nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if st.button("⬅️ Previous") and st.session_state.explorer_page > 0:
        st.session_state.explorer_page -= 1
        st.rerun()

with nav_col2:
    st.markdown(f"<p style='text-align: center;'>Page {st.session_state.explorer_page + 1} of {max_pages + 1}</p>", unsafe_allow_html=True)

with nav_col3:
    if st.button("Next ➡️") and st.session_state.explorer_page < max_pages:
        st.session_state.explorer_page += 1
        st.rerun()

st.divider()

# 6. Display Loop
start_idx = st.session_state.explorer_page * items_per_page
end_idx = start_idx + items_per_page
batch = display_df.iloc[start_idx:end_idx]

if batch.empty:
    st.warning("No Pokémon found matching your search.")
else:
    for _, row in batch.iterrows():
        with st.container(border=True):
            img_col, stat_col = st.columns([1, 2])
            
            with img_col:
                # Use a placeholder if the photo link is missing
                img_path = row['photo'] if pd.notna(row['photo']) else "https://via.placeholder.com/150"
                st.image(img_path, width=180)
            
            with stat_col:
                st.subheader(row['name'].title())
                
                # Create a mini grid for stats
                s1, s2, s3 = st.columns(3)
                s1.write(f"**HP:** {row['hp']}")
                s1.write(f"**ATK:** {row['attack']}")
                
                s2.write(f"**DEF:** {row['defense']}")
                s2.write(f"**SP.ATK:** {row['special-attack']}")
                
                s3.write(f"**SP.DEF:** {row['special-defense']}")
                s3.write(f"**SPD:** {row['speed']}")
                
                # Overall Power Bar
                # BST (Base Stat Total) is usually maxed at 720 for Arceus
                power_percent = min(row['bst'] / 720, 1.0)
                st.progress(power_percent, text=f"Total Power: {row['bst']}")