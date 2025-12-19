import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

<style>
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  background: #2f6f2f;
  touch-action: none;
}

#gameWrap {
  position: relative;
  width: 100vw;
  height: 100vh;
}

canvas {
  background: radial-gradient(circle at top, #4caf50, #1b5e20);
  display: block;
  margin: auto;
}

/* Power Bar */
#powerBarContainer {
  position: absolute;
  left: 12px;
  top: 80px;
  width: 18px;
  height: 180px;
  background: rgba(255,255,255,0.2);
  border: 2px solid white;
  border-radius: 10px;
  overflow: hidden;
}

#powerBarFill {
  width: 100%;
  height: 0%;
  background: linear-gradient(to top, #ff0000, #ffeb3b);
}
</style>
</head>

<body>
<div id="gameWrap">
  <div id="powerBarContainer">
    <div id="powerBarFill"></div>
  </div>
  <canvas id="game"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const powerBarFill = document.getElementById("powerBarFill");

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

// ---------- GAME STATE ----------
let ball = { x: 150, y: canvas.height-120, vx: 0, vy: 0, r: 12 };
let hole = { x: canvas.width-180, y: 180, r: 20 };
let score = 0;
let level = 1;

let dragging = false;
let dragStart = null;
let dragPos = null;

// ---------- OBSTACLES ----------
let obstacles = [];

function randomObstacles() {
  obstacles = [];
  for (let i = 0; i < 3 + level; i++) {
    obstacles.push({
      x: Math.random()*(canvas.width-300)+150,
      y: Math.random()*(canvas.height-300)+120,
      w: Math.random()*100+60,
      h: Math.random()*60+40
    });
  }
}
randomObstacles();

// ---------- INPUT ----------
function getPos(e) {
  if (e.touches) {
    return {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY
    };
  }
  return { x: e.clientX, y: e.clientY };
}

canvas.addEventListener("pointerdown", e => {
  dragging = true;
  dragStart = getPos(e);
  dragPos = dragStart;
});

canvas.addEventListener("pointermove", e => {
  if (!dragging) return;
  dragPos = getPos(e);
  let dx = dragStart.x - dragPos.x;
  let dy = dragStart.y - dragPos.y;
  let power = Math.min(100, Math.hypot(dx, dy));
  powerBarFill.style.height = power + "%";
});

canvas.addEventListener("pointerup", e => {
  if (!dragging) return;
  let pos = getPos(e);
  let dx = dragStart.x - pos.x;
  let dy = dragStart.y - pos.y;
  ball.vx = dx * 0.15;
  ball.vy = dy * 0.15;
  dragging = false;
  powerBarFill.style.height = "0%";
});

// ---------- PHYSICS ----------
function circleRectCollision(ball, rect) {
  let cx = Math.max(rect.x, Math.min(ball.x, rect.x+rect.w));
  let cy = Math.max(rect.y, Math.min(ball.y, rect.y+rect.h));
  let dx = ball.x - cx;
  let dy = ball.y - cy;
  return dx*dx + dy*dy < ball.r*ball.r;
}

// ---------- LOOP ----------
function loop() {
  ctx.clearRect(0,0,canvas.width,canvas.height);

  // Move
  ball.x += ball.vx;
  ball.y += ball.vy;
  ball.vx *= 0.985;
  ball.vy *= 0.985;

  // Wall bounce
  if (ball.x < ball.r) { ball.x = ball.r; ball.vx *= -0.8; }
  if (ball.x > canvas.width-ball.r) { ball.x = canvas.width-ball.r; ball.vx *= -0.8; }
  if (ball.y < ball.r) { ball.y = ball.r; ball.vy *= -0.8; }
  if (ball.y > canvas.height-ball.r) { ball.y = canvas.height-ball.r; ball.vy *= -0.8; }

  // Obstacles
  obstacles.forEach(o => {
    if (circleRectCollision(ball,o)) {
      let dx = ball.x - (o.x+o.w/2);
      let dy = ball.y - (o.y+o.h/2);
      if (Math.abs(dx) > Math.abs(dy)) ball.vx *= -0.9;
      else ball.vy *= -0.9;
    }
  });

  // Hole
  let hx = ball.x-hole.x;
  let hy = ball.y-hole.y;
  if (Math.hypot(hx,hy) < hole.r) {
    score += 100;
    level++;
    ball.x = 150;
    ball.y = canvas.height-120;
    ball.vx = ball.vy = 0;
    hole.x = Math.random()*(canvas.width-200)+150;
    hole.y = Math.random()*(canvas.height-200)+100;
    randomObstacles();
  }

  // Hole (3D)
  ctx.fillStyle = "#000";
  ctx.beginPath();
  ctx.arc(hole.x, hole.y, hole.r, 0, Math.PI*2);
  ctx.fill();

  // Obstacles (3D)
  obstacles.forEach(o => {
    ctx.fillStyle = "#5d4037";
    ctx.fillRect(o.x, o.y, o.w, o.h);
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.fillRect(o.x+4, o.y+4, o.w, o.h);
  });

  // Aim line
  if (dragging && dragPos) {
    ctx.setLineDash([8,6]);
    ctx.strokeStyle = "#ffeb3b";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(ball.x, ball.y);
    ctx.lineTo(dragPos.x, dragPos.y);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // Ball (3D)
  let g = ctx.createRadialGradient(ball.x-4, ball.y-4, 2, ball.x, ball.y, ball.r);
  g.addColorStop(0,"#fff");
  g.addColorStop(1,"#ccc");
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
  ctx.fill();

  // HUD
  ctx.fillStyle = "white";
  ctx.font = "20px Arial";
  ctx.fillText("Level: "+level, 12, 28);
  ctx.fillText("Score: "+score, 12, 54);

  requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(html_code, height=900)
