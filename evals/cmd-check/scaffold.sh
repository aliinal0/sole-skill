#!/usr/bin/env bash
cat > index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Steep &amp; Co</title>
  <style>
    .wrap { width: 1200px; margin: 0 auto; }
    .hero img { display: block; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero"><img src="hero-4000px.jpg" alt="Loose-leaf tea in a glass pot"></div>
    <h1>Loose-leaf tea, packed in Bristol</h1>
  </div>
  <script src="app.js"></script>
</body>
</html>
HTML
