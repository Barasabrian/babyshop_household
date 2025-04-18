from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()

class HouseholdCategory(models.Model):
    ROOM_CHOICES = [
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('bedroom', 'Bedroom'),
        ('living', 'Living Room'),
        ('dining', 'Dining Room'),
        ('outdoor', 'Outdoor'),
        ('office', 'Office'),
        ('storage', 'Storage'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    room_type = models.CharField(max_length=50, choices=ROOM_CHOICES)
    image = models.ImageField(upload_to='household_categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Household Categories"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('household:category_detail', args=[self.slug])

class HouseholdProduct(models.Model):
    MATERIAL_CHOICES = [
        ('wood', 'Wood'),
        ('metal', 'Metal'),
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('fabric', 'Fabric'),
        ('ceramic', 'Ceramic'),
        ('stone', 'Stone'),
        ('other', 'Other'),
    ]
    
    category = models.ForeignKey(
        HouseholdCategory,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    description = models.TextField()
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    dimensions = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Weight in kg"
    )
    care_instructions = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('household:product_detail', args=[self.slug])
    
    def get_discount_percentage(self):
        if self.discounted_price:
            return int(100 - (self.discounted_price / self.price * 100))
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(
        HouseholdProduct,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='household_products/images/')
    alt_text = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"