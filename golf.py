import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components

html_code = """
<style>
  body { margin: 0; overflow: hidden; }
  canvas { background: #3A8F3A; display: block; margin: auto; }

  /* Power Bar */
  #powerBarContainer {
    position: absolute;
    left: 20px;
    top: 100px;
    width: 20px;
    height: 200px;
    background: rgba(255,255,255,0.2);
    border: 2px solid white;
    border-radius: 10px;
    overflow: hidden;
  }

  #powerBarFill {
    width: 100%;
    height: 0%;
    background: red;
    transition: height 0.05s;
  }
</style>

<div id="powerBarContainer">
  <div id="powerBarFill"></div>
</div>

<canvas id="game" width="900" height="500"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const powerBarFill = document.getElementById("powerBarFill");

// Game state
let ball = {x:150, y:400, vx:0, vy:0, r:10};
let hole = {x:700, y:200, r:18};
let score = 0;
let level =
