import os
import sys
import unittest
import django

# Setup django settings if not already configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

class ServiceIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.default_filters = {
            'start_date': '2024-01-01',
            'end_date': '2026-02-26',
            'region_id': None,
            'store_id': None,
            'category_id': None,
            'customer_tier': None
        }

    def test_db_connection_and_scalar(self):
        from dashboard.services.db_service import execute_scalar
        result = execute_scalar("SELECT 42;")
        self.assertEqual(result, 42)

    def test_filter_service_options(self):
        from dashboard.services.filter_service import get_filter_options
        opts = get_filter_options()
        self.assertGreater(len(opts['regions']), 0)
        self.assertGreater(len(opts['stores']), 0)
        self.assertGreater(len(opts['categories']), 0)
        self.assertGreater(len(opts['tiers']), 0)

    def test_executive_service_reconciliation(self):
        from dashboard.services.executive_service import get_executive_summary_data
        data = get_executive_summary_data(self.default_filters)
        net_rev = data['kpis']['net_revenue']['current']
        # Headline revenue should match ₹6,769,536,004.48 (approx 676.95 Cr)
        self.assertAlmostEqual(net_rev, 6769536004.48, delta=100.0)
        self.assertEqual(data['kpis']['order_volume']['current'], 82540)
        self.assertGreater(len(data['monthly_trend']), 20)
        self.assertGreater(len(data['attention_items']), 0)

    def test_sales_service_reconciliation(self):
        from dashboard.services.sales_service import get_sales_dashboard_data
        data = get_sales_dashboard_data(self.default_filters)
        self.assertAlmostEqual(data['headline']['total_net_revenue'], 6769536004.48, delta=100.0)
        self.assertEqual(len(data['categories']), 10)
        self.assertEqual(len(data['top_skus']), 10)
        self.assertGreater(len(data['payment_modes']), 0)

    def test_customer_service_data(self):
        from dashboard.services.customer_service import get_customer_dashboard_data
        data = get_customer_dashboard_data(self.default_filters)
        self.assertGreater(data['overview']['total_active_customers'], 40000)
        self.assertEqual(len(data['tiers']), 4)
        self.assertGreater(len(data['rfm_segments']), 0)
        self.assertEqual(len(data['reviews']), 5)

    def test_operations_service_data(self):
        from dashboard.services.operations_service import get_operations_dashboard_data
        data = get_operations_dashboard_data(self.default_filters)
        self.assertGreater(data['shipment_summary']['total_shipments'], 100000)
        self.assertEqual(len(data['couriers']), 4)
        self.assertEqual(len(data['warehouses']), 5)
        self.assertEqual(len(data['mfg_lines']), 10)

    def test_cross_functional_service_data(self):
        from dashboard.services.cross_functional_service import get_cross_functional_dashboard_data
        data = get_cross_functional_dashboard_data(self.default_filters)
        self.assertGreater(len(data['lead_time_impact']), 0)
        self.assertGreater(len(data['returns_by_reason']), 0)
        self.assertGreater(len(data['mfg_sales_alignment']), 0)
        self.assertGreater(data['perfect_order']['perfect_order_rate_pct'], 50.0)

    def test_simulator_baseline(self):
        from dashboard.services.simulator_service import get_simulator_baseline
        baseline = get_simulator_baseline()
        self.assertAlmostEqual(baseline['base_net_revenue'], 6769536004.48, delta=100.0)
        self.assertGreater(baseline['base_contribution_margin'], 0)
