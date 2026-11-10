# Hardening notes (Lab 7):
# - Valid inputs (in the formats below) give the same results as the original code.
# - Invalid input (wrong type, empty, malformed, unsupported) returns None instead of crashing.
# - Choices made when hardening:
#   * price/qty: whole numbers written with ASCII digits (int() also accepts "-5", "1_0" and
#     other unicode digits, which are not valid cart quantities).
#   * promo: "OFF<n>" with n from 0 to 100 (a discount above 100% makes no sense).
#   * pincode: exactly 6 digits; first digit must be in ZONES (1-8), so 0 and 9 are unserviceable.
import re

ZONES = {"1": "North", "2": "North", "3": "West", "4": "West",
         "5": "South", "6": "South", "7": "East", "8": "East"}

PROMO_PATTERN = re.compile(r"OFF\s*(\d{1,3})", re.ASCII)


def _is_plain_number(text):
    """True only for a non-empty string of ASCII digits (no sign, spaces or unicode digits)."""
    return text.isascii() and text.isdigit()


def cart_total(cart):
    """Total of a 'name:pricexqty' CSV cart. Returns None for invalid input."""
    if not isinstance(cart, str) or not cart.strip():
        return None
    total = 0
    for item in cart.split(','):
        parts = item.split(':')
        if len(parts) != 2:
            return None
        values = parts[1].split('x')
        if len(values) != 2:
            return None
        price, qty = (v.strip() for v in values)
        if not (_is_plain_number(price) and _is_plain_number(qty)):
            return None
        total += int(price) * int(qty)
    return total


def promo_percent(code):
    """Discount percent from a code like 'OFF20' (0-100). Returns None for invalid input."""
    if not isinstance(code, str):
        return None
    match = PROMO_PATTERN.fullmatch(code.strip().upper())
    if not match:
        return None
    percent = int(match.group(1))
    if percent > 100:
        return None
    return percent


def delivery_zone(pincode):
    """Zone for a 6 digit pincode. Returns None for invalid input."""
    if not isinstance(pincode, str):
        return None
    pincode = pincode.strip()
    if len(pincode) != 6 or not _is_plain_number(pincode):
        return None
    return ZONES.get(pincode[0])


def main():
    print("==== Running cart_total ====")
    user_input = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    result = cart_total(user_input)
    if result is None:
        print("Invalid cart. Expected name:pricexqty,name:pricexqty with whole numbers.")
    else:
        print("Cart Total:", result)

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    if result is None:
        print("Invalid promo code. Expected OFF followed by a number from 0 to 100.")
    else:
        print("Discount Percent:", result)

    print("\n==== Running delivery_zone ====")
    user_input = input("Enter a 6 digit pincode (e.g. 560085): ")
    result = delivery_zone(user_input)
    if result is None:
        print("Invalid or unserviceable pincode. Expected 6 digits starting with 1-8.")
    else:
        print("Delivery Zone:", result)


if __name__ == "__main__":
    main()
