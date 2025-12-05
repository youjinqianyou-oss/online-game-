import streamlit as st

# ------------------- Data ---------------------
blox_fruits = {
    "Dragon": {
        "Type": "Beast",
        "Rarity": "Mythical",
        "Price": "3,500,000$ / 2,600 Robux",
        "Notes": "Strong transformations and high damage."
    },
    "Dough": {
        "Type": "Elemental",
        "Rarity": "Mythical",
        "Price": "2,800,000$ / 2,400 Robux",
        "Notes": "Popular for PvP due to combos."
    },
    "Light": {
        "Type": "Elemental",
        "Rarity": "Rare",
        "Price": "650,000$ / 1100 Robux",
        "Notes": "Fast travel and good grinding."
    },
    "Ice": {
        "Type": "Elemental",
        "Rarity": "Uncommon",
        "Price": "350,000$ / 750 Robux",
        "Notes": "Great early-game crowd control."
    },
}

tips = [
    "Grinding on the right island level makes leveling way faster!",
    "Fruit spawns every 60 minutes and despawns after 20 minutes.",
    "Join a crew or friend group to take down bosses easier.",
    "Beli is important—save up and unlock better fighting styles!"
]

# ------------------- UI ---------------------
st.set_page_config(page_title="Blox Fruits Info Hub", layout="centered")
st.title("🍇 Blox Fruits Info Hub")
st.write("Explore popular fruits and learn tips to improve in the game!")

# Fruit viewer
fruit_choice = st.selectbox("Choose a Fruit", list(blox_fruits.keys()))
fruit_info = blox_fruits[fruit_choice]

st.subheader(fruit_choice)
for k, v in fruit_info.items():
    st.write(f"**{k}:** {v}")

st.markdown("---")

# Tips section
st.subheader("⭐ Beginner Tips")
for tip in tips:
    st.write(f"- {tip}")

st.markdown("---")

# Just-for-fun poll
st.subheader("📊 Favorite Fruit Poll")
vote = st.radio("Pick your favorite fruit:", list(blox_fruits.keys()))
if st.button("Submit Vote"):
    st.success(f"Thanks! You voted for {vote} 🍏")
