
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project,  ProjectPurchase, Contact, Feedback

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'users/register.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username is not valid.')
            return redirect('login')
        
        # Try to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, f'You have successfully logged in with username: {username}')
            return redirect('home')
        else:
            # If authentication fails, check password validity
            messages.error(request, 'Password is not valid.')
            return redirect('login')

    return render(request, 'users/login.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')


def is_admin(user):
    return user.is_staff  # Allows access only to admin/staff users

def add_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_pdf = request.FILES.get('project_pdf')
        project_zip = request.FILES.get('project_zip')
        amount = request.POST.get('amount')
        category = request.POST.get('category')

        project = Project(
            project_name=project_name,
            project_pdf=project_pdf,
            project_zip=project_zip,
            amount=amount,
            category=category
        )
        project.save()
        messages.success(request, 'Project added successfully.')

    return render(request, 'admin/add_project.html')

def project_list(request):
    projects = Project.objects.all()
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)


    return render(request, 'users/project_list.html', {
        'projects': projects,
        'purchased_projects': purchased_projects
    })


from django.shortcuts import render
from .models import Project

def ml_projects(request):
    projects = Project.objects.filter(category='ML')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/ml_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def aws_projects(request):
    projects = Project.objects.filter(category='AWS')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/aws_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def react_projects(request):
    projects = Project.objects.filter(category='React')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/react_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def flask_projects(request):
    projects = Project.objects.filter(category='Flask')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/flask_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def python_projects(request):
    projects = Project.objects.filter(category='Python')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/python_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def django_projects(request):
    projects = Project.objects.filter(category='Django')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/django_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def php_projects(request):
    projects = Project.objects.filter(category='PHP')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/php_projects.html', {'projects': projects,'purchased_projects': purchased_projects})

def azure_projects(request):
    projects = Project.objects.filter(category='Azure')
    purchased_projects = ProjectPurchase.objects.filter(user=request.user, purchased=True).values_list('project_id', flat=True)
    return render(request, 'users/azure_projects.html', {'projects': projects,'purchased_projects': purchased_projects})


def initiate_payment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return redirect('project_list',{'project':project})


import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Project, ProjectPurchase
from django.contrib import messages

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_payment(request, project_id):
    project = get_object_or_404(Project, serial_number=project_id)

    # Create Razorpay order
    order_amount = int(project.amount * 100)
    order_currency = 'INR'
    order_receipt = f'order_rcptid_{project_id}'

    # Razorpay order creation
    razorpay_order = razorpay_client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "receipt": order_receipt,
        "payment_capture": "1"
    })

    # Save order details in ProjectPurchase model
    purchase = ProjectPurchase.objects.create(
        user=request.user,
        project=project,
        order_id=razorpay_order['id']
    )

    return render(request, 'users/payment_page.html', {
        'project': project,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_amount': order_amount
    })



def my_orders(request):
    purchases = ProjectPurchase.objects.filter(user=request.user, purchased=True).select_related('project')
    return render(request, 'users/my_orders.html', {'purchases': purchases})


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('order_id')

        try:
            purchase = ProjectPurchase.objects.get(order_id=order_id)
            purchase.razorpay_payment_id = razorpay_payment_id
            purchase.purchased = True
            purchase.save()
            messages.success(request, 'Payment was successful.')

            return redirect('my_orders')
        except ProjectPurchase.DoesNotExist:
            messages.error(request, 'Payment verification failed.')
            return redirect('allprojects')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')  # Retrieve mobile number
        message = request.POST.get('message')

        # Save the feedback to the database
        feedback = Contact(name=name, email=email, mobile=mobile, message=message)
        feedback.save()

    return render(request, "users/contact.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project

def remove_project(request):
    if request.method == 'POST':
        serial_number = request.POST.get('serial_number')

        try:
            # Find the project with the given serial number
            project = Project.objects.get(serial_number=serial_number)
            project.delete()  # Delete the project from the database
            messages.success(request, f'Project with serial number {serial_number} has been removed successfully.')
        except Project.DoesNotExist:
            messages.error(request, f'No project found with serial number {serial_number}.')

        return redirect('remove_project')  # Redirect back to the remove project page

    return render(request, 'admin/remove_project.html')

def home(request):
    return render(request,"users/home.html")


def allprojects(request):
    return render(request,"users/allprojects.html")

def about(request):
    return render(request,"users/about.html")

def callback(request):
    call=Contact.objects.all()
    return render(request,"admin/callback.html",{'call':call})

def admindashboard(request):
    return render(request,"admin/admin_dashboard.html")

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback')

        # Save feedback in the database
        feedback = Feedback(name=name, email=email, feedback=feedback_text)
        feedback.save()
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('feedback')  # Redirect back to feedback page

    return render(request, 'users/feedback.html')

def projects(request):
    all_projects = Project.objects.all()
    return render(request, 'admin/projects.html', {'all_projects': all_projects})

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.project_name = request.POST.get('project_name')
        if 'project_pdf' in request.FILES:
            project.project_pdf = request.FILES.get('project_pdf')
        if 'project_zip' in request.FILES:
            project.project_zip = request.FILES.get('project_zip')
        project.amount = request.POST.get('amount')
        project.category = request.POST.get('category')
        project.save()
        messages.success(request, 'Project updated successfully.')
        return redirect('projects')

    return render(request, 'admin/edit_project.html', {'project': project})

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('projects')

def adminfeed(request):
    feed=Feedback.objects.all()
    return render(request, 'admin/adminfeedback.html',{'feed':feed})

def userdetails(request):
    user=User.objects.all()
    return render(request, 'admin/user_details.html',{'user':user})


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Hardcoded credentials
        admin_username = "admin"
        admin_password = "admin"

        if username == admin_username and password == admin_password:
            # Redirect to the admin dashboard
            return redirect('/admindashboard/')
        else:
            # Display an error message
            messages.error(request, "Invalid username or password.")
            return redirect('admin_login')  # Redirect back to the login page with an error message

    return render(request, 'admin/admin_login.html')
 
def sorry(request):
    return render(request, 'users/sorry.html')


def purchase_details_view(request):
    purchases = ProjectPurchase.objects.select_related('user', 'project').all()
    return render(request, 'admin/purchase_details.html', {'purchases': purchases})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Step 1: Email verification for password reset
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        
        if user:
            # Email exists: redirect to password reset form
            request.session['reset_user_id'] = user.id  # Save user ID in session
            return redirect('password_reset_form')
        else:
            messages.error(request, 'The email is not registered. Please try again.')

    return render(request, 'users/password_reset_request.html')

# Step 2: Form to reset password
def password_reset_form(request):
    if 'reset_user_id' not in request.session:
        return redirect('password_reset_request')  # Ensure the flow is valid

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
        else:
            user_id = request.session.pop('reset_user_id')  # Retrieve and remove user ID from session
            user = User.objects.get(id=user_id)
            user.set_password(new_password)  # Update password
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')

    return render(request, 'users/password_reset_form.html')
