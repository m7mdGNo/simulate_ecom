from django.db.models import QuerySet
from django.db.models import Sum, Count, F

class OrderManager(QuerySet):
    def with_total_price(self):
        return self.annotate(
            total_price=Sum(F('items__product__price') * F('items__quantity')) + F('shipping_price')
        ).annotate(
            total_sub_price=Sum(F('items__product__price') * F('items__quantity'))
        ).order_by('-created') 


class OrderItemManager(QuerySet):
    def with_total_price(self):
        return self.annotate(total_price=F('product__price') * F('quantity'))
    

class BillingAddressManager(QuerySet):
    def is_active(self):
        return self.filter(is_deleted=False)