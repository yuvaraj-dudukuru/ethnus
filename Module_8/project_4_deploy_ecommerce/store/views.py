# Import standard Django shortcut functions
from django.shortcuts import render, get_object_or_404, redirect
# Import decorator to require login for certain views
from django.contrib.auth.decorators import login_required
# Import authentication functions (login, authenticate, logout)
from django.contrib.auth import login, authenticate, logout
# Import built-in Django forms for user registration and authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Import the generic ListView for class-based views
from django.views.generic import ListView
# Import mixin to require login for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# Import our models from the current app
from .models import Category, Product, Order, OrderItem

# --- Product Views ---

# View to list all products, optionally filtered by a category slug
def product_list(request, category_slug=None):
    # Initialize the category variable to None
    category = None
    # Retrieve all Category objects from the database
    categories = Category.objects.all()
    # Retrieve all Product objects that are marked as available
    products = Product.objects.filter(available=True)
    
    # Check if a category slug was passed in the URL
    if category_slug:
        # Retrieve the specific Category object matching the slug, or return a 404 error
        category = get_object_or_404(Category, slug=category_slug)
        # Filter the existing queryset of products to only include those in this category
        products = products.filter(category=category)
        
    # Render the 'product_list.html' template with the required context variables
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

# View to show the details of a single product
def product_detail(request, id, slug):
    # Fetch the Product by id and slug, ensuring it is available. Return 404 if not found.
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # Render the 'product_detail.html' template, passing the product object to it
    return render(request, 'store/product_detail.html', {'product': product})


# --- Cart Views ---

# View to add a product to the user's session-based shopping cart
def cart_add(request, pid):
    # Retrieve the 'cart' dictionary from the user's session. If it doesn't exist, use an empty dict.
    cart = request.session.get('cart', {})
    
    # The dictionary maps stringified product IDs to quantities.
    # We retrieve the current quantity (defaulting to 0) and add 1.
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    
    # We must explicitly reassign the cart dictionary back to request.session
    # This tells Django that the session has been modified and needs to be saved to the database/cookie.
    request.session['cart'] = cart
    
    # Redirect the user to the cart summary page
    return redirect('store:cart_view')

# View to display the contents of the cart
def cart_view(request):
    # Retrieve the cart dictionary from the session
    cart = request.session.get('cart', {})
    
    # Query the database for all products whose IDs are keys in the cart dictionary
    products = Product.objects.filter(id__in=cart.keys())
    
    # Build a list of dictionaries, one for each line item in the cart.
    # 'p' is the Product object, 'qty' is the quantity from the session, 'line' is the total cost for this item.
    items = [{'p': p, 'qty': cart[str(p.id)], 'line': p.price * cart[str(p.id)]} for p in products]
    
    # Calculate the overall total cost of the cart by summing the 'line' values
    total = sum(i['line'] for i in items)
    
    # Render the 'cart.html' template with the items list and total cost
    return render(request, 'store/cart.html', {'items': items, 'total': total})


# --- Checkout & Orders Views ---

# The @login_required decorator ensures only authenticated users can access this view
@login_required
def checkout(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', {})
    
    # If the user submitted a POST request (clicked "Confirm and Pay") and the cart is not empty:
    if request.method == 'POST' and cart:
        # Create a new, empty Order tied to the currently logged-in user with an initial total of 0
        order = Order.objects.create(user=request.user, total=0)
        # Initialize a running total variable
        total = 0
        
        # Iterate over all the actual Product objects that are in the cart
        for p in Product.objects.filter(id__in=cart.keys()):
            # Get the quantity of this specific product from the session cart
            qty = cart[str(p.id)]
            
            # Create an OrderItem linking the Product to the Order
            OrderItem.objects.create(
                order=order, 
                product=p, 
                qty=qty,
                # ⭐ SNAPSHOT: Save the current product price to the OrderItem. 
                # This guarantees historical accuracy even if the product's price is updated tomorrow.
                price_at_purchase=p.price
            )
            # Add the line item cost (price * qty) to the running total
            total += p.price * qty
            
            # (Optional) Stock deduction logic could go here: p.stock -= qty; p.save()
            
        # Update the order's total field with the calculated total amount
        order.total = total
        # Save the updated order to the database
        order.save()
        
        # Clear the user's shopping cart by setting it to an empty dictionary in the session
        request.session['cart'] = {}
        
        # Redirect the user to the order confirmation page, passing the new order's primary key (ID)
        return redirect('store:order_done', pk=order.pk)
        
    # If it's a GET request (or the cart is empty), render the checkout page
    return render(request, 'store/checkout.html', {'cart_has_items': bool(cart)})

# The @login_required decorator ensures only authenticated users can access the confirmation page
@login_required
def order_done(request, pk):
    # Fetch the order by its primary key, ensuring it belongs to the current user (security check!)
    order = get_object_or_404(Order, pk=pk, user=request.user)
    # Render the confirmation template, passing the order object
    return render(request, 'store/order_done.html', {'order': order})


# A class-based view to display a list of the user's past orders
class MyOrdersView(LoginRequiredMixin, ListView):
    # The model this view operates on
    model = Order
    # The template to render
    template_name = 'store/my_orders.html'
    # The name of the context variable to be used in the template (default is 'object_list')
    context_object_name = 'orders'
    
    # Override get_queryset to filter the orders
    def get_queryset(self):
        # Filter Order objects so the user only sees their own orders. 
        # prefetch_related is used to optimize the database query by joining the related order items and products.
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


# --- Auth Views ---

# View to handle user registration
def register(request):
    # If the user submitted the registration form (POST request)
    if request.method == 'POST':
        # Instantiate the UserCreationForm with the submitted POST data
        form = UserCreationForm(request.POST)
        # If the form data is valid (passwords match, username unique, etc.)
        if form.is_valid():
            # Save the new user to the database
            user = form.save()
            # Automatically log the user in after they register
            login(request, user)
            # Redirect them to the homepage/product list
            return redirect('store:product_list')
    # If it's a GET request, create an empty form
    else:
        form = UserCreationForm()
    # Render the registration template with the form
    return render(request, 'store/register.html', {'form': form})

# View to handle user login
def login_view(request):
    # If the user submitted the login form (POST request)
    if request.method == 'POST':
        # Instantiate the AuthenticationForm with the submitted POST data
        form = AuthenticationForm(data=request.POST)
        # If the form data is valid (correct username and password)
        if form.is_valid():
            # Retrieve the authenticated User object from the form
            user = form.get_user()
            # Log the user in (creates a session for them)
            login(request, user)
            # Redirect the user to the 'next' URL parameter if it exists, otherwise to the product list
            return redirect(request.GET.get('next', 'store:product_list'))
    # If it's a GET request, create an empty form
    else:
        form = AuthenticationForm()
    # Render the login template with the form
    return render(request, 'store/login.html', {'form': form})

# View to handle user logout
def logout_view(request):
    # If the user submitted a POST request to logout
    if request.method == 'POST':
        # Log the user out (clears their session data, including the cart!)
        logout(request)
        # Redirect them back to the product list
        return redirect('store:product_list')
    # If it's a GET request, render a confirmation page
    return render(request, 'store/logout.html')
