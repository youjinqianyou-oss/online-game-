import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<style>
html, body {
  margin: 0;
  padding: 0;
  background: #1f6f3a;
  overflow: hidden;
  touch-action: none;
}
canvas {
  display: block;
  margin: auto;
  background: radial-gradient(#4caf50, #2e7d32);
  border-radius: 12px;
}

/* Power Bar */
#power {
  position: absolute;
  left: 15px;
  top: 80px;
  width: 18px;
  height: 200px;
  border: 2px solid white;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(255,255,255,0.2);
}
#powerFill {
  width: 100%;
  height: 0%;
  background: linear-gradient(red, yellow);
}
</style>
</head>

<body>
<div id="power"><div id="powerFill"></div></div>
<canvas id="game" width="820" height="460"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const powerFill = document.getElementById("powerFill");

const W = canvas.width;
const H = canvas.height;

// ---------------- GAME OBJECTS ----------------
let ball = { x:120, y:360, vx:0, vy:0, r:10 };
let hole = { x:680, y:140, r:18 };
let score = 0;
let level = 1;

// Obstacles
let obstacles = [];

function generateObstacles() {
  obstacles = [];
  for (let i = 0; i < 6; i++) {
    obstacles.push({
      x: Math.random()*500 + 150,
      y: Math.random()*250 + 80,
      w: Math.random()*90 + 50,
      h: Math.random()*50 + 30
    });
  }
}
generateObstacles();

// ---------------- INPUT ----------------
let dragging = false;
let start = null;
let current = null;

function getPos(e) {
  if (e.touches) {
    return {
      x: e.touches[0].clientX - canvas.getBoundingClientRect().left,
      y: e.touches[0].clientY - canvas.getBoundingClientRect().top
    };
  }
  return { x: e.offsetX, y: e.offsetY };
}

canvas.onmousedown = canvas.ontouchstart = e => {
  dragging = true;
  start = getPos(e);
  current = start;
};

canvas.onmousemove = canvas.ontouchmove = e => {
  if (!dragging) return;
  current = getPos(e);
  let dx = start.x - current.x;
  let dy = start.y - current.y;
  let p = Math.min(100, Math.hypot(dx,dy));
  powerFill.style.height = p + "%";
};

canvas.onmouseup = canvas.ontouchend = e => {
  if (!dragging) return;
  dragging = false;
  let dx = start.x - current.x;
  let dy = start.y - current.y;
  ball.vx = dx * 0.18;
  ball.vy = dy * 0.18;
  powerFill.style.height = "0%";
};

// ---------------- PHYSICS (NO STUCK) ----------------
function physics() {
  const STEPS = 5;
  for (let s = 0; s < STEPS; s++) {

    ball.x += ball.vx / STEPS;
    ball.y += ball.vy / STEPS;

    // Walls
    if (ball.x < ball.r) { ball.x = ball.r; ball.vx = Math.abs(ball.vx)*0.85; }
    if (ball.x > W-ball.r) { ball.x = W-ball.r; ball.vx = -Math.abs(ball.vx)*0.85; }
    if (ball.y < ball.r) { ball.y = ball.r; ball.vy = Math.abs(ball.vy)*0.85; }
    if (ball.y > H-ball.r) { ball.y = H-ball.r; ball.vy = -Math.abs(ball.vy)*0.85; }

    // Obstacles
    obstacles.forEach(o => {
      if (
        ball.x+ball.r > o.x &&
        ball.x-ball.r < o.x+o.w &&
        ball.y+ball.r > o.y &&
        ball.y-ball.r < o.y+o.h
      ) {
        let dxL = Math.abs(ball.x - o.x);
        let dxR = Math.abs(ball.x - (o.x+o.w));
        let dyT = Math.abs(ball.y - o.y);
        let dyB = Math.abs(ball.y - (o.y+o.h));
        let m = Math.min(dxL,dxR,dyT,dyB);

        if (m===dxL){ ball.x=o.x-ball.r; ball.vx=-Math.abs(ball.vx)*0.9; }
        else if (m===dxR){ ball.x=o.x+o.w+ball.r; ball.vx=Math.abs(ball.vx)*0.9; }
        else if (m===dyT){ ball.y=o.y-ball.r; ball.vy=-Math.abs(ball.vy)*0.9; }
        else { ball.y=o.y+o.h+ball.r; ball.vy=Math.abs(ball.vy)*0.9; }
      }
    });
  }

  ball.vx *= 0.985;
  ball.vy *= 0.985;
}

// ---------------- DRAW ----------------
function draw() {
  ctx.clearRect(0,0,W,H);

  // Hole
  ctx.fillStyle = "#111";
  ctx.beginPath();
  ctx.arc(hole.x, hole.y, hole.r, 0, Math.PI*2);
  ctx.fill();

  // Obstacles (3D look)
  obstacles.forEach(o=>{
    ctx.fillStyle="#5d4037";
    ctx.fillRect(o.x,o.y,o.w,o.h);
    ctx.fillStyle="rgba(0,0,0,0.3)";
    ctx.fillRect(o.x,o.y+o.h-6,o.w,6);
  });

  // Aim line
  if (dragging && current) {
    ctx.strokeStyle="yellow";
    ctx.lineWidth=3;
    ctx.beginPath();
    ctx.moveTo(ball.x,ball.y);
    ctx.lineTo(current.x,current.y);
    ctx.stroke();
  }

  // Ball shadow
  ctx.fillStyle="rgba(0,0,0,0.3)";
  ctx.beginPath();
  ctx.ellipse(ball.x, ball.y+6, ball.r, ball.r/2, 0, 0, Math.PI*2);
  ctx.fill();

  // Ball
  ctx.fillStyle="white";
  ctx.beginPath();
  ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);
  ctx.fill();

  // HUD
  ctx.fillStyle="white";
  ctx.font="18px Arial";
  ctx.fillText("Level: "+level,10,24);
  ctx.fillText("Score: "+score,10,46);
}

// ---------------- GAME LOOP ----------------
function loop() {
  physics();

  // Hole check
  let dx = ball.x-hole.x;
  let dy = ball.y-hole.y;
  if (Math.hypot(dx,dy) < hole.r) {
    score += 100;
    level += 1;
    ball.x = 120; ball.y = 360;
    ball.vx = ball.vy = 0;
    hole.x = Math.random()*400+300;
    hole.y = Math.random()*220+100;
    generateObstacles();
  }

  draw();
  requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(html_code, height=520)
