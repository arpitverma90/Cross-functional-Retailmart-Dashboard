import os
import unittest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User


class ViewRoutingTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test_executive'
        self.password = 'ExecutivePass123!'
        if not User.objects.filter(username=self.username).exists():
            self.user = User.objects.create_user(
                username=self.username,
                password=self.password
            )
        else:
            self.user = User.objects.get(username=self.username)

    def test_health_check_endpoint(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['database'], 'healthy')

    def test_login_page_renders(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('RetailMart', response.content.decode('utf-8'))

    def test_unauthenticated_redirect(self):
        response = self.client.get('/executive-summary/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_authenticated_executive_summary(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/executive-summary/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Executive Summary', response.content.decode('utf-8'))
        self.assertIn('Delivered Net Revenue', response.content.decode('utf-8'))

    def test_authenticated_marketing_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/marketing/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Marketing Intelligence', content)
        self.assertIn('Campaign Ad Spend', content)

    def test_authenticated_digital_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/digital/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Digital Experience', content)
        self.assertIn('Total Web Sessions', content)

    def test_authenticated_logistics_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/logistics/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Logistics &amp; Supply Chain', content)
        self.assertIn('Delivered Shipments', content)

    def test_authenticated_cross_functional_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/cross-functional/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Cross-Functional Integration', content)
        self.assertIn('Delivered Net Revenue', content)

    def test_authenticated_scenario_simulator(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/simulator/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Contribution Margin Scenario Simulator', response.content.decode('utf-8'))

    def test_api_endpoints(self):
        self.client.login(username=self.username, password=self.password)
        res_stores = self.client.get('/api/stores/')
        self.assertEqual(res_stores.status_code, 200)
        self.assertIn('stores', res_stores.json())

        res_sim = self.client.get('/api/simulator-baseline/')
        self.assertEqual(res_sim.status_code, 200)
        self.assertIn('base_net_revenue', res_sim.json())

    def test_filtered_views(self):
        self.client.login(username=self.username, password=self.password)
        params = {
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'region_id': '1',
        }
        for path in ['/business-dashboard/marketing/', '/business-dashboard/digital/', '/business-dashboard/logistics/', '/business-dashboard/cross-functional/']:
            res = self.client.get(path, params)
            self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
