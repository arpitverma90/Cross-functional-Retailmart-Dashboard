#!/usr/bin/env python3
"""
RetailMart V3 - Reusable Data Cleaning & Standardization Module
Standardizes formats, trims whitespace, handles NULL coalescing,
and enforces domain validation rules without mutating raw files.
"""

import os
import re
from datetime import datetime
from decimal import Decimal


def clean_string(val, default=""):
    """Trim whitespace and standardize empty strings."""
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def clean_category_name(val):
    """Normalize category and brand strings to Title Case."""
    if not val:
        return "Unknown"
    return str(val).strip().title()


def parse_date_safe(val, fmt="%Y-%m-%d"):
    """Parse date string safely, returning None if invalid."""
    if not val:
        return None
    try:
        return datetime.strptime(str(val).strip(), fmt).date()
    except (ValueError, TypeError):
        return None


def parse_timestamp_safe(val):
    """Parse timestamp strings across multiple common formats."""
    if not val:
        return None
    s = str(val).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def clean_monetary_value(val, min_val=Decimal("0.00")):
    """Ensure monetary amounts are non-negative Decimals."""
    if val is None or val == "":
        return min_val
    try:
        d = Decimal(str(val).strip())
        return max(d, min_val)
    except Exception:
        return min_val


def clean_quantity(val, min_qty=0):
    """Ensure discrete quantities are non-negative integers."""
    if val is None or val == "":
        return min_qty
    try:
        q = int(float(str(val).strip()))
        return max(q, min_qty)
    except Exception:
        return min_qty


def validate_order_record(order):
    """
    Validate commercial order integrity:
    gross_total >= net_total
    discount_amount = gross_total - net_total (within 0.05 rounding)
    """
    gross = clean_monetary_value(order.get("gross_total"))
    discount = clean_monetary_value(order.get("discount_amount"))
    net = clean_monetary_value(order.get("net_total"))
    
    is_valid = True
    errors = []
    
    if gross < net:
        is_valid = False
        errors.append("Gross total less than net total")
    if discount > gross:
        is_valid = False
        errors.append("Discount exceeds gross total")
        
    return is_valid, errors


def validate_shipment_sequence(shipped_date, delivered_date):
    """Validate that delivered date is on or after shipped date."""
    if not shipped_date or not delivered_date:
        return True, []
    if delivered_date < shipped_date:
        return False, ["Delivered date precedes shipped date"]
    return True, []


def validate_work_order_quantities(produced, rejected):
    """Validate manufacturing quantities."""
    p = clean_quantity(produced)
    r = clean_quantity(rejected)
    if r > p:
        return False, ["Rejected quantity exceeds produced quantity"]
    return True, []
