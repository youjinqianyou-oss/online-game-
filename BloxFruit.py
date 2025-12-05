import streamlit as st
import random

st.set_page_config(page_title="Blox Fruits Skill Battle")
st.title("🔥 Blox Fruits Skill Battle")
st.write("Draw a fruit ➜ Use skills ➜ Defeat enemies ➜ Earn points!")

# Game Data
fruits = {
    "Dragon": {
        "power": 95,
        "skills": ["Dragon Breath", "Dragon Claw"]
    },
    "Dough": {
        "power": 90,
        "skills": ["Dough Fist", "Dough Explosion"]
    },
    "Light": {
        "power": 80,
        "skills": ["Light Kick", "Light Beam"]
    },
    "Ice": {
        "power": 70,
        "skills": ["Ice Spikes", "Ice Bird"]
    },
}

enemies = {
    "Marine Soldier": 60,
    "Bandit": 75,
    "Snow Monster": 90,
    "Desert Officer": 100,
    "Boss: Shadow Samurai": 150,
}

# Session State Init
if "fruit" not in st.session_state:
    st.session_state.fruit = None
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
if "enemy_hp" not in st.session_state:
    st.session_state.enemy_hp = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "log" not in st.session_state:
    st.session_state.log = []

# Draw Fruit
st.markdown("### 1️⃣ Draw a Fruit")

if st.button("🔮 Random Fruit!"):
    st.session_state.fruit = random.choice(list(fruits.keys()))
    st.success(f"Fruit Selected: **{st.session_state.fruit}** 🔥")
    st.session_state.log.insert(0, f"Obtained {st.session_state.fruit}!")

# Battle Section
if st.session_state.fruit:
    fruit_data = fruits[st.session_state.fruit]
    fruit_power = fruit_data["power"]

    st.write(f"❤️ HP: **{st.session_state.player_hp}**")
    st.write(f"🔥 Power: **{fruit_power}**")

    st.markdown("---")
    st.markdown("### 2️⃣ Choose an Enemy")

    enemy_choice = st.selectbox("Pick Opponent:", list(enemies.keys()))

    if st.button("⚔️ Start Battle") and st.session_state.enemy_hp is No

