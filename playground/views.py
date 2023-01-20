from django.shortcuts import render, redirect
from django.http import HttpResponse
from playground.models import Employee
from playground.form import EmployeeForm
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
#request handler


def adduser(request):
    employee = Employee.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')        
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request, 'form.html', {'form':form})



def viewers(request):
    employee = Employee.objects.all().order_by('-id')
    employees = []
    search = request.GET.get('search')
    if search:
        employee = employee.filter( Q(id__icontains=search)|Q(fullname__icontains=search) | Q(email__icontains=search))
        if employee.exists():
            message = None
            paginator = Paginator(employee, 10) # Show 10 employees per page
            page = request.GET.get('page')
            employees = paginator.get_page(page)
            return render(request, 'index.html', {'name':'Jay r', 'employees':employees, 'message': message})
        else:
            message = "No data found for the search query: {}".format(search)
    else:
        message = None
        paginator = Paginator(employee, 10) # Show 10 employees per page
        page = request.GET.get('page')
        employees = paginator.get_page(page)
    return render(request, 'index.html', {'name':'Jay r', 'employees':employees, 'message': message})





def getEdit(request, id):
    employee = Employee.objects.get( id = id)
    return render(request, 'edit.html', {'employee':employee})


def delete(request, id):
    employee = Employee.objects.get(id = id)
    employee.delete()
    return  redirect('/')


def update(request, id):
    employee = Employee.objects.get(id = id)
    form = EmployeeForm(request.POST, instance= employee)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html', {'employee':employee})
