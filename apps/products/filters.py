import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category', lookup_expr='exact')
    farm = django_filters.NumberFilter(field_name='farm', lookup_expr='exact')
    unit = django_filters.NumberFilter(field_name='unit', lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_deleted = django_filters.BooleanFilter(field_name='is_deleted')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'is_deleted']
