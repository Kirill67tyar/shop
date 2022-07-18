from django.utils import timezone
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from coupons.models import Coupon
from coupons.forms import CouponApplyForm
from common.utils import get_object_or_null


@require_POST
def coupon_apply_view(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        coupon = get_object_or_null(
            model=Coupon,
            code__iexact=code,
            valid_from__lte=now,
            valid_to__gte=now,
            active=True,
        )
        if coupon:
            request.session['coupon_id'] = coupon.pk
    return redirect('cart:detail_cart')
