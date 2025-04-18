from django.test import TestCase
from django.urls import reverse
from .models import HouseholdCategory, HouseholdProduct

class HouseholdProductTests(TestCase):
    def setUp(self):
        self.category = HouseholdCategory.objects.create(
            name="Test Category",
            slug="test-category",
            room_type="kitchen"
        )
        self.product = HouseholdProduct.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=19.99,
            description="Test description",
            material="wood",
            stock=5
        )

    def test_product_listing(self):
        self.assertEqual(f"{self.product.name}", "Test Product")
        self.assertEqual(f"{self.product.description}", "Test description")
        self.assertEqual(self.product.price, 19.99)

    def test_product_list_view(self):
        response = self.client.get(reverse('household_product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'household/list.html')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        no_response = self.client.get('/household/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'household/detail.html')