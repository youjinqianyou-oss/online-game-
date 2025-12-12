import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<style>
  body { margin:0; overflow:hidden; }
  canvas { background:#3A8F3A; display:block; margin:auto; }
</style>

<canvas id="game" width="900" height="500"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// simple demo: white ball
ctx.fillStyle = "white";
ctx.beginPath();
ctx.arc(150, 400, 10, 0, Math.PI*2);
ctx.fill();
</script>
"""

components.html(html_code, height=520, width=920)
