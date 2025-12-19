import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html = """
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
#power {
  position: absolute;
  left: 10px;
  top: 60px;
  width: 18px;
  height: 180px;
  border: 2px solid white;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(255,255,255,0.25);
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
<canvas id="game"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const powerFill = document.getElementById("powerFill");

let W,H,scaleX,scaleY;
function resizeCanvas(){
  W = window.innerWidth;
  H = window.innerHeight;
  canvas.width = W*0.95;
  canvas.height = H*0.75;
  scaleX = canvas.width / 900;
  scaleY = canvas.height / 500;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// ---------------- GAME OBJECTS ----------------
let ball = { x:120*scaleX, y:360*scaleY, vx:0, vy:0, r:12*scaleX };
let hole = { x:760*scaleX, y:120*scaleY, r:18*scaleX };
let score = 0;
let level = 1;

// ---------------- WALLS ----------------
let walls = [];
function createWalls() {
  walls = [
    {x:225*scaleX,y:75*scaleY,w:40*scaleX,h:275*scaleY},
    {x:495*scaleX,y:40*scaleY,w:40*scaleX,h:225*scaleY},
    {x:630*scaleX,y:175*scaleY,w:225*scaleX,h:40*scaleY},
  ];
  for (let i=0;i<10;i++){
    walls.push({
      x: Math.random()*(canvas.width*0.6)+canvas.width*0.2,
      y: Math.random()*(canvas.height*0.5)+canvas.height*0.15,
      w: Math.random()*120*scaleX+40*scaleX,
      h: 24*scaleY
    });
  }
}
createWalls();

// ---------------- PARTICLES ----------------
let particles = [];
function createParticles(x,y){
  for(let i=0;i<20;i++){
    particles.push({
      x:x, y:y,
      vx:(Math.random()-0.5)*4,
      vy:(Math.random()-1.5)*4,
      alpha:1,
      r:Math.random()*3+2,
      color: `hsl(${Math.random()*360}, 100%, 70%)`
    });
  }
}
function drawParticles(){
  particles.forEach((p,i)=>{
    p.x+=p.vx;
    p.y+=p.vy;
    p.alpha-=0.03;
    if(p.alpha<=0){ particles.splice(i,1); return; }
    ctx.fillStyle = `rgba(${p.color.match(/\\d+/g).join(",")},${p.alpha})`;
    ctx.beginPath();
    ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fill();
  });
}

// ---------------- INPUT ----------------
let dragging=false;
let start=null;
let cur=null;

function pos(e){
  const r = canvas.getBoundingClientRect();
  if(e.touches){
    return {x:e.touches[0].clientX-r.left,y:e.touches[0].clientY-r.top};
  }
  return {x:e.offsetX,y:e.offsetY};
}

canvas.onmousedown = canvas.ontouchstart = e=>{
  dragging=true;
  start=pos(e);
  cur=start;
};

canvas.onmousemove = canvas.ontouchmove = e=>{
  if(!dragging) return;
  cur=pos(e);
  let dx=start.x-cur.x;
  let dy=start.y-cur.y;
  powerFill.style.height = Math.min(100,Math.hypot(dx,dy))+"%";
};

canvas.onmouseup = canvas.ontouchend = ()=>{
  if(!dragging) return;
  dragging=false;
  let dx=start.x-cur.x;
  let dy=start.y-cur.y;
  ball.vx=dx*0.18;
  ball.vy=dy*0.18;
  powerFill.style.height="0%";
};

// ---------------- COLLISION ----------------
function collideWall(w){
  if(
    ball.x+ball.r > w.x &&
    ball.x-ball.r < w.x+w.w &&
    ball.y+ball.r > w.y &&
    ball.y-ball.r < w.y+w.h
  ){
    let dl=Math.abs(ball.x-(w.x));
    let dr=Math.abs(ball.x-(w.x+w.w));
    let dt=Math.abs(ball.y-(w.y));
    let db=Math.abs(ball.y-(w.y+w.h));
    let m=Math.min(dl,dr,dt,db);
    if(m===dl){ ball.x=w.x-ball.r; ball.vx=-Math.abs(ball.vx); }
    else if(m===dr){ ball.x=w.x+w.w+ball.r; ball.vx=Math.abs(ball.vx); }
    else if(m===dt){ ball.y=w.y-ball.r; ball.vy=-Math.abs(ball.vy); }
    else{ ball.y=w.y+w.h+ball.r; ball.vy=Math.abs(ball.vy); }
  }
}

// ---------------- PHYSICS ----------------
function physics(){
  const STEPS=6;
  for(let i=0;i<STEPS;i++){
    ball.x+=ball.vx/STEPS;
    ball.y+=ball.vy/STEPS;

    if(ball.x<ball.r){ball.x=ball.r;ball.vx=Math.abs(ball.vx);}
    if(ball.x>canvas.width-ball.r){ball.x=canvas.width-ball.r;ball.vx=-Math.abs(ball.vx);}
    if(ball.y<ball.r){ball.y=ball.r;ball.vy=Math.abs(ball.vy);}
    if(ball.y>canvas.height-ball.r){ball.y=canvas.height-ball.r;ball.vy=-Math.abs(ball.vy);}

    walls.forEach(collideWall);
  }
  ball.vx*=0.985;
  ball.vy*=0.985;
}

// ---------------- DRAW ----------------
function draw(){
  ctx.clearRect(0,0,canvas.width,canvas.height);

  ctx.fillStyle="#111";
  ctx.beginPath();
  ctx.arc(hole.x,hole.y,hole.r,0,Math.PI*2);
  ctx.fill();

  walls.forEach(w=>{
    let grad=ctx.createLinearGradient(w.x,w.y,w.x+w.w,w.y+w.h);
    grad.addColorStop(0,"#795548");
    grad.addColorStop(1,"#3e2723");
    ctx.fillStyle=grad;
    ctx.fillRect(w.x,w.y,w.w,w.h);
  });

  if(dragging){
    ctx.strokeStyle="yellow";
    ctx.lineWidth=3;
    ctx.beginPath();
    ctx.moveTo(ball.x,ball.y);
    ctx.lineTo(cur.x,cur.y);
    ctx.stroke();
  }

  drawParticles();

  // 球影
  ctx.fillStyle="rgba(0,0,0,0.35)";
  ctx.beginPath();
  ctx.ellipse(ball.x,ball.y+6,ball.r,ball.r/2,0,0,Math.PI*2);
  ctx.fill();

  // 球
  let ballGrad=ctx.createRadialGradient(ball.x-3,ball.y-3,ball.r/4,ball.x,ball.y,ball.r);
  ballGrad.addColorStop(0,"#fff");
  ballGrad.addColorStop(1,"#ddd");
  ctx.fillStyle=ballGrad;
  ctx.beginPath();
  ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);
  ctx.fill();

  ctx.fillStyle="white";
  ctx.font="18px Arial";
  ctx.fillText("Level "+level,10,22);
  ctx.fillText("Score "+score,10,42);
}

// ---------------- LOOP ----------------
function loop(){
  physics();

  let dx=ball.x-hole.x;
  let dy=ball.y-hole.y;
  if(Math.hypot(dx,dy)<hole.r){
    score+=100;
    level++;
    ball.x=120*scaleX; ball.y=360*scaleY;
    ball.vx=ball.vy=0;
    hole.x=(Math.random()*0.4+0.5)*canvas.width;
    hole.y=(Math.random()*0.5+0.15)*canvas.height;
    createWalls();
    createParticles(hole.x,hole.y); // 進洞粒子
  }

  draw();
  requestAnimationFrame(loop);
}
loop();
</script>
</body>
</html>
"""

components.html(html, height=700)
