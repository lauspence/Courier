from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, JobForm, CustomerForm, CourierRegistrationForm
from googlemaps import Client as GoogleMaps
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Home page view
def home(request):
    return render(request, 'home.html')

# Initialize Google Maps API client
gmaps = GoogleMaps(settings.GOOGLE_MAPS_API_KEY)

def get_location_name(lat, lng):
    """Reverse geocode the lat/lng to get a location name"""
    result = gmaps.reverse_geocode((lat, lng))
    if result:
        return result[0]['formatted_address']  # Get the formatted address
    return "Unknown Location"


# Customer Registration
def customer_registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'register.html', context)

# Login Page
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_job')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)

# Logout User
def logoutUser(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page

# Customer Create Job Page
@login_required(login_url='login')
def create_job(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return redirect('create-customer-profile')  # Redirect to customer profile if not found

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.customer = customer  # Assign the customer to the job

            # Reverse geocode pickup and delivery latitudes and longitudes
            pickup_lat = job.pickup_lat
            pickup_lng = job.pickup_lng
            delivery_lat = job.delivery_lat
            delivery_lng = job.delivery_lng

            # Get the location names
            job.pickup_location = get_location_name(pickup_lat, pickup_lng)
            job.delivery_location = get_location_name(delivery_lat, delivery_lng)

            # Save the job
            job.save()
            return redirect('job-list')  # Redirect to the job list page after saving
    else:
        form = JobForm()

    return render(request, 'create_job.html', {'form': form})

# Create Customer Profile
@login_required(login_url='login')
def create_customer_profile(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)  # Check if the customer exists
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('create_job')  # Redirect to create job after profile creation
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'create_customer_profile.html', {'form': form})

# Job List Page
@login_required(login_url='login')
def job_list(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return redirect('create-customer-profile')  # Redirect to profile creation page if customer doesn't exist
    
    jobs = Job.objects.filter(customer=customer)  # Get all jobs for the customer
    
    return render(request, 'job_list.html', {'jobs': jobs})

# Accept Job (for customer)
def customer_accept_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.is_accepted = True  # Mark the job as accepted
    job.save()
    return redirect('courier_dashboard')  # Redirect back to the courier dashboard

# Job Details Page
def job_details(request, job_id):
    customer = get_object_or_404(Customer, user=request.user)
    job = get_object_or_404(Job, id=job_id, customer=customer)
    return render(request, 'job_details.html', {'job': job})

# Edit Job Page
@login_required(login_url='login')
def edit_job(request, job_id):
    customer = get_object_or_404(Customer, user=request.user)
    job = get_object_or_404(Job, id=job_id, customer=customer)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job-list')
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})

# Delete Job
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('job-list')
@login_required
def courier_dashboard(request):
    try:
        courier_profile = CourierProfile.objects.get(user=request.user)
    except CourierProfile.DoesNotExist:
        # If no CourierProfile exists, redirect to home page or show a message
        return redirect('home')

    # Fetch the Courier instance related to the CourierProfile
    try:
        courier = Courier.objects.get(user=request.user)
    except Courier.DoesNotExist:
        courier = None  # Handle if the Courier instance doesn't exist

    if not courier:
        # If no courier instance is found, redirect to the profile creation page
        return redirect('profile_creation')  # Or provide a message asking them to create a profile

    # Fetch available jobs that are 'pending' and not already assigned to this courier
    available_jobs = Job.objects.filter(status='pending').exclude(courier=courier).select_related('courier')  # Optimizing by using select_related for the 'courier' ForeignKey field

    return render(request, 'courier_dashboard.html', {
        'courier_profile': courier_profile,
        'available_jobs': available_jobs,
    })


# Accept Job (for courier)


@login_required
def accept_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    try:
        courier_profile = CourierProfile.objects.get(user=request.user)
    except CourierProfile.DoesNotExist:
        return redirect('profile_creation')

    if job.status == 'accepted':
        return redirect('courier_dashboard')

    # Assign job to the courier
    try:
        courier = Courier.objects.get(user=request.user)
    except Courier.DoesNotExist:
        return redirect('profile_creation')

    job.courier = courier
    job.status = 'accepted'
    job.save()

    # Pass job details to template for map rendering
    context = {
        'job': job
    }
    return render(request, 'accept_job.html', context)

