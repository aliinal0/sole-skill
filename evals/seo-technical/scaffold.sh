#!/usr/bin/env bash
mkdir -p products
cat > robots.txt <<'TXT'
User-agent: *
Disallow: /products/
Disallow: /cart
TXT
cat > sitemap.xml <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://steepandco.example/</loc><lastmod>2026-11-20</lastmod></url>
  <url><loc>https://steepandco.example/products/kettle.html</loc><lastmod>2026-11-20</lastmod></url>
  <url><loc>https://steepandco.example/products/teapot.html</loc><lastmod>2026-11-20</lastmod></url>
  <url><loc>https://steepandco.example/about.html</loc><lastmod>2026-11-20</lastmod></url>
  <url><loc>https://steepandco.example/thank-you.html</loc><lastmod>2026-11-20</lastmod></url>
</urlset>
XML
cat > index.html <<'HTML'
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Steep &amp; Co - loose-leaf tea from Bristol</title>
<meta name="description" content="Loose-leaf tea, teapots and kettles, packed in Bristol.">
<link rel="canonical" href="https://steepandco.example/">
</head><body>
<img src="/img/hero.jpg" loading="lazy" alt="" width="1600" height="900">
<h1>Loose-leaf tea, packed in Bristol</h1>
<a href="/products/kettle.html">Kettles</a> <a href="/products/teapot.html">Teapots</a> <a href="/about.html">About</a>
</body></html>
HTML
cat > products/kettle.html <<'HTML'
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Products | Steep &amp; Co</title>
<link rel="canonical" href="https://steepandco.example/">
</head><body><h1>Gooseneck kettle, 1 litre</h1><p>Temperature control from 40 to 100 °C.</p></body></html>
HTML
cat > products/teapot.html <<'HTML'
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Products | Steep &amp; Co</title>
<link rel="canonical" href="https://steepandco.example/products/teapot.html">
</head><body><h1>Glass teapot, 600 ml</h1><p>Borosilicate glass with a steel infuser.</p></body></html>
HTML
cat > about.html <<'HTML'
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>About Steep &amp; Co</title>
<link rel="canonical" href="https://steepandco.example/about.html">
</head><body><h1>About us</h1><p>We started packing tea in a Bristol garage in 2019.</p></body></html>
HTML
cat > thank-you.html <<'HTML'
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Thanks for your order</title>
</head><body><h1>Thank you</h1></body></html>
HTML
