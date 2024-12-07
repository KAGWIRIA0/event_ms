from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from events.models import Event, Client, Consultation


@login_required
# Create your views here.
def event_dashboard(request):
    return render(request, 'event_dashboard.html')

#Event List View
@login_required
def events_list(request):
    events = Event.objects.all()
    return render(request, 'events_list.html', {'events': events})


@login_required
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        event.client_id = client_id
        event.save()

        # Redirect to the event dashboard after approval
        return redirect('event_dashboard')  # Ensure 'event_dashboard' is a valid name


    # For GET requests, return 405 Method Not Allowed
    return HttpResponse("Method Not Allowed", status=405)

@login_required

def booked_events(request):
    # Fetch events with status "Booked"
    booked_events = Event.objects.filter(status='Booked')  # Adjust filter if needed
    return render(request, 'booked_events.html', {'booked_events': booked_events})

@login_required
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    clients = Client.objects.all()
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        # Logic to approve the event or link it with the client
        event.client_id = client_id  # assuming 'client_id' is the field
        event.save()

        # Add success message
        messages.success(request, 'Event approved successfully.')

        return redirect('event_dashboard')  # Adjust with your actual redirect URL

    return render(request, 'approve_event.html', {'event': event, 'clients': clients})


@login_required
def pie_chart(request):
    consultations = Consultation.objects.filter(created_at__year=2024)
    returned = consultations.filter(status='RETURNED').count()
    lost = consultations.filter(status='LOST').count()
    booked = consultations.filter(status='BOOKED').count()
    return JsonResponse({
        "title": "Grouped By Status",
        "data": {
            "labels": ["Returned", "Booked", "Lost"],
            "datasets": [{
                "data": [returned, lost, booked],
                "backgroundColor": ['#4e73df', '#1cc88a', '#36b9cc'],
                "hoverBackgroundColor": ['#2e59d9', '#17a673', '#2c9faf'],
                "hoverBorderColor": "rgba(234, 236, 244, 1)",
            }],
        }
    })


@login_required
def line_chart(request):
    consultations = Consultation.objects.filter(created_at__year=2024)
    grouped = consultations.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime("%b"))
    return JsonResponse({
        "title": "Consultations Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Count",
                "lineTension": 0.3,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)",
                "pointRadius": 3,
                "pointBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointBorderColor": "rgba(78, 115, 223, 1)",
                "pointHoverRadius": 3,
                "pointHoverBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointHoverBorderColor": "rgba(78, 115, 223, 1)",
                "pointHitRadius": 10,
                "pointBorderWidth": 2,
                "data": numbers,
            }],
        },
    })


@login_required
def bar_chart(request):
    consultations = Consultation.objects.filter(created_at__year=2024)
    grouped = consultations.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime('%b'))
    return JsonResponse({
        "title": "Consultations Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Total",
                "backgroundColor": "#4e73df",
                "hoverBackgroundColor": "#2e59d9",
                "borderColor": "#4e73df",
                "data": numbers,
            }],
        },
    })


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('event_dashboard')
        messages.warning(request, 'Invalid username or password!')
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cancel_event(request, event_id):
    # Get the event object by its ID
    event = get_object_or_404(Event, id=event_id)

    # Cancel the event (assume the Event model has a 'status' field)
    event.status = 'Cancelled'
    event.save()

    # Set a success message
    messages.success(request, f'The event "{event.name}" has been cancelled successfully!')

    # Redirect back to the booked events page
    return redirect('booked_events')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})