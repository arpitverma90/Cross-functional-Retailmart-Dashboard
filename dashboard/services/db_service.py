import time
import logging
from decimal import Decimal
from datetime import date, datetime
from django.db import connection

logger = logging.getLogger('analytics.db')

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict, serializing Decimals and Dates."""
    columns = [col[0] for col in cursor.description]
    results = []
    for row in cursor.fetchall():
        row_dict = {}
        for col, val in zip(columns, row):
            if isinstance(val, Decimal):
                row_dict[col] = float(val)
            elif isinstance(val, (date, datetime)):
                row_dict[col] = val.isoformat()
            else:
                row_dict[col] = val
        results.append(row_dict)
    return results


def execute_query(sql_query, params=None):
    """Execute a parameterized query and return list of dicts with latency logging."""
    start_time = time.perf_counter()
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params or [])
        data = dictfetchall(cursor)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    if elapsed_ms > 250:
        logger.warning(f"SLOW QUERY ({elapsed_ms:.1f}ms): {sql_query[:100]}... params={params}")
    else:
        logger.debug(f"Query ({elapsed_ms:.1f}ms): {sql_query[:80]}...")
    return data


def execute_one(sql_query, params=None):
    """Execute a parameterized query and return the first row as a dict."""
    rows = execute_query(sql_query, params)
    return rows[0] if rows else {}


def execute_scalar(sql_query, params=None, default=None):
    """Execute a parameterized query returning a single scalar value."""
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params or [])
        row = cursor.fetchone()
        if not row or row[0] is None:
            return default
        val = row[0]
        if isinstance(val, Decimal):
            return float(val)
        return val
