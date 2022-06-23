from django import forms


class AddToCartForm(forms.Form):
    QUANTITY_CHOICE = [(str(i), i) for i in range(1, 21)]

    quantity = forms.TypedChoiceField(
        choices=QUANTITY_CHOICE,
        coerce=int,
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

# TypedChoiceField - тоже что и ChoiceField, только с имнованным аргументом coerce (принуждать)
# который будет менять тип данных из того что выбрали на тот который передаётся в coerce
# в шаблоне будет тег <select> с выбором options (варианты из QUANTITY_CHOICE)
# благодаря этому полю мы имеем в python коде когда достаём из request.POST
# цифру quantity как int
# https://docs.djangoproject.com/en/4.0/ref/forms/fields/#typedchoicefield
# https://github.com/Kirill67tyar/myshop/blob/master/src/cart/forms.py
