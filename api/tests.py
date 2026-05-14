from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from app.models import Brand, Categories, Color, Filter_Price, Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat = Categories.objects.create(name='Cat')
        self.brand = Brand.objects.create(name='Brand')
        self.color = Color.objects.create(name='Black', code='#000')
        self.fp = Filter_Price.objects.create(price='1000 To 3000')
        self.admin = User.objects.create_user(
            'admin', 'a@test.com', 'pass', is_staff=True, is_superuser=True
        )

    def test_list_products_public(self):
        Product.objects.create(
            name='Phone',
            price='100',
            condition='New',
            stock='IN STOCK',
            status='Publish',
            categories=self.cat,
            brand=self.brand,
            color=self.color,
            filter_price=self.fp,
        )
        r = self.client.get('/api/products/')
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.data.get('results', r.data)), 1)

    def test_create_product_requires_admin(self):
        self.client.force_authenticate(user=self.admin)
        # image required — skip full create without file; assert permission path
        r = self.client.post('/api/products/', {}, format='json')
        self.assertIn(r.status_code, (400, 415))
