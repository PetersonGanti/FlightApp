from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, BookingForm
from .models import Flight, Booking



@login_required
def home(request):
    query_source = request.GET.get('source')
    query_dest = request.GET.get('destination')
    query_date = request.GET.get('departure_date')  

    flights = Flight.objects.all()

    if query_source and query_dest and query_date:
        flights = Flight.objects.filter(
            Q(source__icontains=query_source),
            Q(destination__icontains=query_dest),
            Q(departure_time__date=query_date)
        )

    return render(request, 'home.html', {
        'flights': flights,
        'source_query': query_source or '',
        'destination_query': query_dest or '',
        'departure_date_query': query_date or ''
    })



def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        print("🔽 POST Data:", request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.flight = flight
            booking.total_price = flight.price * booking.seats
            booking.save()
            print("booking saved for:",request.user)
            messages.success(request, 'Flight booked successfully!')
            return redirect('my_bookings')
        else:
            print("from errors:",form.errors)
    else:
        form = BookingForm()

    return render(request, 'book_flight.html', {
        'form': form,
        'flight': flight
    })
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('flight').order_by('-booked_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})
    
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking cancelled successfully.")
        return redirect('my_bookings')