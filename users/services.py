import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """ Создаёт продукт в Stripe. """
    try:
        stripe_product = stripe.Product.create(name=product)
        return stripe_product
    except stripe.error.StripeError as e:
        print(f"Произошла ошибка при создании продукта: {e}")
        return None


def create_stripe_price(amount, product_id=None):
    """Создаёт цену в Stripe."""
    unit_amount = int(round(amount * 100))
    return stripe.Price.create(
        currency="rub",
        unit_amount=unit_amount,
        product=product_id,
    )


def create_stripe_sessions(price):
    """Создает сессию на оплату в Stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
