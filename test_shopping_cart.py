from hypothesis import given, strategies as st
from shopping_cart import cart_total, promo_percent, delivery_zone

@given(st.text() | st.none())
def test_cart_total_no_crash(s):

@given(st.text() | st.none())
def test_promo_percent_no_crash(s):

@given(st.text() | st.none())
def test_delivery_zone_no_crash(s):
