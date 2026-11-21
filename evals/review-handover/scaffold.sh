#!/usr/bin/env bash
cat > brief.md <<'MD'
# Brief: Hearth & Crumb landing page
- Headline must mention free delivery on orders over £40.
- Phone number on the page: 0117 496 0123.
- Opening hours: Tue-Sat 7:00-15:00.
- Real photos only (we will send them); no stock photos.
- The order button goes to https://order.hearthandcrumb.co.uk
MD
cat > landing.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hearth &amp; Crumb</title>
</head>
<body>
  <header>
    <h1>Unlock the taste of real sourdough — free delivery over £35</h1>
    <a class="button" href="#">Order now</a>
  </header>
  <img src="https://images.unsplash.com/photo-1509440159596-0249088772ff?w=1600">
  <section>
    <h2>Visit us</h2>
    <p>12 Gloucester Road, Bristol</p>
    <p>Open Tue–Sun 7:00–15:00</p>
    <p>Call 0117 496 0132</p>
  </section>
  <script>console.log("debug: hero loaded");</script>
</body>
</html>
HTML
