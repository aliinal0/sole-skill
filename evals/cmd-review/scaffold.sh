#!/usr/bin/env bash
cat > README.md <<'MD'
# Shop backend

Order totals and order lookups for our small online shop. One web process, a few hundred orders a day.

Free shipping on orders of £50 or more; otherwise shipping is £4.95.
MD
cat > orders.py <<'PY'
from decimal import Decimal

FREE_SHIPPING_OVER = Decimal("50")


class ShippingPolicyFactory:
    @staticmethod
    def create():
        return StandardShippingPolicy()


class StandardShippingPolicy:
    def cost(self, subtotal):
        if subtotal > FREE_SHIPPING_OVER:
            return Decimal("0")
        return Decimal("4.95")


def order_total(items):
    subtotal = sum(Decimal(str(i["price"])) * i["qty"] for i in items)
    policy = ShippingPolicyFactory.create()
    return subtotal + policy.cost(subtotal)


def find_orders(db, customer_email):
    cur = db.execute(f"SELECT id, total FROM orders WHERE email = '{customer_email}'")
    return cur.fetchall()


def refund(db, order_id, amount):
    total = db.execute("SELECT total FROM orders WHERE id = ?", (order_id,)).fetchone()[0]
    db.execute("UPDATE orders SET total = ? WHERE id = ?", (total - amount, order_id))
PY
cat > test_orders.py <<'PY'
from decimal import Decimal
from orders import order_total


def test_small_order_pays_shipping():
    assert order_total([{"price": "10.00", "qty": 2}]) == Decimal("24.95")
PY
cat > change.diff <<'DIFF'
--- a/orders.py
+++ b/orders.py
@@ -1,9 +1,36 @@
 from decimal import Decimal

+FREE_SHIPPING_OVER = Decimal("50")
+
+
+class ShippingPolicyFactory:
+    @staticmethod
+    def create():
+        return StandardShippingPolicy()
+
+
+class StandardShippingPolicy:
+    def cost(self, subtotal):
+        if subtotal > FREE_SHIPPING_OVER:
+            return Decimal("0")
+        return Decimal("4.95")
+

 def order_total(items):
-    return sum(Decimal(str(i["price"])) * i["qty"] for i in items) + Decimal("4.95")
+    subtotal = sum(Decimal(str(i["price"])) * i["qty"] for i in items)
+    policy = ShippingPolicyFactory.create()
+    return subtotal + policy.cost(subtotal)
+
+
+def find_orders(db, customer_email):
+    cur = db.execute(f"SELECT id, total FROM orders WHERE email = '{customer_email}'")
+    return cur.fetchall()
+
+
+def refund(db, order_id, amount):
+    total = db.execute("SELECT total FROM orders WHERE id = ?", (order_id,)).fetchone()[0]
+    db.execute("UPDATE orders SET total = ? WHERE id = ?", (total - amount, order_id))
DIFF
