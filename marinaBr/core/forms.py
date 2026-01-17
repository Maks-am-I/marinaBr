from django import forms
from datetime import date, time


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Имя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя',
            'class': 'form-input'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+7 (999) 999 99 99',
            'class': 'form-input'
        })
    )
    
    question = forms.CharField(
        label='Ваш вопрос',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Опишите ваш вопрос...',
            'class': 'form-textarea'
        })
    )


class OrderForm(forms.Form):
    customer_name = forms.CharField(
        max_length=255,
        label='Ваше имя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Иван Иванов',
            'class': 'form-input'
        })
    )
    
    customer_phone = forms.CharField(
        max_length=20,
        label='Ваш номер телефона',
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '+7 (999) 999 99 99',
            'class': 'form-input'
        })
    )
    
    order_date = forms.DateField(
        label='Дата заказа',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input',
            'min': date.today().isoformat()
        })
    )
    
    order_time = forms.TimeField(
        label='Время заказа',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-input'
        })
    )
    
    delivery_address = forms.CharField(
        label='Адрес доставки',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ленина, д. 1, кв. 1',
            'class': 'form-input'
        })
    )
