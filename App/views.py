from django.utils import timezone
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import ServiceDemandForm, SignUpForm, RejectionReason
from django.contrib import messages
import datetime
from django.shortcuts import get_object_or_404

# Rest of your code...

# Create your views here.

# hold the login

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Set session value
                request.session['session_started'] = True
                request.session.set_expiry(3600) 

                return redirect('index')  # Replace 'home' with the appropriate URL name for your home page
            else:
                messages.error(request, 'Invalid email or password.')
            
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

# hold the signup

from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail

from .forms import SignUpForm, LoginForm
from .models import AcceptedCommand, Client, CompletedCommand, ServiceDemand, personnel, projet, service, detail, equipe
from django.shortcuts import render
from django.db.models import Count, F, FloatField, ExpressionWrapper, Sum
from django.db.models.functions import Coalesce
from .models import ServiceDemand, AcceptedCommand, CompletedCommand, Client, service, personnel

# views.py
from django.db.models.functions import ExtractMonth

@login_required
def Dashboard(request):
    # Get all available services
    all_services = service.objects.all()

    # Count total number of commands
    total_commands = ServiceDemand.objects.count()

    # Annotate the count and percentage for each service
    service_type_data = (
        all_services
        .annotate(
            service_type_count=Count('servicedemand'),
            percentage=ExpressionWrapper(
                (Count('servicedemand') * 100.0) / total_commands,
                output_field=FloatField()
            )
        )
    )

    # Calculate total incomes
    total_incomes = ServiceDemand.objects.aggregate(total=Coalesce(Sum('price'), 0, output_field=FloatField()))['total']

    # Get the best customer
    best_customer = ServiceDemand.objects.values('client__name').annotate(total_commands=Count('id')).order_by('-total_commands').first()

    # Get the most and least sold service types
    most_sold_service = ServiceDemand.objects.values('service_type__type').annotate(total_sold=Count('id')).order_by('-total_sold').first()
    least_sold_service = ServiceDemand.objects.values('service_type__type').annotate(total_sold=Count('id')).order_by('total_sold').first()

    # Calculate total completed commands this month
    current_month = timezone.now().month
    total_completed_commands_this_month = ServiceDemand.objects.filter(
        completion_time__month=current_month
    ).count()

    # Get names and emails of users from the Client table
    clients_info = Client.objects.values('name', 'email')

    # Get the total number of accepted commands and completed commands
    total_accepted_commands = AcceptedCommand.objects.count()
    total_completed_commands = CompletedCommand.objects.count()

    clients = Client.objects.all()
    personnels = personnel.objects.all()
    projets = projet.objects.all()

    context = {
        'clients': clients,
        'personnels': personnels,
        'projets': projets,
    
        'total_commands': total_commands,
        'total_accepted_commands': total_accepted_commands,
        'total_completed_commands': total_completed_commands,
        'total_completed_commands_this_month': total_completed_commands_this_month,

        'service_type_data': service_type_data,
        'clients_info': clients_info,
        'total_incomes': total_incomes,
        'best_customer': best_customer,
        'most_sold_service': most_sold_service,
        'least_sold_service': least_sold_service,
    }

    return render(request, 'Dashboard.html', context)

@login_required
def Profile(request):
    clients = Client.objects.all()
    personnels = personnel.objects.all()
    projets = projet.objects.all()
    context = {
        'clients': clients,
        'personnels' : personnels,
        'projets' : projets
    }
    return render(request, 'profile.html', context)


def SignupView(request):
    form = SignUpForm()  # Initialize an empty instance of SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            pwd1 = form.cleaned_data.get('password1')
            pwd2 = form.cleaned_data.get('password2')
            if pwd1 != pwd2:
                messages.error(request, 'Passwords do not match')
            else:
                mail = form.cleaned_data.get('email')
                subject = 'Welcome to Our Service!'
                message = 'Thank you for signing up. Enjoy our services!'
                sent = send_mail(subject, message, 'boufaiedmortadha7@gmail.com', [mail], fail_silently=False)
                if sent:
                    user = Client.objects.create_user(
                        name=form.cleaned_data.get('name'),
                        email=form.cleaned_data.get('email'),
                        password=pwd1
                    )
                    user.save()

                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, 'An error occurred while sending the confirmation email. Please try again later.')
                    return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect

from django.contrib.auth import logout
from django.views import View

def index(request):
    Clients = Client.objects.all()
    personnels = personnel.objects.all()
    services = service.objects.all()
    details = detail.objects.all()
    equipes = equipe.objects.all()
    projets = projet.objects.all()

    context = {
        'services' : services,
        'Clients' : Clients,
        'projets' :projets,
        'personnels' : personnels,
        'details' : details,
        'equipes' : equipes,
    } 
    return render(request, 'index.html', context)

def contact(request):
    email_sent = False
    user_email = request.user.email   

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message') + f'\n {user_email}'

        from_email = request.user.email   
        to_email = 'boufaiedmortadha7@gmail.com'
        try:
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )
        except:
            pass  

        if email_sent:
            messages.success(request, 'Your message have been sent successfully!') 
    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ServiceDemand
from django.utils import timezone

