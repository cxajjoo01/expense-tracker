from .models import Expense
from django.forms import ModelForm

class Expenseform(ModelForm):
    class Meta:
        model = Expense
        fields = ('name','amount','category',)