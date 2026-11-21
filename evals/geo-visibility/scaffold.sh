#!/usr/bin/env bash
cat > robots.txt <<'TXT'
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: *
Allow: /

Sitemap: https://ledgerleaf.example/sitemap.xml
TXT
cat > pricing.html <<'HTML'
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pricing - Ledgerleaf accounting for sole traders</title>
</head><body>
<h1>Pricing</h1>
<div id="plans"></div>
<script src="/plans.js"></script>
<h2>Is Ledgerleaf right for Irish sole traders?</h2>
<p>Running a business is a journey, and every journey needs the right companion. We built Ledgerleaf with care.</p>
<p>Ledgerleaf files your Form 11 return, tracks VAT at Irish rates and connects to AIB and Bank of Ireland.</p>
</body></html>
HTML
cat > plans.js <<'JS'
document.getElementById("plans").innerHTML =
  "<div><h3>Solo</h3><p>€12/month</p></div><div><h3>Solo + VAT</h3><p>€19/month</p></div>";
JS