def get_services(request):
    services = service.objects.all()
    demand_sent = False

    if request.method == 'POST':
        # Extract form data directly from the request
        service_type_id = request.POST.get('service_type')
        object_value = request.POST.get('object')
        details_value = request.POST.get('details')
        address_value = request.POST.get('address')
        country_value = request.POST.get('country')
        phone_value = request.POST.get('phoneNumber')

        # Create a ServiceDemand instance and populate its fields
        service_demand = ServiceDemand()
        service_demand.client = request.user
        service_demand.submission_date = timezone.now()
        service_demand.service_type_id = service_type_id
        service_demand.object = object_value
        service_demand.details = details_value

        # Save the address, country, and phone to the Client model
        request.user.address = address_value
        request.user.country = country_value
        request.user.phone = phone_value
        request.user.save()

        if 'commandebtn' in request.POST:
            service_demand.save()
            demand_sent = True

        subject = 'Command validation'
        message = 'We successfully received your command. We will try to answer you as soon as possible.'

        from_email = 'boufaiedmortadha7@gmail.com'  # use the email of the authenticated user
        to_email = request.user.email
        try:
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )
            email_sent = True
        except:
            pass

        if email_sent:
            messages.success(request, 'Your demand is received! We have sent an email of confirmation to you.')
            return redirect('index')

    else:
        # If it's not a POST request, create an empty form
        form = None

    context = {
        'services': services,
        'form': form,
        'demand_sent': demand_sent,
    }

    return render(request, 'index.html', context)

################################################################################

def ComandList(request):
    service_demands = ServiceDemand.objects.filter(is_accepted=False).order_by('-submission_date')
    
    context = {
        "servDem": service_demands
    }
    
    return render(request, 'comand_list.html', context)

# views.py
def accept_command(request, command_id):
    service_demand = get_object_or_404(ServiceDemand, id=command_id)

    # Check if an AcceptedCommand already exists for this ServiceDemand
    accepted_command, created = AcceptedCommand.objects.get_or_create(command=service_demand)

    # If not created, update the acceptance_date
    if not created:
        accepted_command.acceptance_date = timezone.now()
        accepted_command.save()

    service_demand.is_accepted = True
    service_demand.save()

    if request.method == 'POST':
        price = request.POST.get('price', '')
        service_demand.price = price

        if service_demand.is_accepted:
            subject = 'Command accepted'
            message = (
                f'Thank you for choosing our services! We are pleased to inform you that your command has been accepted.\n\n'
                f'Suggested Price: {price} Dinar\n\n'
                f'If you would like to proceed, please make the payment to confirm your order. You can pay securely by visiting the following link:\n\n'
                f'[Payment Verification Link](http://127.0.0.1:8000/payment/)\n\n'
                f'Once the payment is confirmed, we will proceed with your command. If you have any questions or need assistance, feel free to contact us via email at boufaiedmortadha7@gmail.com or visit our website.\n\n'
                f'We look forward to working with you!\n\nBest regards,\nThe [MarketMinds] Team'
            )

            from_email = 'boufaiedmortadha7@gmail.com' 
            to_email = service_demand.client.email

            try:
                send_mail(subject, message, from_email, [to_email], fail_silently=False)
                messages.success(request, 'An e-mail of confirmation was sent to the client.')
            except:
                messages.error(request, 'Error sending email.')

        # Save the ServiceDemand instance to persist the changes to the database
        service_demand.save()

    return redirect('comand_list')


def delete_command(request, command_id):
    command = get_object_or_404(ServiceDemand, id=command_id)

    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        subject = 'Command refused'
        message = f"Sorry to inform you that your command has been rejected for the following reasons:\n{reason}"
        from_email = 'boufaiedmortadha7@gmail.com' 
        to_email = command.client.email

        try:
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
            messages.success(request, 'An e-mail of confirmation was sent to the client.')
            command.delete()
            return redirect('comand_list')

        except:
            messages.error(request, 'Error sending email.')

    return render(request, 'comand_list.html', {'command': command})


###############################################################################""

def accepted_commands_list(request):
    accepted_commands = AcceptedCommand.objects.all()
    context = {
        'accepted_commands': accepted_commands,
    }
    return render(request, 'accepted_commands_list.html', context)

def complete_accepted_command(request, accepted_command_id):
    accepted_command = get_object_or_404(AcceptedCommand, id=accepted_command_id)

    # Add to CompletedCommand
    completed_command = CompletedCommand(command=accepted_command.command, completion_date=accepted_command.acceptance_date)
    completed_command.save()

    service_demand = accepted_command.command

    subject = 'Command Completed'
    message = 'Your command has been completed. Thank you for choosing our services.'
    from_email = 'boufaiedmortadha7@gmail.com'  # Replace with your email
    to_email = service_demand.client.email

    try:
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        messages.success(request, 'Email sent to the command owner.')
    except:
        messages.error(request, 'Error sending email.')    
    
    accepted_command.delete()

    return redirect('accepted_commands_list')

#####################################################################################

def completed_command_list(request):
    completed_commands = CompletedCommand.objects.all().order_by('-completion_date')

    context = {
        'completed_commands': completed_commands,
    }

    return render(request, 'completed_command_list.html', context)
#####################################################################################

def get_command_details(request, command_id):
    if request.method == 'POST':
        completed_command = get_object_or_404(CompletedCommand, id=command_id)

        context = { 
            'completed_commands': completed_command,
        }

        return render(request, 'command_details_by_id.html', context)