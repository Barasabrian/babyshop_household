from django import forms
from .models import BabyProduct, ProductReview, BabyProductCategory

class BabyProductForm(forms.ModelForm):
    class Meta:
        model = BabyProduct
        fields = [
            'category', 'name', 'slug', 'price', 'description',
            'age_range', 'safety_rating', 'stock', 'image', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.NumberInput(attrs={'min': 1, 'max': 5})
        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 4})

class ProductFilterForm(forms.Form):
    age_range = forms.ChoiceField(choices=[], required=False)
    min_price = forms.DecimalField(min_value=0, required=False, label='Min Price')
    max_price = forms.DecimalField(min_value=0, required=False, label='Max Price')
    safety_rating = forms.DecimalField(min_value=0, max_value=5, required=False, label='Min Safety Rating')
    search = forms.CharField(max_length=100, required=False, label='Search')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate age_range choices from BabyProduct model
        age_ranges = BabyProduct.objects.values_list('age_range', flat=True).distinct()
        self.fields['age_range'].choices = [('', 'All Ages')] + [(age, age) for age in age_ranges if age]
