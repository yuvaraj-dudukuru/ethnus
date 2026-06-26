def cart_count(request):
    """
    Context processor to make the total number of items in the cart
    available to all templates (e.g., for a navbar badge).
    """
    # Get the cart from the session
    cart = request.session.get('cart', {})
    
    # Calculate the total number of items (sum of quantities)
    total_items = sum(cart.values())
    
    # Return a dictionary to be merged into the template context
    return {'cart_count': total_items}
