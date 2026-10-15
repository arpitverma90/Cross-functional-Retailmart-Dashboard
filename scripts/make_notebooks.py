import json
import os

nb_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'project_documents', 'notebooks')
os.makedirs(nb_dir, exist_ok=True)

def create_nb(cells):
    return {
        'cells': cells,
        'metadata': {
            'language_info': {'name': 'python', 'version': '3.13.1'},
            'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
        },
        'nbformat': 4,
        'nbformat_minor': 5
    }

# 1. 01_profiling.ipynb
c1 = [
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['# RetailMart V3 - Notebook 01: Data Profiling\n', 'Comprehensive structural and statistical profiling of raw datasets across 16 schemas and 55 tables.']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'import os\n', 'import psycopg2\n', 'import pandas as pd\n', 'from dotenv import load_dotenv\n', 'load_dotenv()\n',
        'conn = psycopg2.connect(dbname="accio_retailmart_27", user="postgres", password="postgres", host="localhost", port="5432")\n',
        'print("Connected to accio_retailmart_27")'
    ]},
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['### 1. Table Counts and Grains Summary']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'query = """\n',
        'SELECT table_schema, count(*) as tables, sum(n_live_tup) as total_estimated_rows\n',
        'FROM pg_stat_user_tables\n',
        'WHERE table_schema NOT IN (\'analytics\')\n',
        'GROUP BY table_schema ORDER BY table_schema;\n',
        '"""\n',
        'df_summary = pd.read_sql(query, conn)\n',
        'df_summary'
    ]},
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['### 2. Commercial Orders & Revenue Profiling']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'query_orders = """\n',
        'SELECT order_status, count(*) as order_count, sum(net_total) as total_net_revenue, round(avg(net_total), 2) as aov\n',
        'FROM sales.orders\n',
        'GROUP BY order_status ORDER BY total_net_revenue DESC;\n',
        '"""\n',
        'df_orders = pd.read_sql(query_orders, conn)\n',
        'df_orders'
    ]}
]

# 2. 02_cleaning.ipynb
c2 = [
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['# RetailMart V3 - Notebook 02: Data Cleaning & Wrangling\n', 'Documentation of null handling rules, string trimming, boundary validation, and type standardization.']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'import psycopg2\n', 'import pandas as pd\n',
        'conn = psycopg2.connect(dbname="accio_retailmart_27", user="postgres", password="postgres", host="localhost", port="5432")\n',
        'print("Connected for cleaning validation")'
    ]},
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['### 1. Delivery Sequence Verification']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'query_seq = """\n',
        'SELECT count(*) as invalid_shipments\n',
        'FROM sales.shipments\n',
        'WHERE delivered_date < shipped_date;\n',
        '"""\n',
        'pd.read_sql(query_seq, conn)'
    ]},
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['### 2. Financial Boundary Checks']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'query_fin = """\n',
        'SELECT \n',
        '  count(CASE WHEN net_total < 0 THEN 1 END) as negative_orders,\n',
        '  count(CASE WHEN discount_amount > gross_total THEN 1 END) as excessive_discount\n',
        'FROM sales.orders;\n',
        '"""\n',
        'pd.read_sql(query_fin, conn)'
    ]}
]

# 3. 03_data_quality.ipynb
c3 = [
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['# RetailMart V3 - Notebook 03: 5-Pillar Data Quality Audit\n', 'Evaluating Completeness, Accuracy, Consistency, Timeliness, and Uniqueness.']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'import sys\n', 'import os\n', 'sys.path.append(os.path.abspath("../../scripts"))\n',
        'from verify_data_quality import run_dq_checks\n',
        'run_dq_checks()'
    ]}
]

# 4. 04_eda_catalogue.ipynb
c4 = [
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['# RetailMart V3 - Notebook 04: Exploratory Data Analysis (EDA) Catalog\n', 'Detailed business question analysis supporting Executive, Sales, Customer, Operations, and Cross-Functional dashboards.']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'import psycopg2\n', 'import pandas as pd\n', 'import matplotlib.pyplot as plt\n',
        'conn = psycopg2.connect(dbname="accio_retailmart_27", user="postgres", password="postgres", host="localhost", port="5432")\n',
        'print("Ready for EDA Analysis")'
    ]},
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['### EDA Question 1: Monthly Net Sales Velocity']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [
        'q1 = """\n',
        'SELECT \n',
        '    to_char(date_trunc(\'month\', order_date), \'YYYY-MM\') as yr_month,\n',
        '    count(*) as delivered_orders,\n',
        '    round(sum(net_total) / 10000000.0, 2) as net_revenue_crores,\n',
        '    round(avg(net_total), 2) as aov\n',
        'FROM sales.orders\n',
        'WHERE order_status = \'Delivered\'\n',
        'GROUP BY date_trunc(\'month\', order_date)\n',
        'ORDER BY yr_month;\n',
        '"""\n',
        'df_monthly = pd.read_sql(q1, conn)\n',
        'df_monthly'
    ]}
]

with open(os.path.join(nb_dir, '01_profiling.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(create_nb(c1), f, indent=2)

with open(os.path.join(nb_dir, '02_cleaning.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(create_nb(c2), f, indent=2)

with open(os.path.join(nb_dir, '03_data_quality.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(create_nb(c3), f, indent=2)

with open(os.path.join(nb_dir, '04_eda_catalogue.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(create_nb(c4), f, indent=2)

print('All 4 Jupyter notebooks successfully created.')
