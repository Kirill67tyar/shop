# from django.contrib.sessions.backends.db import SessionStore
# from django.conf import settings

# from django.template.context_processors import request

from django.contrib.auth.context_processors import auth

# ---------------------------------------------------------------------- braintree
# панель для системы оплаты braintree - demo version (не для продакшн).
# https://sandbox.braintreegateway.com/merchants/nv5dfpjh7jv353hc/home
# именно от сюда берется BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY и BRAINTREE_PRIVATE_KEY

# для пробного варианта используй карту:
# № 4111 1111 1111 1111
# CVV - 123
# date - 12/24
# ---------------------------------------------------------------------- braintree
