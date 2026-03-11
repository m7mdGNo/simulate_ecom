from django.db.models import QuerySet
from orders.models import OrderItem
from django.db.models import Sum, Count

class ProductManager(QuerySet):
    def active_products(self):
        return self.filter(is_deleted=False)
    
    def in_stock_products(self):
        return self.active_products().filter(quantity__gt=0)

    def products_by_category(self, category_id):
        return self.in_stock_products().filter(category_id=category_id)
    
    def products_by_farm(self, farm_id):
        return self.in_stock_products().filter(farm_id=farm_id)
    
    def products_by_unit(self, unit_id):
        return self.in_stock_products().filter(unit_id=unit_id)
    
    def search_products(self, query):
        return self.in_stock_products().filter(title__icontains=query)
    
    def with_num_of_orders(self):
        return self.annotate(num_of_orders=Count('orderitem'))
    
    def with_total_order_items(self):
        return self.annotate(total_order_items=Sum('orderitem__quantity'))
    

class CategoryManager(QuerySet):
    def active_categories(self):
        return self.filter(is_deleted=False)
    

class UnitManager(QuerySet):
    def active_units(self):
        return self.filter(is_deleted=False)