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
let level = 1;

let dragging = false;
let dragStart = null;
let dragPos = null;
let power = 0;

let obstacles = [
  {x:300, y:150, w:80, h:200},
  {x:550, y:100, w:60, h:250},
  {x:420, y:330, w:180, h:40},
];

function randomObstacles() {
  obstacles = [];
  for (let i = 0; i < 3; i++) {
    obstacles.push({
      x: Math.random()*600 + 150,
      y: Math.random()*300 + 80,
      w: Math.random()*100 + 50,
      h: Math.random()*80 + 30
    });
  }
}

// Mouse & Touch Events
function getPos(evt) {
  if (evt.touches) {
    return {
      x: evt.touches[0].clientX - canvas.offsetLeft,
      y: evt.touches[0].clientY - canvas.offsetTop
    };
  }
  return {x: evt.offsetX, y: evt.offsetY};
}

canvas.addEventListener("mousedown", e => { dragging = true; dragStart = getPos(e); dragPos = dragStart; });
canvas.addEventListener("mousemove", e => { if(dragging){ dragPos = getPos(e); let dx = dragStart.x - dragPos.x; let dy = dragStart.y - dragPos.y; power = Math.min(100, Math.sqrt(dx*dx + dy*dy)); powerBarFill.style.height = power + "%"; }});
canvas.addEventListener("mouseup", e => { if(!dragging) return; let pos = getPos(e); let dx = dragStart.x - pos.x; let dy = dragStart.y - pos.y; ball.vx = dx*0.2; ball.vy = dy*0.2; powerBarFill.style.height="0%"; dragging=false; dragPos=null; });

canvas.addEventListener("touchstart", e => { dragging = true; dragStart = getPos(e); dragPos = dragStart; });
canvas.addEventListener("touchmove", e => { if(dragging){ dragPos = getPos(e); let dx = dragStart.x - dragPos.x; let dy = dragStart.y - dragPos.y; power = Math.min(100, Math.sqrt(dx*dx + dy*dy)); powerBarFill.style.height = power + "%"; }});
canvas.addEventListener("touchend", e => { dragging=false; dragPos=null; powerBarFill.style.height="0%"; });

// Physics Loop
function loop() {
  ctx.clearRect(0,0,900,500);

  // Ball movement
  ball.x += ball.vx; ball.y += ball.vy;
  ball.vx *= 0.97; ball.vy *= 0.97;
  if(ball.x < ball.r || ball.x > 900-ball.r) ball.vx*=-0.7;
  if(ball.y < ball.r || ball.y > 500-ball.r) ball.vy*=-0.7;

  // Obstacles collision
  obstacles.forEach(o => {
    if(ball.x>o.x && ball.x<o.x+o.w && ball.y>o.y && ball.y<o.y+o.h){
      let left = Math.abs(ball.x - o.x);
      let right = Math.abs(ball.x - (o.x+o.w));
      let top = Math.abs(ball.y - o.y);
      let bottom = Math.abs(ball.y - (o.y+o.h));
      let m = Math.min(left,right,top,bottom);
      if(m===left){ ball.x=o.x-ball.r; ball.vx*=-0.8; }
      else if(m===right){ ball.x=o.x+o.w+ball.r; ball.vx*=-0.8; }
      else if(m===top){ ball.y=o.y-ball.r; ball.vy*=-0.8; }
      else{ ball.y=o.y+o.h+ball.r; ball.vy*=-0.8; }
    }
  });

  // Hole detection
  let dx = ball.x - hole.x; let dy = ball.y - hole.y;
  if(Math.sqrt(dx*dx + dy*dy) < hole.r){
    score+=100; level+=1;
    ball.x=150; ball.y=400; ball.vx=0; ball.vy=0;
    hole.x=Math.random()*600+200; hole.y=Math.random()*350+80;
    randomObstacles();
  }

  // Draw hole
  ctx.fillStyle="#222"; ctx.beginPath(); ctx.arc(hole.x,hole.y,hole.r,0,Math.PI*2); ctx.fill();
  // Draw obstacles
  ctx.fillStyle="#4b2e05"; obstacles.forEach(o=>ctx.fillRect(o.x,o.y,o.w,o.h));
  // Draw aiming line
  if(dragging && dragPos){ ctx.strokeStyle="yellow"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(ball.x,ball.y); ctx.lineTo(dragPos.x,dragPos.y); ctx.stroke(); }
  // Draw ball
  ctx.fillStyle="white"; ctx.beginPath(); ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2); ctx.fill();
  // HUD
  ctx.fillStyle="white"; ctx.font="22px Arial"; ctx.fillText("Level: "+level,10,25); ctx.fillText("Score: "+score,10,55);

  requestAnimationFrame(loop);
}

loop();
</script>
"""

components.html(html_code, height=520, width=920)
