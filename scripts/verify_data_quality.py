#!/usr/bin/env python3
"""
RetailMart V3 - Data Quality Framework
Evaluates the 5 Pillars of Enterprise Data Quality on PostgreSQL:
1. Completeness  2. Accuracy  3. Consistency  4. Timeliness  5. Uniqueness
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "accio_retailmart_27")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


def run_dq_checks():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    
    print("=" * 80)
    print("RETAILMART V3 - 5-PILLAR ENTERPRISE DATA QUALITY AUDIT")
    print("=" * 80)
    
    total_checks = 0
    passed_checks = 0
    
    # Pillar 1: Completeness
    print("\n[PILLAR 1: COMPLETENESS]")
    completeness_tests = [
        ("sales.orders", "cust_id IS NULL", "Orders without Customer ID"),
        ("sales.orders", "order_date IS NULL", "Orders without Order Date"),
        ("sales.orders", "net_total IS NULL", "Orders without Net Total"),
        ("sales.order_items", "prod_id IS NULL", "Order items without Product ID"),
        ("customers.customers", "email IS NULL", "Customers without Email"),
        ("products.products", "price IS NULL", "Products without Price"),
    ]
    for tbl, cond, desc in completeness_tests:
        total_checks += 1
        cur.execute(f"SELECT count(*) FROM {tbl} WHERE {cond};")
        fail_cnt = cur.fetchone()[0]
        status = "[PASSED]" if fail_cnt == 0 else "[FAILED]"
        if fail_cnt == 0:
            passed_checks += 1
        print(f"  {status} {desc:<42} | Failures: {fail_cnt}")

    # Pillar 2: Accuracy & Range Validity
    print("\n[PILLAR 2: ACCURACY & DOMAIN VALIDITY]")
    accuracy_tests = [
        ("sales.orders", "net_total < 0", "Negative Order Net Total"),
        ("sales.orders", "discount_amount < 0", "Negative Order Discount"),
        ("sales.order_items", "quantity <= 0", "Non-positive Order Item Quantity"),
        ("sales.order_items", "unit_price < 0", "Negative Unit Price"),
        ("products.products", "cost_price < 0", "Negative Product Cost"),
        ("sales.shipments", "delivered_date < shipped_date", "Delivery Date Precedes Shipped Date"),
        ("manufacture.work_orders", "rejected_quantity > quantity_produced", "Rejected Quantity Exceeds Produced"),
        ("products.inventory", "quantity_on_hand < 0", "Negative Store Inventory"),
    ]
    for tbl, cond, desc in accuracy_tests:
        total_checks += 1
        cur.execute(f"SELECT count(*) FROM {tbl} WHERE {cond};")
        fail_cnt = cur.fetchone()[0]
        status = "[PASSED]" if fail_cnt == 0 else "[FAILED]"
        if fail_cnt == 0:
            passed_checks += 1
        print(f"  {status} {desc:<42} | Failures: {fail_cnt}")

    # Pillar 3: Consistency & Cross-Table Reconciliation
    print("\n[PILLAR 3: CONSISTENCY & RECONCILIATION]")
    # Check Delivered Net Total reconciliation between orders and order_items
    cur.execute("""
        SELECT 
            (SELECT SUM(net_total) FROM sales.orders WHERE order_status = 'Delivered') AS order_sum,
            (SELECT SUM(oi.net_amount) 
             FROM sales.order_items oi 
             JOIN sales.orders o ON oi.order_id = o.order_id 
             WHERE o.order_status = 'Delivered') AS item_sum;
    """)
    ord_sum, itm_sum = cur.fetchone()
    diff = abs(ord_sum - itm_sum)
    total_checks += 1
    status = "[PASSED]" if diff < 0.01 else "[FAILED]"
    if diff < 0.01:
        passed_checks += 1
    print(f"  {status} {'Delivered Revenue: Orders vs Order Items':<42} | Diff: Rs. {diff:,.2f}")

    # Orphan checks across core relations
    orphan_tests = [
        ("sales.orders c LEFT JOIN customers.customers p ON c.cust_id = p.customer_id WHERE p.customer_id IS NULL", "Orphan Orders (Invalid Customer)"),
        ("sales.order_items c LEFT JOIN sales.orders p ON c.order_id = p.order_id WHERE p.order_id IS NULL", "Orphan Order Items (Invalid Order)"),
        ("sales.shipments c LEFT JOIN sales.orders p ON c.order_id = p.order_id WHERE p.order_id IS NULL", "Orphan Shipments (Invalid Order)"),
        ("sales.returns c LEFT JOIN sales.orders p ON c.order_id = p.order_id WHERE p.order_id IS NULL", "Orphan Returns (Invalid Order)"),
    ]
    for cond, desc in orphan_tests:
        total_checks += 1
        cur.execute(f"SELECT count(*) FROM {cond};")
        fail_cnt = cur.fetchone()[0]
        status = "[PASSED]" if fail_cnt == 0 else "[FAILED]"
        if fail_cnt == 0:
            passed_checks += 1
        print(f"  {status} {desc:<42} | Failures: {fail_cnt}")

    # Pillar 4: Timeliness
    print("\n[PILLAR 4: TIMELINESS & CALENDAR BOUNDARIES]")
    cur.execute("SELECT min(order_date), max(order_date) FROM sales.orders;")
    min_date, max_date = cur.fetchone()
    total_checks += 1
    timely = (str(min_date) == "2024-01-01" and str(max_date) == "2026-02-26")
    status = "[PASSED]" if timely else "[FAILED]"
    if timely:
        passed_checks += 1
    print(f"  {status} {'Orders Date Range Boundary [2024-01-01..2026-02-26]':<42} | Observed: {min_date} to {max_date}")

    # Pillar 5: Uniqueness
    print("\n[PILLAR 5: UNIQUENESS & PRIMARY KEY INTEGRITY]")
    unique_tests = [
        ("sales.orders", "order_id", "Unique Orders PK"),
        ("sales.order_items", "order_item_id", "Unique Order Items PK"),
        ("customers.customers", "customer_id", "Unique Customers PK"),
        ("products.products", "product_id", "Unique Products PK"),
        ("stores.stores", "store_id", "Unique Stores PK"),
        ("sales.shipments", "shipment_id", "Unique Shipments PK"),
        ("sales.returns", "return_id", "Unique Returns PK"),
    ]
    for tbl, pk, desc in unique_tests:
        total_checks += 1
        cur.execute(f"SELECT count(*) - count(DISTINCT {pk}) FROM {tbl};")
        dup_cnt = cur.fetchone()[0]
        status = "[PASSED]" if dup_cnt == 0 else "[FAILED]"
        if dup_cnt == 0:
            passed_checks += 1
        print(f"  {status} {desc:<42} | Duplicate PKs: {dup_cnt}")

    print("\n" + "=" * 80)
    print(f"DATA QUALITY AUDIT SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED ({(passed_checks/total_checks)*100:.1f}%)")
    print("=" * 80)
    
    cur.close()
    conn.close()
    return passed_checks == total_checks


if __name__ == "__main__":
    ok = run_dq_checks()
    sys.exit(0 if ok else 1)
