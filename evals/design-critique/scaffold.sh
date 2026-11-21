#!/usr/bin/env bash
cat > index.html <<'HTML'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Hilltop Roasters - Coffee</title>
<style>
body{font-family:Inter,sans-serif;background:#0b0b12;color:#fff;margin:0}
.eyebrow{text-transform:uppercase;letter-spacing:.2em;font-size:12px;color:#a78bfa}
h1{font-size:64px;background:linear-gradient(90deg,#6366f1,#a855f7);-webkit-background-clip:text;color:transparent}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.card{border-radius:24px;border:1px solid rgba(255,255,255,.1);box-shadow:0 20px 60px rgba(0,0,0,.4);padding:32px}
.glass{backdrop-filter:blur(20px);background:rgba(255,255,255,.06)}
.num{font-family:monospace;color:#a78bfa}
</style></head>
<body>
<section class="hero"><p class="eyebrow">Specialty coffee</p><h1>Elevate your mornings</h1><p>Unlock the perfect cup.</p><a href="#">Get started &rarr;</a></section>
<section><p class="eyebrow">Why us</p><h2>Features</h2>
<div class="cards">
<div class="card glass"><span class="num">01</span><div>&#9749;</div><h3>Fresh beans</h3><p>Seamless freshness.</p></div>
<div class="card"><span class="num">02</span><div>&#127793;</div><h3>Ethical</h3><p>Robust sourcing.</p></div>
<div class="card"><span class="num">03</span><div>&#128666;</div><h3>Fast delivery</h3><p>Next-level speed.</p></div>
</div></section>
<section><p class="eyebrow">Testimonials</p><h2>Loved by thousands</h2></section>
</body></html>
HTML
