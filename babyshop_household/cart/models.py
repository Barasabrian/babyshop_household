from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from baby_shop.models import BabyProduct
from household.models import HouseholdProduct
from django.utils import timezone

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts'
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f"Cart #{self.id} - {self.user.email}"
        return f"Cart #{self.id} - Anonymous"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    def merge_cart(self, other_cart):
        """Merge another cart into this one"""
        for item in other_cart.items.all():
            existing_item = self.items.filter(
                baby_product=item.baby_product,
                household_product=item.household_product
            ).first()
            
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
                item.delete()
            else:
                item.cart = self
                item.save()
        
        other_cart.delete()
        return self

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    baby_product = models.ForeignKey(
        BabyProduct,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    household_product = models.ForeignKey(
        HouseholdProduct,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-added_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(baby_product__isnull=False) | models.Q(household_product__isnull=False),
                name='not_both_null'
            ),
            models.UniqueConstraint(
                fields=['cart', 'baby_product'],
                name='unique_baby_product',
                condition=models.Q(baby_product__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['cart', 'household_product'],
                name='unique_household_product',
                condition=models.Q(household_product__isnull=False)
            ),
        ]
    
    def __str__(self):
        product = self.get_product()
        return f"{self.quantity}x {product.name} in Cart #{self.cart.id}"
    
    def get_product(self):
        return self.baby_product if self.baby_product else self.household_product
    
    def get_unit_price(self):
        product = self.get_product()
        return product.discounted_price if product.discounted_price else product.price
    
    def get_total_price(self):
        return self.get_unit_price() * self.quantity
    
    def clean(self):
        if not self.baby_product and not self.household_product:
            raise ValidationError("At least one product must be set")
        if self.baby_product and self.household_product:
            raise ValidationError("Only one product can be set")

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.PROTECT,
        related_name='order'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    billing_address = models.TextField()
    shipping_method = models.CharField(max_length=50, blank=True)
    tracking_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"
    
    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.total_amount and self.cart:
            self.total_amount = self.cart.get_total_price()
        super().save(*args, **kwargs)