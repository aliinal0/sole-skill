#!/usr/bin/env bash
mkdir -p src/routes src/services src/db src/jobs test
cat > package.json <<'JSON'
{
  "name": "parcelpost-api",
  "version": "1.4.0",
  "scripts": { "start": "node src/server.js", "worker": "node src/jobs/worker.js", "test": "node --test" },
  "dependencies": { "express": "^4.19.0", "pg": "^8.11.0", "stripe": "^14.0.0", "bullmq": "^5.0.0" }
}
JSON
cat > src/server.js <<'JS'
const express = require("express");
const shipments = require("./routes/shipments");
const webhooks = require("./routes/webhooks");

const app = express();
app.use("/webhooks", express.raw({ type: "application/json" }), webhooks);
app.use(express.json());
app.use("/shipments", shipments);
app.listen(process.env.PORT || 3000);
JS
cat > src/routes/shipments.js <<'JS'
const router = require("express").Router();
const { quote } = require("../services/pricing");
const db = require("../db");
const queue = require("../queue");

router.post("/", async (req, res) => {
  const price = quote(req.body.weightKg, req.body.zone);
  const shipment = await db.insertShipment({ ...req.body, price });
  await queue.add("label", { shipmentId: shipment.id });
  res.status(201).json(shipment);
});

module.exports = router;
JS
cat > src/routes/webhooks.js <<'JS'
const router = require("express").Router();
const stripe = require("stripe")(process.env.STRIPE_KEY);
const db = require("../db");

router.post("/stripe", async (req, res) => {
  const event = stripe.webhooks.constructEvent(req.body, req.headers["stripe-signature"], process.env.STRIPE_WEBHOOK_SECRET);
  if (event.type === "payment_intent.succeeded") await db.markPaid(event.data.object.metadata.shipmentId);
  res.sendStatus(200);
});

module.exports = router;
JS
cat > src/services/pricing.js <<'JS'
const ZONES = { uk: 3.2, eu: 7.5, world: 14 };

function quote(weightKg, zone) {
  if (!ZONES[zone]) throw new Error(`unknown zone ${zone}`);
  return Math.round((ZONES[zone] + weightKg * 1.1) * 100) / 100;
}

module.exports = { quote };
JS
cat > src/services/labels.js <<'JS'
async function generate(shipment) {
  // calls the carrier's label API; returns a PDF URL
  return `https://labels.example/${shipment.id}.pdf`;
}
module.exports = { generate };
JS
cat > src/db/index.js <<'JS'
const { Pool } = require("pg");
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function insertShipment(s) {
  const { rows } = await pool.query(
    "INSERT INTO shipments (weight_kg, zone, price) VALUES ($1, $2, $3) RETURNING *", [s.weightKg, s.zone, s.price]);
  return rows[0];
}
async function markPaid(id) { await pool.query("UPDATE shipments SET paid = true WHERE id = $1", [id]); }
async function attachLabel(id, url) { await pool.query("UPDATE shipments SET label_url = $2 WHERE id = $1", [id, url]); }
async function getShipment(id) { const { rows } = await pool.query("SELECT * FROM shipments WHERE id = $1", [id]); return rows[0]; }

module.exports = { insertShipment, markPaid, attachLabel, getShipment };
JS
cat > src/queue.js <<'JS'
const { Queue } = require("bullmq");
module.exports = new Queue("shipments", { connection: { url: process.env.REDIS_URL } });
JS
cat > src/jobs/worker.js <<'JS'
const { Worker } = require("bullmq");
const labels = require("../services/labels");
const db = require("../db");

new Worker("shipments", async (job) => {
  if (job.name !== "label") return;
  const shipment = await db.getShipment(job.data.shipmentId);
  const url = await labels.generate(shipment);
  await db.attachLabel(shipment.id, url);
}, { connection: { url: process.env.REDIS_URL } });
JS
cat > test/pricing.test.js <<'JS'
const test = require("node:test");
const assert = require("node:assert");
const { quote } = require("../src/services/pricing");
test("uk quote", () => assert.strictEqual(quote(2, "uk"), 5.4));
JS
