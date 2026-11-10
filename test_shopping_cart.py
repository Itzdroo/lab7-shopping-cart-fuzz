import pytest
from hypothesis import given, strategies as st
from shopping_cart import cart_total, promo_percent, delivery_zone


# Fuzz inputs: any text, None, plus a few non-string types
fuzz_input = st.text() | st.none() | st.integers() | st.binary()


@given(fuzz_input)
def test_cart_total_no_crash(s):
    try:
        result = cart_total(s)
    except Exception as e:
        assert False, f"cart_total crashed with: {e!r}"
    # valid result is a non-negative int, invalid input is reported as None
    assert result is None or (isinstance(result, int) and result >= 0)


@given(fuzz_input)
def test_promo_percent_no_crash(s):
    try:
        result = promo_percent(s)
    except Exception as e:
        assert False, f"promo_percent crashed with: {e!r}"
    assert result is None or (isinstance(result, int) and 0 <= result <= 100)


@given(fuzz_input)
def test_delivery_zone_no_crash(s):
    try:
        result = delivery_zone(s)
    except Exception as e:
        assert False, f"delivery_zone crashed with: {e!r}"
    assert result is None or result in {"North", "West", "South", "East"}


# Structured fuzzing: well-formed inputs must give correct answers
item = st.tuples(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8),
    st.integers(min_value=0, max_value=10**6),
    st.integers(min_value=0, max_value=1000),
)


@given(st.lists(item, min_size=1, max_size=10))
def test_cart_total_valid_carts(items):
    cart = ",".join(f"{n}:{p}x{q}" for n, p, q in items)
    assert cart_total(cart) == sum(p * q for _, p, q in items)


@given(st.integers(min_value=0, max_value=100), st.sampled_from(["OFF", "off", "Off"]))
def test_promo_percent_valid_codes(pct, prefix):
    assert promo_percent(f"{prefix}{pct}") == pct


@given(st.text(alphabet="12345678", min_size=1, max_size=1), st.text(alphabet="0123456789", min_size=5, max_size=5))
def test_delivery_zone_valid_pincodes(first, rest):
    assert delivery_zone(first + rest) in {"North", "West", "South", "East"}


# Example-based checks: valid inputs keep their original meaning, invalid ones return None
@pytest.mark.parametrize("cart, expected", [
    ("pen:10x2,book:250x1", 270),      # example from the program prompt
    ("pen:0x5", 0),
    ("a:1x1,b:2x2,c:3x3", 14),
    ("pen: 10 x 2", 20),               # int() in the original tolerated spaces
])
def test_cart_total_examples(cart, expected):
    assert cart_total(cart) == expected


@pytest.mark.parametrize("cart", ["", ",", "pen", "pen:10", "pen:10x", "pen:x2", "pen:-1x2",
                                  "pen:10x2,", "pen:1.5x2", "pen:10x2x3", "a:b:1x1"])
def test_cart_total_invalid_examples(cart):
    assert cart_total(cart) is None


@pytest.mark.parametrize("code, expected", [("OFF20", 20), ("off5", 5), ("Off100", 100),
                                            ("OFF0", 0), (" OFF20 ", 20)])
def test_promo_percent_examples(code, expected):
    assert promo_percent(code) == expected


@pytest.mark.parametrize("code", ["", "OFF", "OFFabc", "20", "OFF-5", "OFF101", "SAVE20", "OFF20OFF5"])
def test_promo_percent_invalid_examples(code):
    assert promo_percent(code) is None


@pytest.mark.parametrize("pin, zone", [("560085", "South"), ("110001", "North"), ("300001", "West"),
                                       ("700001", "East"), ("800001", "East")])
def test_delivery_zone_examples(pin, zone):
    assert delivery_zone(pin) == zone


@pytest.mark.parametrize("pin", ["", "56008", "5600855", "abcdef", "056008", "956008", "56 085"])
def test_delivery_zone_invalid_examples(pin):
    assert delivery_zone(pin) is None
