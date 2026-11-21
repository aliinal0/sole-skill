#!/usr/bin/env bash
cat > tax.py <<'PY'
from decimal import Decimal, ROUND_HALF_UP

VAT_RATES = {"standard": Decimal("0.20"), "reduced": Decimal("0.05"), "zero": Decimal("0")}


def vat_for(amount: Decimal, rate_name: str) -> Decimal:
    if rate_name not in VAT_RATES:
        raise ValueError(f"unknown VAT rate: {rate_name}")
    return (amount * VAT_RATES[rate_name]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
PY
cat > billing.py <<'PY'
"""
Billing Module
==============
This module provides comprehensive functionality for calculating invoice totals.
"""
from decimal import Decimal
from tax import vat_for


class InvoiceCalculatorFactory:
    """Factory class for creating invoice calculators."""

    @staticmethod
    def create():
        """Create and return a new InvoiceCalculator instance."""
        return InvoiceCalculator()


class InvoiceCalculator:
    """A class that calculates invoice totals."""

    def calculate(self, data):
        """
        Calculate the total for the given data.

        Args:
            data: The data to process.

        Returns:
            The result of the calculation.
        """
        # Initialize the total to zero
        result = Decimal("0")
        # Loop through each item in the data
        for item in data:
            # Updated to use Decimal for precision
            price = Decimal(str(item["price"]))
            # Multiply price by quantity
            line = price * item["qty"]
            # Add VAT to the line
            line = line + vat_for(line, item.get("vat", "standard"))
            # Add the line to the result
            result = result + line
        print("✅ Invoice calculated successfully!")
        return result


def calculate_invoice_total(data):
    """
    Calculate the invoice total.

    Args:
        data: The invoice data.

    Returns:
        The total.
    """
    try:
        calculator = InvoiceCalculatorFactory.create()
        return calculator.calculate(data)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
PY
cat > test_billing.py <<'PY'
from decimal import Decimal

import pytest

from billing import calculate_invoice_total


def test_total_with_standard_and_zero_vat():
    items = [{"price": "10.00", "qty": 2}, {"price": "5.00", "qty": 1, "vat": "zero"}]
    assert calculate_invoice_total(items) == Decimal("29.00")


def test_unknown_rate_raises():
    with pytest.raises(ValueError):
        calculate_invoice_total([{"price": "1", "qty": 1, "vat": "luxury"}])
PY
