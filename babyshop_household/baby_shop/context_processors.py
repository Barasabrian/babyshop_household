from .models import BabyProductCategory  

def baby_categories(request):
    """
    Context processor to make baby product categories available in all templates
    """
    categories = BabyProductCategory.objects.filter(is_active=True)
    return {'baby_categories': categories}