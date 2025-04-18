from django.test import TestCase
from django.urls import reverse
from .models import BabyProductCategory, BabyProduct

class BabyProductTests(TestCase):
    def setUp(self):
        self.category = BabyProductCategory.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.product = BabyProduct.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=9.99,
            description="Test description",
            age_range="0-6",
            safety_rating=4,
            stock=10
        )

    def test_product_listing(self):
        self.assertEqual(f"{self.product.name}", "Test Product")
        self.assertEqual(f"{self.product.description}", "Test description")
        self.assertEqual(self.product.price, 9.99)

    def test_product_list_view(self):
        response = self.client.get(reverse('baby_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'baby_shop/list.html')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        no_response = self.client.get('/baby/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'baby_shop/detail.html')