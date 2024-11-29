
from django.shortcuts import render, get_object_or_404, redirect
from app1.views import *
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,"index.html")



def adddept(request):
    return render(request,"adddept.html")

from django.shortcuts import render
from .models import Dept

def createdept(request):
    msg = ""  # Default message
    if request.method == 'GET':
        deptno = request.GET.get('deptno', '').strip()
        deptname = request.GET.get('dname', '').strip()

        # Validate deptno to be an integer
        if deptno.isdigit():
            deptno = int(deptno)
        else:
            msg = "Invalid Deptno. Please enter a valid number."
            return render(request, "adddept.html", context={'msg': msg})

        # Validate deptname is not empty
        if not deptname:
            msg = "Department Name cannot be empty."
            return render(request, "adddept.html", context={'msg': msg})

        try:
            # Create new department in the database
            d = Dept.objects.create(deptno=deptno, dname=deptname)
            d.save()
            msg = "Department Added Successfully!"
        except Exception:
            msg = f"Already Exits / Use Another Department Number"
    
    # Render the form with the result message
    return render(request, "adddept.html", context={'msg': msg})





def addemp(request):
    qs=Dept.objects.all()
    dept=[]
    for row in qs:
        dept.append(row.deptno)
    return render(request,"addemp.html",{'dept':dept})

def create_emp(request):
    msg = ""  # Default message
    try:
        # Get data from the request
        empno = int(request.GET['empno'])  # Convert empno to integer
        ename = request.GET['ename']
        job = request.GET['job']
        sal = float(request.GET['sal'])  # Convert salary to float
        deptno = int(request.GET['deptno'])  # Convert deptno to integer
        
        # Check if deptno exists
        dept = Dept.objects.get(deptno=deptno)
        
        # Create employee
        e = Employee.objects.create(empno=empno, ename=ename, job=job, sal=sal, dept=dept)
        e.save()
        msg = "Employee Added Successfully"
    
    except ValueError:
        msg = "Invalid input data. Please make sure all fields are correct."
    except Dept.DoesNotExist:
        msg = "Department not found with the provided deptno."
    except Exception as e:
        msg = f"Enter Valid Details"
    return render(request, "addemp.html", context={'msg': msg})





def employee_list(request):
    # Fetch all employees
    employees = Employee.objects.all()
    
    # Render the employee list to the template
    return render(request, 'employee_list.html', {'employees': employees})


def delete_employee(request):
    empno = request.GET.get('empno')  # Get empno from the query parameter
    
    if empno:
        try:
            employee = get_object_or_404(Employee, empno=empno)
            employee.delete()
            messages.success(request, "Employee deleted successfully")
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found")
    
    return redirect('employee_list')  # Redirect back to the employee list page



def update_employee(request):
    if request.method == 'GET':
        # Get employee details based on empno passed in the query string
        empno = request.GET.get('empno')
        employee = get_object_or_404(Employee, empno=empno)
        context = {'employee': employee}
        return render(request, 'update_employee.html', context)

    elif request.method == 'POST':
        # Process the form submission
        empno = request.POST.get('empno')
        ename = request.POST.get('ename')
        job = request.POST.get('job')
        sal = request.POST.get('sal')
        deptno = request.POST.get('deptno')

        # Update the employee in the database
        employee = get_object_or_404(Employee, empno=empno)
        department = get_object_or_404(Dept, deptno=deptno)

        employee.ename = ename
        employee.job = job
        employee.sal = sal
        employee.dept = department
        employee.save()

        messages.success(request, 'Employee updated successfully!')
        return redirect('employee_list')
