from django import forms


class OrderForm(forms.Form):
    quantity = forms.IntegerField(label = 'Количество', min_value = 0, max_value = 10)