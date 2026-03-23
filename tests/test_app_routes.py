import unittest

from app import app


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_portfolio_home_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Michael Phillips", response.data)
        self.assertIn(b"Selected Work", response.data)
        self.assertIn(b"Drinking well", response.data)
        self.assertIn(b"An accidental discovery", response.data)
        self.assertIn(b"Asado Vineyard Dinner", response.data)
        self.assertIn(b"Start with the right culinary partner", response.data)
        self.assertIn(b"Bitter Orange Lambrusco PDP", response.data)
        self.assertIn(b"2021 Cabernet Sauvignon Beauregard Ranch", response.data)

    def test_project_detail_renders(self):
        response = self.client.get("/projects/harvest-weekend-email-system")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Beauregard Vineyards Email Campaigns", response.data)
        self.assertIn(b"Real Email Examples", response.data)

    def test_asado_project_detail_renders(self):
        response = self.client.get("/projects/asado-vineyard-dinner")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Asado Vineyard Dinner", response.data)
        self.assertIn(b"Argentinian Asado at the Beauregard Ranch", response.data)

    def test_live_chronicles_renders(self):
        response = self.client.get("/projects/biodynamic-chronicles/live")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Biodynamic Chronicles", response.data)


if __name__ == "__main__":
    unittest.main()
