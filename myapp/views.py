from django.shortcuts import render,redirect
from .forms import Expenseform
from .models import Expense
from django.db.models import Sum
import datetime

# Create your views here.
def index(request):
    if request.method =="POST":
        expense = Expenseform(request.POST)
        if expense.is_valid():
            expense.save()
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
   

   #logic to calculate 365 days Expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))
    
   #logic to calculate 30 days Expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

       
   #logic to calculate 7 days Expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    #print(categorical_sums)

    expense_form = Expenseform()
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,'daily_sums':daily_sums,'categorical_sums':categorical_sums})

def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = Expenseform(instance=expense)
    if request.method =="POST":
        expense = Expense.objects.get(id=id)
        form = Expenseform(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request,'myapp/edit.html',{'expense_form':expense_form})

def delete(request,id):
    if request.method =="POST" and "delete" in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
