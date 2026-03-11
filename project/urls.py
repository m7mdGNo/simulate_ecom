from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import accounts.urls as accounts_url
import cart.urls as cart_url
import orders.urls as orders_url
import products.urls as products_url
import blog.urls as blog_urls
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language


schema_view = get_schema_view(
    openapi.Info(
        title="Farm Ecommerce API",
        default_version="v1",
        description="API documentation for the Farm Ecommerce project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/accounts/', include(accounts_url)),
    path('api/cart/', include(cart_url)),
    path('api/orders/', include(orders_url)),
    path('api/products/', include(products_url)),
    path('api/blogs/', include(blog_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += i18n_patterns(
    path('set_language/', set_language, name='set_language'),
)