#!/usr/bin/env bash
cat > product.html <<'HTML'
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Ethiopia Yirgacheffe Coffee Beans 250 g | Hilltop Roasters</title>
<meta name="description" content="Ethiopia Yirgacheffe, light roast, floral and lemony notes. 250 g of freshly roasted beans.">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product","name":"Ethiopia Yirgacheffe 250 g","image":"https://hilltoproasters.example/img/yirgacheffe.jpg",
 "offers":{"@type":"Offer","price":"12.50","priceCurrency":"GBP"},
 "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"1240"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HowTo","name":"How to brew with a V60","step":[{"@type":"HowToStep","text":"Grind 15 g of coffee medium-fine."},{"@type":"HowToStep","text":"Brew with 250 ml of water at 93 C."}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How long does delivery take?","acceptedAnswer":{"@type":"Answer","text":"1-3 working days."}}]}
</script>
</head><body>
<h1>Ethiopia Yirgacheffe 250 g</h1>
<p>Light roast. Floral, bergamot and lemon notes. The roast date is printed on every bag.</p>
<p><strong>£12.50</strong> <button>Add to basket</button></p>
<h2>Brewing with a V60</h2><ol><li>Grind 15 g of coffee medium-fine.</li><li>Brew with 250 ml of water at 93 C.</li></ol>
<h2>Questions</h2><p><b>How long does delivery take?</b> 1-3 working days.</p>
</body></html>
HTML
