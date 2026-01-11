from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('search/', views.home, name='search'),  # 👈 This line added
    path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),  # ✅ new
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
            # still keep this for root
]