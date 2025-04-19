from .models import HouseholdCategory

def household_categories(request):
    """
    Makes active household categories available in all templates
    """
    categories = HouseholdCategory.objects.filter(is_active=True)
    return {
        'household_categories': categories,
        'household_room_types': HouseholdCategory.ROOM_CHOICES
    }