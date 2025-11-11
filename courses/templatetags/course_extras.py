from django import template

register = template.Library()

@register.filter
def star_rating(rating):
    """
    Returns a list of stars based on the rating
    Each item in the list is a dict with 'type' key having values 'fill', 'half', or 'empty'
    """
    stars = []
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    
    # Add full stars
    for i in range(full_stars):
        stars.append({'type': 'fill'})
    
    # Add half star if needed
    if half_star:
        stars.append({'type': 'half'})
    
    # Add empty stars to make total 5
    while len(stars) < 5:
        stars.append({'type': 'empty'})
    
    return stars

@register.filter
def to_k_format(value):
    """
    Convert number to 'k' format if over 1000 (e.g., 1500 becomes '1.5k')
    """
    try:
        value = int(value)
        if value >= 1000:
            k_value = value / 1000.0
            if k_value.is_integer():
                return f"{int(k_value)}k"
            else:
                return f"{k_value:.1f}k"
        return str(value)
    except (ValueError, TypeError):
        return value

@register.filter
def multiply(value, arg):
    """Multiplies the arg value by the given value"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value

@register.filter  
def add_multiply(value, args):
    """Adds first argument to value, then multiplies by second argument"""
    try:
        args = args.split(',')
        add_val = int(args[0])
        mult_val = int(args[1])
        return (int(value) + add_val) * mult_val
    except (ValueError, TypeError, IndexError):
        return value