@login_required
def start_delivery(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return redirect('courier_dashboard')

    # Check if the job is already in progress
    if job.status == 'in_progress':
        return redirect('courier_dashboard')

    job.status = 'in_progress'
    job.save()

    # Optionally: Notify the customer that the delivery has started
    send_mail(
        'Job In Progress',
        f'Your job {job.id} is now in progress.',
        'from@example.com',
        [job.customer.user.email],
        fail_silently=False,
    )

    return redirect('courier_dashboard')




# Courier Registration
def courier_registration(request):
    if request.method == "POST":
        form = CourierRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('courier_login')
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        form = CourierRegistrationForm()

    return render(request, "courier_registration.html", {"form": form})

# Courier Login
def courier_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'courier'):
                login(request, user)
                return redirect("courier_dashboard")
            else:
                messages.error(request, "You are not authorized as a courier.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "courier_login.html")




def update_job_status(request, job_id, new_status):
    job = get_object_or_404(Job, id=job_id)

    # Step 1: Track the previous status (optional)
    previous_status = job.status

    # Step 2: Validate if the status transition is allowed
    valid_transitions = {
        'accepted': ['in_progress'],
        'in_progress': ['completed'],
    }

    if new_status not in valid_transitions.get(job.status, []):
        # Invalid transition response
        return JsonResponse({'status': 'error', 'message': 'Invalid status transition'}, status=400)

    # Step 3: Update the job status
    job.status = new_status
    job.save()  # Save the new status

    # Step 4: Create a DeliveryHistory entry for this status change (if necessary)
    if job.courier:  # Ensure that the job has an associated courier
        DeliveryHistory.objects.create(
            courier=job.courier,
            job=job,
            status=new_status,
            completed_at=timezone.now()
        )

    # Step 5: Return JSON response with the updated status and timestamp
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': new_status,
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        })

    # If it's a regular request, redirect to the accept_job page
    return redirect('accept_job', job_id=job.id)


@login_required
def customer_accept_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if job is pending
    if job.status == 'pending':
        job.status = 'in_progress'  # Update job status to 'in_progress'
        job.save()

    # Render the customer_accept_job page for the customer
    return render(request, 'customer_accept_job.html', {'job': job})

def profile_creation(request):
    # Your logic for profile creation
    return render(request, 'profile_creation.html')

@login_required
def start_delivery(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Ensure the job belongs to the current courier
    if job.courier == request.user.courier:  # Assuming Courier model is linked to the user
        if job.status == 'accepted':
            job.status = 'in_progress'
            job.save()  # Save the updated job status
            return redirect('courier_dashboard')  # Redirect to the courier's dashboard or wherever appropriate

    return redirect('job-list')  # Redirect if something goes wrong


@login_required
def update_job_status(request, job_id, new_status):
    # Fetch the job object
    job = get_object_or_404(Job, id=job_id)

    # Ensure the job status is only updated to a valid next step
    valid_transitions = {
        'accepted': ['in_progress'],
        'in_progress': ['completed'],
    }

    # Check if the new status is a valid transition
    if new_status not in valid_transitions.get(job.status, []):
        return JsonResponse({'status': 'error', 'message': 'Invalid status transition'})

    # Update the job status
    job.status = new_status
    job.save()

    # Create a delivery history entry
    if job.courier:
        DeliveryHistory.objects.create(
            courier=job.courier,
            job=job,
            status=new_status,
            completed_at=timezone.now()
        )

    # Prepare the response data
    return JsonResponse({
        'status': new_status,
        'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    })


@login_required
def mark_job_as_completed(job_id):
    try:
        # Get the job object
        job = Job.objects.get(id=job_id)

        # Ensure the job status is not already completed
        if job.status != 'completed':
            job.status = 'completed'
            job.save()

            # Add entry to DeliveryHistory if the job has a courier
            if job.courier:
                DeliveryHistory.objects.create(
                    courier=job.courier,
                    job=job,
                    status='completed',
                    completed_at=timezone.now()
                )

            return "Job marked as completed."
        else:
            return "Job is already completed."
    except Job.DoesNotExist:
        return "Job not found."

@login_required   
def get_job_status(request, job_id):
    job = Job.objects.get(id=job_id)
    return JsonResponse({'status': job.status})
    
@login_required
def complete_job(request, job_id):
    # Call the function to mark the job as completed
    message = mark_job_as_completed(job_id)

    # Optionally, you can return a response or redirect based on success
    return render(request, 'job/complete_confirmation.html', {'message': message})

@login_required
def courier_delivery_history(request):
    # Fetch the courier object associated with the logged-in user
    courier = Courier.objects.get(user=request.user)

    # Fetch all completed delivery history entries for this courier
    delivery_history = courier.delivery_history.all()

    # Render the delivery history in a template
    return render(request, 'courier/delivery_history.html', {'delivery_history': delivery_history})



@login_required
def customer_job_list(request):
    try:
        customer = request.user.customer  # Access the Customer profile
    except Customer.DoesNotExist:
        return redirect('home')  # If the user is not a customer, redirect to home

    # Fetch ongoing and completed jobs for the customer
    ongoing_jobs = Job.objects.filter(customer=customer, status="in_progress")
    completed_jobs = Job.objects.filter(customer=customer, status="completed")
    
    context = {
        'ongoing_jobs': ongoing_jobs,
        'completed_jobs': completed_jobs,
    }
    return render(request, 'customer_job_list.html', context)

# View for courier job list
@login_required
def courier_job_list(request):
    try:
        courier = request.user.courier  # Access the Courier profile
    except Courier.DoesNotExist:
        return redirect('home')  # If the user is not a courier, redirect to home

    # Fetch jobs that are either pending or accepted and assigned to the courier
    available_jobs = Job.objects.filter(courier=None, status="pending")  # Jobs without assigned courier
    in_progress_jobs = Job.objects.filter(courier=courier, status="in_progress")

    context = {
        'available_jobs': available_jobs,
        'in_progress_jobs': in_progress_jobs,
    }
    return render(request, 'courier_job_list.html', context)
