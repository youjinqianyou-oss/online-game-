# app.py
import streamlit as st
import random

st.set_page_config(page_title="Blox Fruits Skill Battle", layout="centered")
st.title("🔥 Blox Fruits Skill Battle")
st.write("Draw a fruit → Use skills → Defeat enemies → Earn points!")

# ---------------------------
# Game data
# ---------------------------
FRUITS = {
    "Dragon": {"power": 95, "skills": ["Dragon Breath", "Dragon Claw"]},
    "Dough": {"power": 90, "skills": ["Dough Fist", "Dough Explosion"]},
    "Light": {"power": 80, "skills": ["Light Kick", "Light Beam"]},
    "Ice": {"power": 70, "skills": ["Ice Spikes", "Ice Bird"]},
    "Smoke": {"power": 60, "skills": ["Smoke Slash", "Vanish Strike"]},
}

ENEMIES = {
    "Marine Soldier": 60,
    "Bandit": 75,
    "Snow Monster": 90,
    "Desert Officer": 100,
    "Boss: Shadow Samurai": 150,
}

# ---------------------------
# Session state initialization
# ---------------------------
def init_state():
    defaults = {
        "fruit": None,               # chosen fruit name
        "player_hp": 100,            # player's HP
        "enemy_hp": None,            # current enemy HP (int) or None
        "current_enemy": None,       # current enemy name
        "score": 0,                  # player score
        "log": [],                   # action log (newest first)
        "battle_active": False,      # whether a battle is ongoing
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------------------------
# Utility helpers
# ---------------------------
def add_log(text):
    st.session_state.log.insert(0, text)
    # keep log to reasonable length
    if len(st.session_state.log) > 50:
        st.session_state.log = st.session_state.log[:50]

def reset_battle():
    st.session_state.enemy_hp = None
    st.session_state.current_enemy = None
    st.session_state.battle_active = False

def restart_game():
    st.session_state.fruit = None
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = None
    st.session_state.current_enemy = None
    st.session_state.score = 0
    st.session_state.log = []
    st.session_state.battle_active = False
    add_log("Game restarted.")

# ---------------------------
# UI: Draw a fruit
# ---------------------------
st.header("1️⃣ Draw a Fruit")
col1, col2 = st.columns([2, 3])

with col1:
    if st.button("🔮 Random Fruit", key="draw_fruit"):
        st.session_state.fruit = random.choice(list(FRUITS.keys()))
        add_log(f"You obtained **{st.session_state.fruit}**!")
        # When drawing a new fruit, do not automatically reset score/HP;
        # but reset any active battle
        reset_battle()
        st.success(f"Fruit selected: {st.session_state.fruit}")

with col2:
    if st.session_state.fruit:
        fruit = FRUITS[st.session_state.fruit]
        st.markdown(f"**Current Fruit:**
