import streamlit as st
import random

st.set_page_config(page_title="Blox Fruits Battle Adventure")
st.title("⚔️ Blox Fruits Battle Adventure")
st.write("Draw a fruit ➜ Fight enemies ➜ Survive as long as you can!")

# Game Data
fruits = {
    "Dragon": {"power": 95},
    "Dough": {"power": 90},
    "Light": {"power": 80},
    "Ice": {"power": 70},
    "Smoke": {"power": 50},
}

enemies = {
    "Marine Soldier": 50,
    "Bandit": 60,
    "Snow Monster": 70,
    "Desert Officer": 80,
    "Boss: Shadow Samurai": 100,
}

# State initialization
if "fruit" not in st.session_state:
    st.session_state.fruit = None
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
if "score" not in st.session_state:
    st.session_state.score = 0
if "log" not in st.session_state:
    st.session_state.log = []

# Step 1: Draw Fruit
st.markdown("### 1️⃣ Draw a Fruit")

if st.button("🔮 Random Fruit!"):
    st.session_state.fruit = random.choice(list(fruits.keys()))
    st.session_state.log.insert(0, f"You obtained **{st.session_state.fruit}**!")
    st.success(f"Fruit chosen: {st.session_state.fruit}")

# Step 2: Battle System
if st.session_state.fruit:
    fruit_power = fruits[st.session_state.fruit]["power"]
    st.write(f"Your HP: **{st.session_state.player_hp}** ❤️")
    st.write(f"Fruit Power: **{fruit_power}** 🔥")

    st.markdown("---")
    st.markdown("### 2️⃣ Choose an Enemy")

    enemy = st.selectbox("Pick a target:", list(enemies.keys()))
    enemy_hp = enemies[enemy]

    if st.button("⚔️ Attack!"):
        player_damage = random.randint(10, fruit_power // 2)
        enemy_damage = random.randint(5, 20)

        st.session_state.log.insert(0, f"You dealt **{player_damage}** dmg to {enemy}")
        st.session_state.log.insert(0, f"{enemy} hit you for **{enemy_damage}** dmg")

        st.session_state.player_hp -= enemy_damage

        if player_damage >= enemy_hp:
            st.session_state.score += 20
            st.session_state.log.insert(0, f"🎉 You defeated **{enemy}**! +20 points")

        if st.session_state.player_hp <= 0:
            st.error("💀 You have been defeated!")
            st.session_state.player_hp = 0

    if st.button("🍎 Heal"):
        heal_amount = random.randint(10, 25)
        st.session_state.player_hp = min(100, st.session_state.player_hp + heal_amount)
        st.session_state.log.insert(0, f"You healed **{heal_amount} HP**!")

# Score + Reset
st.markdown("---")
st.subheader(f"🏆 Score: {st.session_state.score}")

if st.button("🔁 Restart Game"):
    st.session_state.fruit = None
    st.session_state.player_hp = 100
    st.session_state.score = 0
    st.session_state.log = []
    st.info("Game restarted!")

# Battle Log
st.markdown("---")
st.subheader("📜 Battle Log")
for entry in st.session_state.log[:10]:
    st.write(entry)
