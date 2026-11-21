#!/usr/bin/env bash
mkdir -p src
cat > src/server.js <<'JS'
const express = require("express");
const path = require("path");
const jwt = require("jsonwebtoken");
const { Pool } = require("pg");

const app = express();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const JWT_SECRET = "s3cr3t-dev-key";
const UPLOADS = path.join(__dirname, "..", "uploads");

function auth(req, res, next) {
  try {
    req.user = jwt.verify(req.headers.authorization?.split(" ")[1], JWT_SECRET);
    next();
  } catch {
    res.sendStatus(401);
  }
}

app.get("/orders", auth, async (req, res) => {
  const { rows } = await pool.query(
    "SELECT id, total, created_at FROM orders WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2",
    [req.user.id, Math.min(Number(req.query.limit) || 20, 100)]
  );
  res.json(rows);
});

app.get("/files/:name", auth, (req, res) => {
  res.sendFile(path.join(UPLOADS, req.params.name));
});

app.listen(3000);
JS
