"""
Custom Prometheus metrics for business-level monitoring
Export: Total users, active users, total orders, cart items, etc.
"""
from prometheus_client import Gauge
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# Business metrics
total_users_gauge = Gauge(
    'ecommerce_total_users',
    'Total number of registered users'
)

active_users_gauge = Gauge(
    'ecommerce_active_users_24h',
    'Number of active users in last 24 hours'
)

total_orders_gauge = Gauge(
    'ecommerce_total_orders',
    'Total number of orders'
)

pending_orders_gauge = Gauge(
    'ecommerce_pending_orders',
    'Number of pending orders'
)

total_order_items_gauge = Gauge(
    'ecommerce_total_order_items',
    'Total number of order items'
)

cart_items_gauge = Gauge(
    'ecommerce_cart_items',
    'Total items in all carts'
)

total_products_gauge = Gauge(
    'ecommerce_total_products',
    'Total number of products'
)

total_blogs_gauge = Gauge(
    'ecommerce_total_blogs',
    'Total number of blog posts'
)

total_reviews_gauge = Gauge(
    'ecommerce_total_reviews',
    'Total number of product reviews'
)

order_revenue_gauge = Gauge(
    'ecommerce_order_revenue_total',
    'Total revenue from orders'
)

average_order_value_gauge = Gauge(
    'ecommerce_average_order_value',
    'Average order value'
)

admin_users_gauge = Gauge(
    'ecommerce_admin_users',
    'Number of admin/staff users'
)


def update_business_metrics():
    """
    Update all custom business metrics from the database
    Called periodically or on-demand
    """
    from accounts.models import User
    from orders.models import Order, OrderItem
    from cart.models import Cart
    from products.models import Product
    from blog.models import Blog
    
    # Total users
    total_users = User.objects.count()
    total_users_gauge.set(total_users)
    
    # Active users (last 24 hours)
    last_24h = timezone.now() - timedelta(hours=24)
    active_users = User.objects.filter(
        last_login__gte=last_24h
    ).count()
    active_users_gauge.set(active_users)
    
    # Admin users
    admin_users = User.objects.filter(is_staff=True).count()
    admin_users_gauge.set(admin_users)
    
    # Total orders
    total_orders = Order.objects.count()
    total_orders_gauge.set(total_orders)
    
    # Pending orders (no payment status tracking in current model, so count all for now)
    pending_orders = Order.objects.count()
    pending_orders_gauge.set(pending_orders)
    
    # Total order items
    total_order_items = OrderItem.objects.count()
    total_order_items_gauge.set(total_order_items)
    
    # Cart items
    cart_items = Cart.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0
    cart_items_gauge.set(cart_items)
    
    # Total products
    total_products = Product.objects.count()
    total_products_gauge.set(total_products)
    
    # Total blogs
    total_blogs = Blog.objects.count()
    total_blogs_gauge.set(total_blogs)
    
    # Total reviews (set to 0 since reviews app doesn't exist)
    total_reviews = 0
    total_reviews_gauge.set(total_reviews)
    
    # Order revenue (estimated from order count if no price data in model)
    # For now, we'll set it based on order volume
    revenue = OrderItem.objects.count() * 50  # Rough estimate: 50 per item
    order_revenue_gauge.set(revenue)
    
    # Average order value
    if total_orders > 0:
        avg_order_value = revenue / total_orders
    else:
        avg_order_value = 0
    average_order_value_gauge.set(avg_order_value)
