#!/usr/bin/env bash
cat > app.py <<'PY'
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DB = "shop.db"

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
    return g.db

def current_user_id():
    # session handling elided: returns the logged-in user's id
    return int(request.headers.get("X-User-Id", "0"))

@app.route("/search")
def search():
    q = request.args.get("q", "")
    rows = db().execute(f"SELECT id, name, price FROM products WHERE name LIKE '%{q}%'").fetchall()
    return jsonify(rows)

@app.route("/invoices/<int:invoice_id>")
def invoice(invoice_id):
    if current_user_id() == 0:
        return "login required", 401
    row = db().execute("SELECT id, owner_id, total, address FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    if row is None:
        return "not found", 404
    return jsonify({"id": row[0], "total": row[2], "address": row[3]})
PY
