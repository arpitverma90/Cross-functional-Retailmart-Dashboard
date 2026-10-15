import os
import unittest
import django

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

    def test_marketing_service_kpis(self):
        from dashboard.services.marketing_service import get_marketing_kpis, get_spend_by_platform, get_top_campaigns
        kpis = get_marketing_kpis(self.default_filters)
        self.assertAlmostEqual(kpis['total_spend'], 10302874.41, delta=100.0)
        self.assertEqual(kpis['total_campaigns'], 244)  # 244 campaigns within 2024-01-01 to 2026-02-26
        self.assertGreater(kpis['open_rate'], 20.0)
        self.assertGreater(kpis['ctr'], 15.0)

        platforms = get_spend_by_platform(self.default_filters)
        self.assertEqual(len(platforms), 5)
        top_c = get_top_campaigns(self.default_filters, limit=5)
        self.assertEqual(len(top_c), 5)

    def test_digital_service_kpis(self):
        from dashboard.services.digital_service import get_digital_kpis, get_device_os_mix, get_digital_funnel
        kpis = get_digital_kpis(self.default_filters)
        self.assertEqual(kpis['total_sessions'], 99320)
        self.assertEqual(kpis['total_page_views'], 500000)
        self.assertGreater(kpis['mobile_share_pct'], 50.0)

        devices = get_device_os_mix(self.default_filters)
        self.assertGreater(len(devices), 0)
        funnel = get_digital_funnel(self.default_filters)
        self.assertEqual(len(funnel), 4)

    def test_logistics_service_kpis(self):
        from dashboard.services.logistics_service import get_logistics_kpis, get_courier_sla_breakdown, get_warehouse_utilization
        kpis = get_logistics_kpis(self.default_filters)
        self.assertEqual(kpis['delivered_shipments'], 82331)  # 82,331 delivered shipments within window
        self.assertAlmostEqual(kpis['otd_sla_rate'], 79.8, delta=2.0)

        couriers = get_courier_sla_breakdown(self.default_filters)
        self.assertEqual(len(couriers), 4)
        warehouses = get_warehouse_utilization(self.default_filters)
        self.assertEqual(len(warehouses), 5)
        self.assertEqual(kpis['stockout_skus'], 17475)

    def test_cross_functional_service_kpis(self):
        from dashboard.services.cross_functional_service import get_cross_functional_dashboard_data
        data = get_cross_functional_dashboard_data(self.default_filters)
        self.assertAlmostEqual(data['kpis']['delivered_revenue'], 6769536004.48, delta=100.0)
        self.assertGreater(data['kpis']['mer_ratio'], 500.0)
        self.assertGreater(len(data['alignment']), 20)
        self.assertGreater(len(data['leakage']), 0)
        self.assertGreater(len(data['promos']), 0)

    def test_executive_service_data(self):
        from dashboard.services.executive_service import get_executive_summary_data
        data = get_executive_summary_data(self.default_filters)
        self.assertEqual(len(data['kpi_cards']), 10)
        self.assertGreater(len(data['monthly_trajectory']), 20)
        self.assertEqual(len(data['management_attention']), 4)

    def test_simulator_baseline(self):
        from dashboard.services.simulator_service import get_simulator_baseline
        baseline = get_simulator_baseline()
        self.assertAlmostEqual(baseline['base_net_revenue'], 6769536004.48, delta=100.0)
        self.assertGreater(baseline['base_contribution_margin'], 0)


if __name__ == '__main__':
    unittest.main()
