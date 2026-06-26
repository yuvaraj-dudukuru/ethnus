# ============================================================================
#  urls.py — the project's master "address book"
# ----------------------------------------------------------------------------
#  A DRF "router" builds the standard CRUD URLs for the product and order
#  ViewSets. On top of that we hand-write the cart URLs (the cart is a simple
#  pair of endpoints), plus login/logout and the docs.
# ============================================================================
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # serves a plain HTML page (NEW in M6)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from shop.api_views import (
    CategoryViewSet, ProductViewSet, OrderViewSet,
    CartView, CartItemsView, LogoutAPI, MeView,
)

# 1) Register the ViewSets with the router.
router = DefaultRouter()
router.register('products', ProductViewSet)              # /api/products/...
router.register('orders', OrderViewSet, basename='order')  # /api/orders/...
router.register('categories', CategoryViewSet)          # /api/categories/  (NEW in M6)

# 2) The full list of URL patterns.
urlpatterns = [
    # --- Module 6: the front-end dashboard page ---
    # The home page ("/") renders shop/templates/shop/dashboard.html. All the
    # live behaviour (polling stock, flashing changes, product CRUD) is done by
    # JavaScript talking to the API below.
    path('', TemplateView.as_view(template_name='shop/dashboard.html'),
         name='dashboard'),

    path('admin/', admin.site.urls),

    # "Who am I?" — the front-end auth/staff check (NEW in M6).
    path('api/me/', MeView.as_view(), name='api-me'),

    # --- Cart endpoints (the cart is per-user, not a ViewSet) ---
    path('api/cart/', CartView.as_view(), name='cart'),            # GET mine • DELETE clear
    path('api/cart/items/', CartItemsView.as_view(), name='cart-items'),  # POST add/update • DELETE remove

    # All router-generated API URLs (products, orders, categories).
    path('api/', include(router.urls)),

    # --- Authentication endpoints ---
    path('api/login/', obtain_auth_token, name='api-login'),   # POST -> {"token": ...}
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),

    # --- Auto-generated documentation ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

# Handy URLs (also in the README):
#   http://127.0.0.1:8000/api/products/   -> public catalog (cursor-paginated)
#   http://127.0.0.1:8000/api/cart/       -> your cart (auth)
#   http://127.0.0.1:8000/api/orders/     -> your orders / POST to checkout (auth)
#   http://127.0.0.1:8000/api/docs/       -> Swagger documentation
#   http://127.0.0.1:8000/admin/          -> admin panel (admin / admin)
