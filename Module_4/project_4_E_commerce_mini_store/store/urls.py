# path() builds individual URL rules; we import the app's views to attach to them.
from django.urls import path
from . import views

# Namespace for this app so templates can reverse URLs as 'store:product_list', etc.
app_name = 'store'

# Every entry maps a URL pattern -> a view function/class, with a reusable name.
urlpatterns = [
    # --- Product listing and detail ---
    # Home page: list every available product.
    path('', views.product_list, name='product_list'),
    # Same listing view, but filtered to a single category captured from the slug.
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # Product detail page, identified by both its numeric id and SEO-friendly slug.
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # --- Cart urls (the cart lives in the session, not the database) ---
    # Show the current cart contents and running total.
    path('cart/', views.cart_view, name='cart_view'),
    # Add one unit of product <pid> to the cart, then redirect to the cart.
    path('cart/add/<int:pid>/', views.cart_add, name='cart_add'),

    # --- Checkout and Orders ---
    # Turn the session cart into permanent Order + OrderItem records (login required).
    path('checkout/', views.checkout, name='checkout'),
    # Order confirmation / "thank you" page for a specific order.
    path('order/<int:pk>/done/', views.order_done, name='order_done'),
    # A logged-in user's personal order history.
    path('my-orders/', views.MyOrdersView.as_view(), name='my_orders'),

    # --- Authentication (custom views wrapping Django's auth forms) ---
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
