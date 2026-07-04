from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employee, Department, Role
from datetime import datetime


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def all_emp(request):
    emps = Employee.objects.select_related('dept', 'role').all()
    context = {'emps': emps}
    return render(request, 'all_emp.html', context)


@login_required
def add_emp(request):
    departments = Department.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        try:
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()
            salary = int(request.POST['salary'])
            dept_id = request.POST['dept']
            role_id = request.POST['role']
            bonus = int(request.POST.get('bonus', 0))
            phone = request.POST['phone'].strip()

            if not first_name or not last_name or not phone:
                messages.error(request, 'First name, last name and phone are required.')
                return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})

            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept_id=dept_id,
                role_id=role_id,
                hire_date=datetime.now().date()
            )
            new_emp.save()
            messages.success(request, f'Employee {first_name} {last_name} added successfully!')
            return redirect('all_emp')

        except (ValueError, KeyError):
            messages.error(request, 'Invalid data submitted. Please check all fields.')
            return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})

    return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})


@login_required
def remove_emp(request):
    emps = Employee.objects.select_related('dept', 'role').all()

    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        emp = get_object_or_404(Employee, id=emp_id)
        name = f"{emp.first_name} {emp.last_name}"
        emp.delete()
        messages.success(request, f'Employee {name} removed successfully!')
        return redirect('remove_emp')

    return render(request, 'remove_emp.html', {'emps': emps})


@login_required
def filter_emp(request):
    emps = None
    departments = Department.objects.all()
    roles = Role.objects.all()
    query = {}

    if request.method == 'GET' and request.GET:
        dept_id = request.GET.get('dept')
        role_id = request.GET.get('role')
        min_salary = request.GET.get('min_salary')
        max_salary = request.GET.get('max_salary')
        search = request.GET.get('search', '').strip()

        emps = Employee.objects.select_related('dept', 'role').all()

        if dept_id:
            emps = emps.filter(dept_id=dept_id)
            query['dept'] = dept_id
        if role_id:
            emps = emps.filter(role_id=role_id)
            query['role'] = role_id
        if min_salary:
            emps = emps.filter(salary__gte=int(min_salary))
            query['min_salary'] = min_salary
        if max_salary:
            emps = emps.filter(salary__lte=int(max_salary))
            query['max_salary'] = max_salary
        if search:
            from django.db.models import Q
            emps = emps.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))
            query['search'] = search

    context = {
        'emps': emps,
        'departments': departments,
        'roles': roles,
        'query': query,
    }
    return render(request, 'filter_emp.html', context)
