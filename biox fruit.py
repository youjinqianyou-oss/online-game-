import streamlit as st
import random

st.set_page_config(page_title="Blox Fruits Mini Game")
st.title("⚔️ Blox Fruits Mini Game")
st.write("Draw a fruit ➜ Fight enemies ➜ Earn points!")

# Game data
fruits = {
    "Dragon": {"power": 95},
    "Dough": {"power": 90},
    "Light": {"power": 80},
    "Ice": {"power": 70},
    "Smoke": {"power": 50},
}

enemies = {
    "Marine Soldier": 40,
    "Bandit": 50,
    "Snow Monster": 60,
    "Desert Officer": 70,
    "Boss: Shadow Samurai": 90,
}

# Initialize session state
if "fruit" not in st.session_state:
    st.session_state.fruit = None
if "score" not in st.session_state:
    st.session_state.score = 0

st.markdown("### 1️⃣ Draw a Fruit")

if st.button("🔮 Random Fruit!"):
    st.session_state.fruit = random.choice(list(fruits.keys()))
    st.success(f"You got: **{st.session_state.fruit}**!🔥")

if st.session_state.fruit:
    fruit_power = fruits[st.session_state._]()_

